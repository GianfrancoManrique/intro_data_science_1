# Caso de estudio: delincuencia y vulnerabilidad social en Lima Metropolitana

Este proyecto analiza la relación entre la incidencia de denuncias policiales y la vulnerabilidad social en los distritos de Lima Metropolitana. El estudio combina información administrativa, demográfica y socioeconómica para identificar patrones territoriales y describir diferencias entre distritos.

## Objetivo

Evaluar cómo se relacionan la delincuencia reportada y la vulnerabilidad social en Lima, considerando diferencias de población y distribución geográfica.

## Fuentes de datos

- Denuncias policiales registradas por distrito y año
- Población total por distrito
- Indicadores de necesidad básica insatisfecha (NBI)

## Metodología

1. Revisión y limpieza de datos
2. Normalización de identificadores geográficos
3. Unión de bases por UBIGEO
4. Agregación por distrito y año
5. Cálculo de la tasa de delitos por cada 10,000 habitantes
6. Análisis exploratorio y visualización

La métrica principal utilizada para comparar distritos con distinto tamaño poblacional es:

TASA_DELITOS_10K = (TOTAL_DELITOS / POBLACION_TOTAL) * 10000

## Estructura del repositorio

- [index.html](index.html): presentación pública del caso de estudio
- [notebooks/03_Recoleccion_EDA.ipynb](notebooks/03_Recoleccion_EDA.ipynb): notebook principal con recolección y EDA
- [02_merge_ejecucion.py](02_merge_ejecucion.py): ejecución del merge de datos
- [04_agregacion_temporal.py](04_agregacion_temporal.py): agregación temporal
- [05_eda.py](05_eda.py): análisis exploratorio y gráficos
- [data/raw](data/raw): datos originales
- [data/clean](data/clean): datos limpios y fusionados
- [data/processed](data/processed): datos preparados para análisis
- [results/eda](results/eda): gráficos y estadísticas generadas

## Ejecutar el proyecto

Se recomienda abrir el notebook principal en [notebooks/03_Recoleccion_EDA.ipynb](notebooks/03_Recoleccion_EDA.ipynb) y ejecutar cada celda en orden. Los gráficos se generan en el mismo notebook sin depender de imágenes precargadas.

## Nota metodológica

El análisis es de carácter descriptivo y exploratorio. Busca identificar patrones territoriales y asociaciones observadas en los datos, sin afirmar causalidad directa entre vulnerabilidad social y delincuencia.