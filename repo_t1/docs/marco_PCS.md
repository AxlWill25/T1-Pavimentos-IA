# Aplicación prevista del marco PCS

Referencia obligatoria: Yu, B., & Barter, R. (2024). Veridical data science. MIT Press. https://vdsbook.com/

## Predictibilidad

El problema se formula como clasificación binaria de fisura visible por recorte. La anotación C/U permite comparar predicciones con etiquetas existentes. La disponibilidad de etiquetas no garantiza buen desempeño. Se prevé informar sensibilidad de la clase con fisura y precisión, además de la referencia de mayoría. El desequilibrio de clases impide interpretar la exactitud por sí sola. Se reservarán grupos independientes para evaluación; la asignación de prefijos a fotografías originales debe verificarse antes de tratarla como un mapeo confirmado.

## Computabilidad

El inventario puede ejecutarse en Python leyendo el ZIP directamente. Genera metadatos y huellas SHA256 sin cargar todas las imágenes en memoria. El resumen registra la versión real de Python y Pillow. La fase predictiva se limitará inicialmente a modelos de tamaño compatible con el entorno que el equipo consiga; no se afirma un tiempo de entrenamiento o disponibilidad de GPU que todavía no se haya comprobado.

## Estabilidad

Se propone comparar las predicciones bajo cambios moderados de brillo y distintas particiones por grupo de origen. Las perturbaciones conservarán el contenido físico y la etiqueta visible. Las imágenes transformadas permanecerán en el mismo grupo que su original. Se documentarán las decisiones sobre preprocesamiento, semillas, umbrales y exclusiones. Los casos con respuestas inestables o puntuaciones cercanas al umbral se derivarán a revisión humana. Los umbrales se elegirán con validación y no sobre la prueba reservada.

## Límite de la T1

Estos compromisos describen cómo se evaluará la confiabilidad. T1 presenta el problema, datos, repositorio y justificación PCS; no informa un modelo entrenado ni demuestra aún predictibilidad o estabilidad. Los datos de USU no acreditan transferibilidad automática a pavimentos locales.
