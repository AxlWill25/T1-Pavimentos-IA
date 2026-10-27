"""Inventario reproducible de pavimentos SDNET2018 para la entrega T1.

No entrena modelos ni modifica las imágenes del archivo de origen.
Uso: python src/inventariar_sdnet.py SDNET2018.zip --salida resultado_t1
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import platform
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

SOURCE = "https://digitalcommons.usu.edu/all_datasets/48/"
REFERENCE_COUNTS = {"con_fisura": 2608, "sin_fisura": 21726, "total": 24334}
GROUP_NOTE = (
    "prefijo_archivo se obtiene del nombre antes del primer guion. "
    "La correspondencia prefijo-fotografia original es una inferencia, no un "
    "mapeo documentado por el README oficial. Se proponen particiones "
    "conservadoras por este prefijo, sujetas a verificar la correspondencia. "
    "No repartir aleatoriamente recortes hermanos entre entrenamiento y prueba."
)
FIELDS = [
    "ruta_zip", "nombre_original", "clase", "etiqueta", "ancho_px", "alto_px",
    "modo", "canales", "sha256", "prefijo_archivo", "grupo_origen_verificado",
    "legible", "error",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pavement_label(name: str):
    path = PurePosixPath(name.replace("\\", "/"))
    if path.suffix.lower() not in {".jpg", ".jpeg", ".jpe", ".png"}:
        return None
    parts = path.parts
    if "P" not in parts or path.parent.name not in {"CP", "UP"}:
        return None
    return ("con_fisura", 1) if path.parent.name == "CP" else ("sin_fisura", 0)


def font(size: int):
    for candidate in ["DejaVuSans.ttf", "Arial.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo_zip", type=Path)
    parser.add_argument("--salida", type=Path, default=Path("resultado_t1"))
    args = parser.parse_args()
    if not args.archivo_zip.is_file():
        parser.error(f"No existe {args.archivo_zip}. Descargue el ZIP oficial y revise la ruta.")
    if not zipfile.is_zipfile(args.archivo_zip):
        parser.error("El archivo no es un ZIP válido. Puede ser una página de error guardada como ZIP.")
    root = args.salida
    data = root / "datos"
    figures = root / "figuras"
    for directory in [data, figures, root / "docs"]:
        directory.mkdir(parents=True, exist_ok=True)

    rows, samples = [], {"con_fisura": [], "sin_fisura": []}
    count_readable, hashes, prefixes = Counter(), Counter(), set()
    with zipfile.ZipFile(args.archivo_zip) as archive:
        members = sorted(
            [member for member in archive.infolist()
             if not member.is_dir() and pavement_label(member.filename) is not None],
            key=lambda member: member.filename,
        )
        if not members:
            raise SystemExit("No se encontraron imágenes P/CP o P/UP. Verifique que usa SDNET2018.zip oficial.")
        for index, member in enumerate(members, start=1):
            category, label = pavement_label(member.filename)
            name = PurePosixPath(member.filename.replace("\\", "/")).name
            prefix = name.split("-", 1)[0] if "-" in name else ""
            if not re.fullmatch(r"\d+", prefix):
                prefix = ""
            prefixes.add(prefix)
            row = {key: "" for key in FIELDS}
            row.update(ruta_zip=member.filename, nombre_original=name, clase=category,
                       etiqueta=label, prefijo_archivo=prefix, legible=0)
            try:
                blob = archive.read(member)
                row["sha256"] = hashlib.sha256(blob).hexdigest()
                hashes[row["sha256"]] += 1
                with Image.open(io.BytesIO(blob)) as image:
                    image.load()
                    row.update(ancho_px=image.width, alto_px=image.height, modo=image.mode,
                               canales=len(image.getbands()), legible=1)
                    count_readable[category] += 1
                    # One example per observed prefix improves variety without
                    # asserting that this is a verified original-photo ID.
                    seen = {entry[0]["prefijo_archivo"] for entry in samples[category]}
                    if len(samples[category]) < 4 and prefix not in seen:
                        rgb = image.convert("RGB")
                        samples[category].append((row.copy(), rgb.copy()))
                        dest = data / "muestra" / ("C" if label else "U") / name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(blob)
            except Exception as error:
                row["error"] = f"{type(error).__name__}: {error}"
            rows.append(row)
            if index % 4000 == 0 or index == len(members):
                print(f"Inventariadas {index:,}/{len(members):,} imágenes", flush=True)

    with (data / "inventario_pavimentos.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    observed = Counter(row["clase"] for row in rows)
    readable_total = sum(count_readable.values())
    summary = {
        "fuente_primaria": SOURCE,
        "licencia_dataset": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "archivo_origen": args.archivo_zip.name,
        "bytes_archivo_origen": args.archivo_zip.stat().st_size,
        "sha256_archivo_origen_calculado": sha256_file(args.archivo_zip),
        "nota_checksum": "Huella calculada localmente para reproducibilidad; no afirma coincidencia con un checksum publicado.",
        "conteos_reportados_por_fuente": REFERENCE_COUNTS,
        "conteos_archivos_en_zip": dict(observed) | {"total": len(rows)},
        "conteos_imagenes_legibles": dict(count_readable) | {"total": readable_total},
        "archivos_no_legibles": len(rows) - readable_total,
        "duplicados_binarios_adicionales": sum(value - 1 for value in hashes.values() if value > 1),
        "grupos_sha256_repetidos": sum(value > 1 for value in hashes.values()),
        "prefijos_distintos_observados": len(prefixes - {""}),
        "advertencia_grupos_origen": GROUP_NOTE,
        "proporcion_con_fisura_en_archivos": observed["con_fisura"] / len(rows),
        "dimensiones_observadas": sorted({f'{r["ancho_px"]}x{r["alto_px"]}' for r in rows if r["legible"]}),
        "modos_observados": sorted({r["modo"] for r in rows if r["legible"]}),
        "entorno": {"python": platform.python_version(), "pillow": pillow_version},
        "alcance": "Inventario y documentación T1. Sin entrenamiento, EDA ni resultados predictivos.",
    }
    (data / "resumen_datos.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # Two rows: four real examples with cracks, then four without cracks.
    canvas = Image.new("RGB", (1200, 740), "white")
    draw = ImageDraw.Draw(canvas)
    for row_index, category in enumerate(["con_fisura", "sin_fisura"]):
        for col, (record, image) in enumerate(samples[category]):
            x, y = 20 + col * 295, 16 + row_index * 345
            image.thumbnail((270, 270))
            canvas.paste(image, (x, y))
            draw.text((x, y + 277), f'{"Con fisura C" if record["etiqueta"] else "Sin fisura U"}', fill="black", font=font(19))
            draw.text((x, y + 302), record["nombre_original"], fill="black", font=font(17))
    draw.text((20, 712), "Fuente SDNET2018 | Maguire, Dorafshan y Thomas (2018) | CC BY 4.0", fill="black", font=font(17))
    canvas.save(figures / "ejemplos_pavimentos.png")
    (root / "docs" / "criterio_de_grupos.md").write_text(
        "# Agrupación y prevención de fuga de información\n\n" + GROUP_NOTE + "\n\n"
        "grupo_origen_verificado queda vacío hasta comprobar el mapeo original. "
        "El prefijo se conserva como identificador auxiliar observado. "
        "Las variantes de brillo, recortes y aumentos derivados deberán permanecer en el mismo grupo.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"Salida creada en {root.resolve()}", flush=True)


if __name__ == "__main__":
    main()
