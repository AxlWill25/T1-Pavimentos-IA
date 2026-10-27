# Propuesta de IA para detectar fisuras superficiales en pavimentos rígidos con derivación de casos inciertos a inspección técnica

## Entrega T1

Propuesta de un sistema de IA para identificar fisuras visibles en imágenes de pavimentos rígidos y derivar los casos inciertos a revisión humana. El apoyo se limita al cribado visual. Una fotografía no permite calcular la capacidad portante, el espesor, la resistencia ni la vida remanente del pavimento.

## Autor y modalidad de trabajo

- Autor: Axel Williams Chevarría Rojas
- Usuario de GitHub: AxlWill25

## Datos

Se selecciona exclusivamente el subconjunto P de SDNET2018, publicado por Utah State University. La fuente reporta 24 334 recortes de pavimentos: 2608 con fisura (P/CP) y 21 726 sin fisura (P/UP). Los conteos realmente procesados y los archivos no legibles se registran en `datos/resumen_datos.json` cuando se ejecuta el inventario. Los recortes tienen 256 × 256 píxeles; las dimensiones y el modo de cada archivo se verifican con el script. El archivo ZIP original se conserva fuera de GitHub por su tamaño.

Fuente primaria y descarga: https://digitalcommons.usu.edu/all_datasets/48/

Licencia de los datos: Creative Commons Attribution 4.0 International (CC BY 4.0). Citar autores y conservar atribución. No se aplica esta licencia automáticamente al código del equipo.

## Organización

- `src/inventariar_sdnet.py`: inventario reproducible de imágenes, metadatos y huellas SHA256.
- `T1_inventario_Colab.ipynb`: cuaderno autónomo que descarga el ZIP oficial, ejecuta el inventario y prepara las evidencias.
- `datos/inventario_pavimentos.csv`: tabla de archivos realmente inventariados, después de la ejecución.
- `datos/resumen_datos.json`: conteos, dimensiones, legibilidad, duplicados binarios y versión del entorno, después de la ejecución.
- `datos/muestra/`: ocho archivos originales de ejemplo, después de la ejecución.
- `figuras/ejemplos_pavimentos.png`: ejemplos reales con nombre original y etiqueta.
- `docs/diccionario_datos.md`: significado de campos y límites de interpretación.
- `docs/fuente_datos.md`: procedencia y referencia.
- `docs/marco_PCS.md`: justificación de predictibilidad, computabilidad y estabilidad previstas.
- `docs/bitacora_ia.md`: registro que debe completar el equipo con su uso efectivo de IA.
- `docs/Informe_T1_pavimentos.docx`: colocar aquí el informe terminado.
- `evidencias/`: colocar aquí las capturas propias de GitHub, fuente y ejecución.

## Ejecución en Google Colab

1. Abrir https://colab.research.google.com/ y elegir Archivo > Subir cuaderno.
2. Seleccionar `T1_inventario_Colab.ipynb` de esta carpeta.
3. Ejecutar las celdas de arriba hacia abajo con el botón triangular. La primera descarga el ZIP oficial de aproximadamente 528 MB. Revisar los mensajes; no cerrar la pestaña durante la descarga.
4. Si la fuente bloquea la descarga, descargar `SDNET2018.zip` desde la ficha original en el navegador y usar el icono Archivos > Subir al almacenamiento de sesión. Volver a ejecutar la primera celda. Alternativa para un ZIP ya disponible en Drive: seguir el bloque opcional al final del cuaderno.
5. La última celda ofrece `evidencias_t1.zip`, que contiene el inventario, resumen, muestra y figura. Extraer ese ZIP en la computadora y subir sus carpetas al repositorio.

Ejecución local, si Python ya está instalado:

```bash
python -m pip install -r requirements.txt
python src/inventariar_sdnet.py SDNET2018.zip --salida resultado_t1
```

No se necesita entrenar modelos para T1. El inventario comprueba disponibilidad y documenta los datos; no es una evaluación predictiva.

## Aplicación prevista de PCS

Predictibilidad: la salida será presencia de fisura visible. Se prevé evaluar sensibilidad y precisión de la clase con fisura, frente a una referencia trivial de mayoría. La exactitud sola puede ocultar errores por el desequilibrio de clases. Separar grupos de origen antes de generar aumentos; verificar el mapeo de nombres a fotografía original.

Computabilidad: inventario en Python y procesamiento de imágenes de 256 × 256. Registrar versiones y recursos efectivos. No se ha demostrado aquí el tiempo de entrenamiento ni disponibilidad de GPU.

Estabilidad: se propone comprobar cambios de predicción ante pequeñas variaciones de iluminación y distintas particiones por grupo; los umbrales de abstención se definirán usando validación. Son verificaciones previstas, no resultados ejecutados de T1.

## Precaución sobre agrupación

El archivo incluye 104 prefijos numéricos distintos antes del primer guion, consistentes con las 104 fotografías de pavimentos descritas por la fuente. La correspondencia prefijo-fotografía no está documentada en el README original; se registra como inferencia. El campo `grupo_origen_verificado` permanece vacío. Se propone una partición conservadora por prefijo, sujeta a comprobar el mapeo. No mezclar recortes relacionados entre conjuntos de entrenamiento y prueba.

## Transparencia de IA

La IA se utiliza como apoyo a la organización, redacción y programación. La bitácora debe conservar el prompt inicial, refinamientos reales, responsables, fuentes verificadas y correcciones al código. No declarar pruebas o validaciones que el equipo no haya efectuado.

## Referencias

Maguire, M., Dorafshan, S., & Thomas, R. J. (2018). SDNET2018: A concrete crack image dataset for machine learning applications [Conjunto de datos]. Utah State University. https://doi.org/10.15142/T3TD19

Yu, B., & Barter, R. (2024). Veridical data science. MIT Press. https://vdsbook.com/

Dorafshan, S., Thomas, R. J., & Maguire, M. (2018). SDNET2018: An annotated image dataset for non-contact concrete crack detection using deep convolutional neural networks. Data in Brief, 21, 1664–1668. https://doi.org/10.1016/j.dib.2018.11.015
