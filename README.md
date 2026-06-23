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

**Secciones principales:**

1. **Carga y Preprocesamiento**: Integración de datasets limpios
2. **Ingeniería de Características**:
   - Tasa de Violencia contra la Mujer (TVM)
   - Índice de Vulnerabilidad
3. **Análisis Exploratorio (EDA)**:
   - Visualización geográfica de patrones
   - Análisis de distribuciones y relaciones entre variables
4. **Análisis de Correlaciones**: Identificación de relaciones entre vulnerabilidad y violencia
5. **Clustering**: Agrupación de distritos mediante K-Means, clustering jerárquico y NMF
6. **Análisis de PCA**: Reducción de dimensionalidad y visualización

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
- Primero ejecutar los notebooks **00** (en orden) para limpiar datos
- Luego ejecutar **01-tareas_dm.ipynb** para el análisis de data mining

## 📊 Visualizaciones Generadas

- Mapas de violencia (general y específico de Lima)
- Gráficos de correlación entre variables
- Análisis de varianza explicada (PCA)
- Visualizaciones 3D de clusters (K-Means, jerárquico, NMF)
- Métricas de evaluación de clustering
- Pairplot de variables con alta correlación

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
