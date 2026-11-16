# Análisis del catálogo de Netflix: Pandas, MapReduce y Databricks

Tecnologías Emergentes I · Segundo momento evaluativo · Unidad 3: Big Data y herramientas esenciales

**Equipo:** [Nombre del equipo]
**Integrantes:** [Integrante 1], [Integrante 2], [Integrante 3]

## Objetivo

Analizar el catálogo de Netflix para responder tres preguntas:

1. ¿Cuántas películas y series contiene?
2. ¿Qué actores participan en la mayor cantidad de títulos?
3. ¿Cuál es la duración promedio de las películas por país?

## Versiones utilizadas

| Herramienta | Versión |
|---|---|
| Python | [x.y.z] (`python --version`) |
| pandas | [x.y.z] (`pip show pandas`) |
| matplotlib | [x.y.z] (`pip show matplotlib`) |
| Docker Desktop | [x.y.z] |
| Imagen base del contenedor | Ubuntu 22.04 |
| Java | OpenJDK 8 |
| Hadoop (HDFS y Hadoop Streaming) | 3.3.6 |
| Databricks | Free Edition (Apache Spark, notebooks en Python y SQL) |

## Datos

- Origen: conjunto de datos *Netflix Movies and TV Shows* (Shivam Bansal), Kaggle.
- Archivo original: `netflix_titles.csv` (8 807 registros, 12 columnas).
- Archivo limpio: `netflix_clean.csv` (8 807 registros, 13 columnas).

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `netflix_titles.csv` | Archivo original de Kaggle |
| `netflix_clean.csv` | Archivo limpio (reto 1) |
| `01_limpiar_netflix.py` | Limpieza con Python y Pandas |
| `Dockerfile` | Contenedor con HDFS y Hadoop Streaming |
| `02_mapper_actores.py` | Mapper de MapReduce |
| `02_reducer_actores.py` | Reducer de MapReduce |
| `02_ejecutar_mapreduce.txt` | Comando completo de ejecución en Hadoop |
| `02_exportar_resultado.py` | Une las partes del resultado en un CSV |
| `mapreduce_actores.csv` | Títulos por actor, resultado de MapReduce |
| `03_analisis_netflix.ipynb` | Notebook de Databricks con resultados visibles |

## Pasos de ejecución, en orden

### Reto 1. Limpieza

1. Colocar `netflix_titles.csv` en la carpeta de trabajo.
2. Instalar dependencias: `pip install pandas matplotlib`
3. Ejecutar: `python 01_limpiar_netflix.py`
4. Resultado: `netflix_clean.csv` y los indicadores de la Tabla 1 en pantalla.

### Reto 2. HDFS y MapReduce

1. Construir la imagen: `docker build -t hadoop-netflix .`
2. Iniciar el contenedor: `docker run -d --name hadoop -v "${PWD}:/work" hadoop-netflix` (PowerShell). Esperar unos 40 segundos.
3. Entrar al contenedor: `docker exec -it hadoop bash`
4. Cargar el archivo limpio en HDFS:
   ```
   hdfs dfs -mkdir -p /data/netflix/clean
   hdfs dfs -put -f /work/netflix_clean.csv /data/netflix/clean/
   hdfs dfs -ls -h /data/netflix/clean/
   ```
5. Si existe una salida anterior: `hdfs dfs -rm -r -f /data/netflix/results/actores`
6. Ejecutar el comando de `02_ejecutar_mapreduce.txt`.
7. Descargar el resultado: `hdfs dfs -get /data/netflix/results/actores /work/actores_parts` y salir con `exit`.
8. Exportar el CSV final: `python 02_exportar_resultado.py`
9. Resultado: `mapreduce_actores.csv`.

### Reto 3 y 4. Databricks

1. Crear en Databricks un volumen `workspace.default.netflix` y subir `netflix_clean.csv` y `mapreduce_actores.csv`.
2. Importar `03_analisis_netflix.ipynb` y ejecutar las celdas en orden.
3. El notebook crea las tablas `workspace.default.netflix_clean` y `workspace.default.mapreduce_actores`, resuelve los análisis A, B y C con SQL y PySpark, compara sus resultados y compara MapReduce con Spark.
4. Los gráficos y la tabla de duración por país están al final del notebook.

## Resultados principales

- Títulos: 8 807 (6 131 películas y 2 676 series).
- Actor con más títulos: Anupam Kher (43).
- Mayor duración promedio entre los diez países con más películas: India (125,91 min).
- SQL y PySpark coinciden en los tres análisis; MapReduce y Spark coinciden en los 36 439 actores.

## Nota técnica

La exportación de `mapreduce_actores.csv` lee las partes con `quoting=csv.QUOTE_NONE`, para conservar las comillas dentro de nombres como `"Riley" Lakdhar Dridi`.