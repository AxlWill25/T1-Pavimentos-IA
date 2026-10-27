# Diccionario del inventario de pavimentos

Los campos siguientes son metadatos generados para documentar el dataset. No representan ensayos mecánicos ni variables originales de diseño. La entrada predictiva futura es la imagen y la variable objetivo es su etiqueta binaria.

| Campo | Tipo | Significado |
|---|---|---|
| ruta_zip | Texto | Ruta original del archivo dentro del ZIP oficial. |
| nombre_original | Texto | Nombre del recorte sin renombrarlo. |
| clase | Categórico | con_fisura o sin_fisura, según CP o UP. |
| etiqueta | Entero binario | 1 con fisura visible, 0 sin fisura visible según anotación original. |
| ancho_px | Entero | Ancho leído realmente, en píxeles. |
| alto_px | Entero | Alto leído realmente, en píxeles. |
| modo | Categórico | Modo de imagen leído por Pillow, por ejemplo RGB. |
| canales | Entero | Número de canales leído realmente. |
| sha256 | Texto | Huella de bytes del recorte para identificar duplicados exactos. |
| prefijo_archivo | Texto | Cadena antes del primer guion del nombre. Se conserva como texto para mantener ceros iniciales. |
| grupo_origen_verificado | Texto | Vacío hasta verificar el mapeo a la fotografía original. |
| legible | Entero binario | 1 si Pillow pudo abrir y cargar toda la imagen; 0 si falló. |
| error | Texto | Excepción observada si la imagen no se pudo leer. |

Las imágenes RGB de 256 × 256 contienen 196 608 valores de intensidad por recorte. No se deben anunciar los 13 campos de este inventario como 13 predictores mecánicos. Los píxeles se utilizan como entrada visual; la transformación a características depende del modelo futuro.

El CSV usa UTF-8 con BOM para facilitar su apertura en Excel. Importar prefijo_archivo como texto, para conservar valores como 001.
