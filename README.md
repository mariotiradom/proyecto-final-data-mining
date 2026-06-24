# Análisis de Vulnerabilidad y Violencia contra la Mujer en Distritos de Lima

Proyecto de Data Mining que analiza los patrones de vulnerabilidad y violencia contra la mujer en los distritos de Lima, combinando datos de denuncias, indicadores socioeconómicos y variables demográficas.

## 📊 Descripción del Proyecto

Este proyecto realiza un análisis integral de la situación de vulnerabilidad y violencia contra la mujer en Lima mediante técnicas de data mining y análisis exploratorio. Se construyen indicadores clave (Tasa de Violencia contra la Mujer y Índice de Vulnerabilidad) para identificar patrones, correlaciones geográficas y agrupar distritos según su perfil de riesgo.

## 📁 Estructura del Proyecto

```
.
├── notebooks/
│   ├── 00-limpieza-denuncias.ipynb      # Limpieza de datos de denuncias
│   ├── 00-limpieza-enaho.ipynb          # Limpieza de datos ENAHO (socioeconómicos)
│   ├── 00-limpieza_poblacion.ipynb      # Limpieza de datos de población
│   └── 01-tareas_dm.ipynb               # Análisis principal y data mining
├── data/
│   ├── raw/                             # Datos originales
│   └── processed/                       # Datos procesados
├── requirements.txt
└── README.md
```

## 🔄 Flujo de Ejecución

### Fase 0: Limpieza de Datos
Los notebooks que comienzan con **00** preparan los datos originales:

- **00-limpieza-denuncias.ipynb**: Procesa datos de denuncias por violencia
- **00-limpieza-enaho.ipynb**: Limpia y prepara indicadores socioeconómicos (ENAHO)
- **00-limpieza_poblacion.ipynb**: Procesa datos demográficos de población

Salida: Datasets limpios en `data/processed/`

### Fase 1: Data Mining y Análisis (01-tareas_dm.ipynb)

Secciones principales y últimas modificaciones:

1. Carga y Preprocesamiento: integra datasets limpios en la base final (base_final_lima).
2. Ingeniería de Características: TVM, Índice de Vulnerabilidad, nuevas variables y tratamiento mejorado de NA.
3. Análisis Exploratorio (EDA): mapas, distribuciones y relaciones entre variables.
4. Análisis de Correlaciones: identificación de relaciones clave.
5. Clustering: K-Means, jerárquico y NMF — parámetros guardados para reproducibilidad.
6. PCA: reducción de dimensionalidad y visualización.

Actualizaciones clave: 01-tareas_dm.ipynb fue actualizado con mejoras en la ingeniería de variables, persistencia de parámetros de clustering y pasos reproducibles que usan base_final_lima como la base final sobre la que se ejecutan los análisis.

## 📦 Requisitos

- Python 3.8+
- pandas
- geopandas
- matplotlib
- seaborn
- pyreadstat
- openpyxl
- mlxtend
- scikit-learn (incluido con pandas/análisis)

## 🚀 Instalación y Ejecución

### 1. Crear entorno virtual
```bash
python -m venv .dm-proyecto-venv
source .dm-proyecto-venv/bin/activate  # En Windows: .dm-proyecto-venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar análisis

Orden secuencial del código:

1. Ejecutar 00-limpieza-denuncias.ipynb
2. Ejecutar 00-limpieza-enaho.ipynb
3. Ejecutar 00-limpieza_poblacion.ipynb
4. Ejecutar el script/notebook que crea la base final: base_final_lima (fusión/join de los outputs en data/processed/)
5. Ejecutar 01-tareas_dm.ipynb (usa base_final_lima como entrada principal)
6. (Opcional) Ejecutar dashboard: `streamlit run streamlit_app.py`

## 📊 Visualizaciones Generadas

- Mapas de violencia (general y específico de Lima)
- Gráficos de correlación entre variables
- Análisis de varianza explicada (PCA)
- Visualizaciones 3D de clusters (K-Means, jerárquico, NMF)
- Métricas de evaluación de clustering
- Pairplot de variables con alta correlación
- Dashboard interactivo en Streamlit con mapa choropleth nacional y distrital por región

## 📈 Resultados Clave

El análisis identifica:
- Patrones geográficos de violencia y vulnerabilidad en Lima
- Correlaciones entre indicadores socioeconómicos y violencia contra la mujer
- Agrupaciones de distritos con perfiles similares de riesgo
- Componentes principales que explican la varianza en los datos

## 📝 Notas

- Los datos procesados se almacenan en `data/processed/` para referencia
- Las visualizaciones se guardan en el directorio `notebooks/`
- El análisis principal está centralizado en `01-tareas_dm.ipynb`
