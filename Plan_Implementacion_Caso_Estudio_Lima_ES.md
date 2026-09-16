# Plan de Implementación: Recolección de Datos + EDA para el Caso de Estudio de Lima Metropolitana

## 1. Objetivo del trabajo

El proyecto se centra en dos etapas principales:

1. Recolección y preparación de datos.
2. Exploratory Data Analysis (EDA) para identificar patrones, distribuciones, relaciones y anomalías entre la delincuencia y la vulnerabilidad socioeconómica en Lima Metropolitana.

La finalidad no es construir un modelo predictivo avanzado ni un sistema final, sino responder preguntas de exploración con datos reales utilizando los conceptos vistos en los notebooks compartidos.

---

## 2. Pregunta de investigación

> ¿Existen diferencias relevantes entre los distritos de Lima Metropolitana en términos de incidencia delictiva y vulnerabilidad socioeconómica, y qué patrones pueden observarse mediante un análisis exploratorio de datos?

---

## 3. Alcance y enfoque

* **Unidad de análisis:** distrito
* **Cobertura:** 43 distritos de Lima Metropolitana
* **Clave de integración:** `UBIGEO`
* **Enfoque principal:** EDA con visualización y estadística descriptiva
* **No se contempla como objetivo principal:** clustering, modelado predictivo, mapas geoespaciales avanzados ni pipelines de ML

---

## 4. Fuentes de datos a recolectar

### 4.1. Datos de seguridad ciudadana
* Fuente sugerida: MININTER / datosabiertos.gob.pe / observatorio de seguridad ciudadana
* Variables esperadas:
  * `UBIGEO`
  * `DISTRITO`
  * `TIPO_DELITO`
  * `FECHA` o año
  * `CANTIDAD` o conteo de delitos

### 4.2. Datos socioeconómicos y demográficos
* Fuente sugerida: INEI / indicadores distritales / datos municipales
* Variables esperadas:
  * `UBIGEO`
  * `DISTRITO`
  * `POBLACION_TOTAL`
  * `% NBI` o indicador equivalente de vulnerabilidad

### 4.3. Datos geográficos (opcionales)
* Solo como apoyo visual
* Se pueden usar para un mapa básico si se cuenta con shapefiles o GeoJSON
* No es obligatorio para la parte central del trabajo

---

## 5. Fase 1: Recolección y organización de datos

### Paso 1.1: Definir el periodo de análisis
* Elegir un año o un conjunto de años con información disponible.
* Mejor si el análisis es anual, porque facilita la comparación entre distritos.

### Paso 1.2: Descargar los datasets
* Guardar una copia original en una carpeta `data/raw/`.
* Registrar la fuente y la fecha de acceso.

### Paso 1.3: Validar la estructura de cada archivo
* Revisar si existen columnas clave.
* Confirmar que los nombres de distritos y códigos `UBIGEO` sean consistentes.
* Verificar si los datos están en formato útil para agregación por distrito.

### Paso 1.4: Organizar archivos
Estructura sugerida:

```
project/
├── data/
│   ├── raw/
│   ├── clean/
│   └── processed/
├── notebooks/
├── results/
└── README.md
```

---

## 6. Fase 2: Limpieza y preparación de datos

Esta parte debe usarse como base para todo el EDA.

### Paso 2.1: Estandarizar la clave `UBIGEO`
* Convertir a texto.
* Completar con ceros a la izquierda hasta 6 dígitos.
* Filtrar solo distritos de Lima Metropolitana.

### Paso 2.2: Homogeneizar nombres
* Normalizar distrito y provincia.
* Corregir mayúsculas, espacios y errores de escritura.

### Paso 2.3: Revisar valores faltantes
* Identificar nulos y decidir si se eliminan, completan o se mantienen según el caso.
* Evaluar si hay distritos sin información en alguna base.

### Paso 2.4: Limpiar tipos de variables
* Convertir fechas a formato adecuado.
* Asegurar que columnas numéricas sean numéricas.
* Quitar duplicates o filas inconsistentes.

### Paso 2.5: Agregar por distrito
* Agrupar denuncias por UBIGEO / DISTRITO.
* Calcular:
  * total de delitos por distrito,
  * tasa de delitos por cada 10,000 habitantes,
  * número de tipos de delito reportados,
  * proporción o porcentaje de vulnerabilidad por distrito.

---

## 7. Fase 3: EDA siguiendo los conceptos de los notebooks

A continuación se detallan exactamente los temas que sí forman parte del trabajo y que se corresponden con los ejercicios y ejemplos mostrados.

### 7.1. EDA univariado
Estos conceptos son esenciales y se usan directamente en los notebooks.

* **Estadísticas descriptivas**
  * media
  * mediana
  * desviación estándar
  * mínimo y máximo
  * cuartiles
  * IQR
  * MAD

* **Histogramas**
  * distribución de delitos por distrito
  * distribución de población
  * distribución del % NBI

* **Boxplots**
  * detectar outliers
  * comparar rangos entre distritos

* **Q-Q plot**
  * evaluar si una variable se parece a una distribución normal
  * detectar sesgo y colas pesadas

* **Countplot**
  * para variables categóricas o ordinales
  * ejemplo: tipos de delito o niveles de vulnerabilidad

* **Densidad / KDE**
  * comparar distribución de precios o tasas entre grupos

### 7.2. EDA bivariado
Estos son los conceptos clave para explorar relaciones entre dos variables.

* **Scatterplot**
  * relación entre `% NBI` y tasa de delitos por 10 mil habitantes
  * relación entre población y total de delitos

* **Correlación**
  * Pearson
  * Spearman
  * interpretación de relaciones lineales o no lineales

* **Boxplot por grupo**
  * comparar la tasa de delitos por zona o por nivel de vulnerabilidad

* **Violin plot**
  * mostrar la forma de la distribución dentro de cada grupo

* **Line plot**
  * útil si se trabaja con series temporales o evolución anual

### 7.3. EDA multivariado
Estos temas aparecen en los notebooks y permiten enriquecer la interpretación.

* **Pairplot**
  * observar relaciones entre varias variables simultáneamente

* **Matriz de correlación con heatmap**
  * identificar variables muy relacionadas

* **FacetGrid / faceting**
  * comparar distribuciones por grupo usando paneles

* **Visualización por hue**
  * separar distritos o zonas por color dentro de un gráfico de dispersión

### 7.4. Transformaciones simples para mejor lectura
Estos conceptos son útiles y aparecen en los notebooks.

* Aplicar logaritmo cuando una variable tiene cola derecha muy larga.
* Usar el Q-Q plot para decidir si conviene transformar una variable.
* Interpretar el sesgo antes y después de la transformación.

---

## 8. Análisis sugerido para este caso

### 8.1. Análisis univariado
* Distribución del total de delitos por distrito.
* Distribución de la población por distrito.
* Distribución del % NBI.
* Distribución de la tasa de delitos por 10,000 habitantes.
* Identificación de outliers y distritos atípicos.

### 8.2. Análisis bivariado
* `% NBI` vs `tasa_delitos_10k`
* `población` vs `total_denuncias`
* `población` vs `tasa_delitos_10k`
* comparar tasas entre zonas o grupos de distritos

### 8.3. Análisis multivariado
* Combinar criminalidad, vulnerabilidad y población para observar si hay patrones más complejos.
* Ver si una relación se mantiene dentro de subgrupos de distritos.
* Mirar si ciertas variables están altamente correlacionadas y no aportan información nueva.

---

## 9. Visualizaciones mínimas que sí se pueden hacer con estos conceptos

1. Histograma de delitos por distrito
2. Boxplot de tasa de delitos por distrito
3. Scatterplot de % NBI vs tasa de delitos
4. Correlación con heatmap
5. Pairplot para comparar varias variables juntas
6. Violinplot o density plot para comparar grupos
7. FacetGrid para separar por zona o por tipo de distrito
8. Countplot de tipos de delitos si se tiene esa variable

---

## 10. Conceptos que sí bastan para este trabajo

Sí, estos conceptos bastan para cumplir la etapa de recolección + EDA del caso de estudio.

Se pueden hacer con seguridad:

* limpieza y preparación de datos,
* estadísticas descriptivas,
* histogramas,
* boxplots,
* scatterplots,
* correlaciones,
* heatmaps,
* pairplots,
* facetas,
* violín y densidad,
* detección de outliers,
* interpretación preliminar de relaciones.

Esto cubre perfectamente el objetivo de un estudio exploratorio y de presentación en clase.

---

## 11. ¿Qué no quedaría cubierto con estos conceptos?

Estos conceptos no bastan si el objetivo del trabajo incluye tareas más avanzadas, como:

* clustering (K-Means)
* mapas geoespaciales complejos con folium o geopandas
* modelado predictivo con regresión o clasificación
* feature engineering más avanzada
* dashboard interactivo
* pipeline de ML completo

Es decir, para una tarea de **recolección de datos + EDA**, sí es suficiente. Para una versión más avanzada del caso que incluya modelado, geospatial analytics o machine learning, se necesitarían conceptos adicionales.

---

## 12. Conclusión

El enfoque más realista y consistente con los notebooks entregados es:

- recolectar datos,
- limpiar y preparar la base,
- explorar distribuciones y relaciones,
- producir gráficas claras,
- interpretar hallazgos preliminares.

Con esto, se cumple el objetivo principal del trabajo y se aprovecha al máximo el material teórico y práctico de los notebooks.

---

## 13. Lista de chequeo final

- [ ] Descargar los datasets de delitos y socioeconómicos
- [ ] Validar columnas y clave `UBIGEO`
- [ ] Estandarizar nombres y limpiar valores vacíos
- [ ] Agregar los datos por distrito
- [ ] Realizar estadísticas descriptivas
- [ ] Graficar histogramas y boxplots
- [ ] Hacer scatterplots y correlaciones
- [ ] Analizar distribución por grupos con violin/density
- [ ] Usar pairplot y heatmap para inspección multivariada
- [ ] Redactar los hallazgos preliminares del EDA
- [ ] Preparar la presentación de clase

Este plan está alineado con los notebooks y con el nivel de trabajo que corresponde a recolección de datos + EDA.
