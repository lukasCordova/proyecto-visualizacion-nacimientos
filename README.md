# Análisis de Factores de Riesgo Perinatal en Chile

## Integrantes
- Lukas Córdova
- Cristopher Ramírez
- Felipe Molina

## Descripción del Problema y Motivación
La postergación de la maternidad y las brechas socioeducativas en Chile plantean nuevos desafíos en la salud materno-infantil. Este proyecto analiza cómo influyen las condiciones sociodemográficas en los desenlaces perinatales adversos (bajo peso al nacer y nacimiento prematuro). Este análisis puede entregar conclusiones que construyan una mejor salud pública en el país, pues correlaciona la desigualdad económica del país con la calidad de vida de quienes nacen aquí.

## Pregunta del Proyecto
¿De qué manera influyen la edad materna, el nivel educacional y la paridad (X) en la probabilidad de resultados perinatales adversos —bajo peso al nacer y prematurez— (Y) en Chile durante el período 2020-2023 (T)?

## Alcance
- **Población:** Recién nacidos vivos y madres registradas en Chile.
- **Período:** 2020–2023.
- **Límites:** Análisis enfocado en microdatos clínicos y sociodemográficos disponibles en registros hospitalarios oficiales.

## Fuente y Obtención de Datos
- **Fuente:** Departamento de Estadísticas e Información de Salud (DEIS) - Ministerio de Salud de Chile.
- **Acceso:** Descarga pública desde "https://deis.minsal.cl/" y "https://www.ine.gob.cl/"  (datos de Estadísticas Vitales - Nacimientos).
- **Ubicación local:** Los archivos `.csv` deben situarse dentro de `data/raw/`.

## Descripción del Dataset
El proyecto utiliza los registros vitales de nacimientos proporcionados por el Departamento de Estadísticas e Información de Salud (DEIS) del Ministerio de Salud de Chile. El conjunto de datos abarca el periodo 2020-2023 y contiene variables demográficas maternas (educación, estado civil) y variables clínicas del recién nacido (semanas de gestación, peso al nacer). El dataset ha sido preprocesado rigurosamente para conservar únicamente partos simples y valores dentro de rangos fisiológicos viables, transformando además el peso continuo en un indicador binario de riesgo clínico (Bajo Peso < 2500g).

## Instrucciones para Obtener los Datos
Debido a las restricciones de tamaño de GitHub, el archivo de datos crudos original (que pesa más de 100 MB) no está incluido en este repositorio. Para preparar los datos localmente:
1. Descarga el archivo de registros abiertos desde el portal del DEIS o solicita el archivo `Serie_Nacimientos_2020_2023.csv`.
2. Ubica este archivo crudo dentro de la carpeta `data/raw/`.
3. El preprocesamiento está automatizado. Puedes ejecutar el script independiente `limpiar_datos.py` o simplemente correr la aplicación web, la cual detectará los datos crudos, aplicará los filtros y generará automáticamente el archivo `nacimientos_valpo_limpio.csv` dentro de la carpeta `data/processed/`.

## Instrucciones para Ejecutar la Aplicación
1. Clona este repositorio en tu máquina local.
2. Abre una terminal en la raíz del proyecto y asegúrate de tener tu entorno virtual activado.
3. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install -r requeriments.txt


## Estructura del repositorio

* **ProyectoVIS/**
  * **app/** - Carpeta principal de la aplicación web.
    * `app.py` - Página 1: Contexto, métricas y preprocesamiento.
    * **pages/** - Subdirectorio que Streamlit usa para el menú lateral.
      * `2_Analisis_exploratorio.py`
      * `3_Analisis_Pregunta.py`
  * **data/** - Almacenamiento local de los datos (ignorado en Git).
    * **processed/** - Dataset limpio y estandarizado listo para visualización.
    * **raw/** - Dataset original crudo del DEIS.
  * **figures/** - Carpeta para exportar gráficos o almacenar imágenes estáticas.
  * **notebooks/** - Cuadernos Jupyter para exploración inicial (EDA).
  * **src/** - Carpeta para módulos o scripts auxiliares futuros.
  * `.gitignore` - Archivo para excluir datos pesados y archivos de caché de Git.
  * `limpiar_datos.py` - Script ETL independiente para limpiar y agrupar la data.
  * `README.md` - Documentación principal del proyecto.
  * `requeriments.txt` - Listado exacto de dependencias para reproducibilidad.
