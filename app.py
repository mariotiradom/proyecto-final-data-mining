# app.py
# Dashboard: Vulnerabilidad territorial y violencia contra la mujer en Lima Metropolitana, 2025
# Ejecutar con: streamlit run app.py

from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Observatorio VCM Lima 2025",
    page_icon="📍",
    layout="wide"
)

# -----------------------------
# Estilo visual
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.6rem 1.8rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #3b0a45 0%, #6d2a7a 55%, #9b4bb3 100%);
    color: white;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 1.85rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    letter-spacing: -0.3px;
}
.hero p {
    font-size: 0.97rem;
    opacity: 0.88;
    max-width: 680px;
    line-height: 1.5;
}
.card {
    padding: 1.1rem 1.2rem;
    border-radius: 14px;
    border: 1px solid #ebebeb;
    background: #ffffff;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    min-height: 130px;
}
.card h3 {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #1a1a1a;
}
.card p {
    font-size: 0.9rem;
    color: #555;
    line-height: 1.55;
}
.insight {
    padding: 1rem 1.1rem;
    border-left: 4px solid #6d2a7a;
    background: #faf4fd;
    border-radius: 0 10px 10px 0;
    margin-top: 0.8rem;
    font-size: 0.91rem;
    color: #3a3a3a;
    line-height: 1.6;
}
.warningbox {
    padding: 0.9rem 1rem;
    border-left: 4px solid #e67e22;
    background: #fff7ed;
    border-radius: 0 10px 10px 0;
    font-size: 0.9rem;
}
.figure-title {
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 0.2rem;
    color: #1a1a1a;
}
.step-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6d2a7a;
    margin-bottom: 0.15rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Configuración de imágenes
# -----------------------------
GRAFICOS_DIR = Path("graficos")

FIGURAS = {
    "Mapa territorial": {
        "archivo": "mapa_violencia_lima.png",
        "descripcion": "Distribución distrital de la tasa de violencia contra la mujer (TVM) y principales modalidades de violencia.",
        "lectura": "La violencia registrada presenta una distribución heterogénea en Lima Metropolitana. La violencia física y psicológica muestran mayor presencia territorial, mientras que la violencia sexual aparece más concentrada en zonas específicas. Esta variabilidad espacial sugiere que los factores explicativos operan a escala local."
    },
    "Vulnerabilidad vs TVM": {
        "archivo": "correlacion_vulnerabilidad_tvm.png",
        "descripcion": "Relación entre el índice de vulnerabilidad territorial y la TVM por distrito.",
        "lectura": "La dispersión de los distritos no revela una tendencia lineal positiva consistente entre vulnerabilidad territorial y tasa de denuncias registradas. Este hallazgo es central: una mayor precariedad estructural no se traduce necesariamente en más denuncias, lo que abre la posibilidad de que existan barreras de acceso que operan de forma diferenciada según el territorio."
    },
    "Matriz de correlación": {
        "archivo": "matriz_correlacion.png",
        "descripcion": "Mapa de calor de las asociaciones entre variables territoriales y modalidades de violencia.",
        "lectura": "Se observan correlaciones moderadas a altas entre indicadores de calidad de vivienda, acceso a servicios básicos, nivel educativo y conectividad. La colinealidad entre estas variables sugiere que capturan dimensiones latentes comunes de vulnerabilidad territorial, lo que justifica el uso de técnicas de reducción de dimensionalidad."
    },
    "Varianza PCA": {
        "archivo": "varianza_explicada_acumulada.png",
        "descripcion": "Varianza explicada acumulada por componente principal.",
        "lectura": "Los primeros componentes concentran una proporción sustancial de la variabilidad del conjunto de datos. Esta estructura permite trabajar con una representación reducida sin sacrificar la mayor parte de la información, y constituye la base sobre la cual se aplica el clustering distrital."
    },
    "Métricas K-Means": {
        "archivo": "metricas_kmeans.png",
        "descripcion": "Criterios de selección del número óptimo de clústeres: método del codo, Silhouette y Davies-Bouldin.",
        "lectura": "La evaluación conjunta de los tres criterios orienta la selección de cinco clústeres como partición más adecuada. El coeficiente Silhouette indica una separación razonable entre grupos, mientras que Davies-Bouldin confirma una compacidad interna aceptable. La decisión no responde a un umbral arbitrario sino al balance entre estas métricas."
    },
    "Clustering PCA": {
        "archivo": "cluster_pca_3d.png",
        "descripcion": "Agrupamiento de distritos proyectado sobre los primeros tres componentes principales.",
        "lectura": "Los cinco grupos identificados muestran separación en el espacio reducido, lo que evidencia perfiles territoriales diferenciados. Cada clúster reúne distritos con características socioeconómicas, educativas y de condiciones del hogar similares, permitiendo una lectura comparativa de las distintas realidades distritales de Lima."
    },
    "Clustering NMF": {
        "archivo": "clustering_nmf_3d.png",
        "descripcion": "Agrupamiento de distritos sobre factores derivados de la Factorización Matricial No Negativa (NMF).",
        "lectura": "La representación NMF ofrece una perspectiva complementaria al PCA: al construir los factores como combinaciones aditivas de variables originales, los perfiles resultantes son más interpretables en términos sustantivos. La correspondencia entre ambas soluciones de clustering refuerza la robustez de los grupos identificados."
    },
    "Dendrograma Ward": {
        "archivo": "dendrograma_ward.png",
        "descripcion": "Dendrograma del clustering jerárquico aglomerativo con enlace de Ward.",
        "lectura": "La estructura jerárquica muestra cómo los distritos se fusionan progresivamente según similitud territorial. El corte que define cinco grupos es consistente con la solución K-Means, lo que valida la partición desde una perspectiva metodológica independiente y sin necesidad de especificar K de antemano."
    },
    "Pairplot opcional": {
        "archivo": "pairplot_variables_alta_correlacion.png",
        "descripcion": "Relaciones bivariadas entre variables con alta correlación entre sí.",
        "lectura": "La visualización en pares permite identificar patrones de dispersión no lineales y posibles valores atípicos entre las variables más correlacionadas. Complementa el análisis matricial al ofrecer una inspección visual directa de las distribuciones conjuntas."
    }
}

def image_path(filename: str) -> Path:
    return GRAFICOS_DIR / filename

def show_image_block(nombre: str, info: dict):
    path = image_path(info["archivo"])
    st.markdown(f'<div class="figure-title">{nombre}</div>', unsafe_allow_html=True)
    st.caption(info["descripcion"])
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.markdown(f"""
        <div class="warningbox">
        Imagen no encontrada: <b>{info['archivo']}</b><br>
        Ruta esperada: <code>graficos/{info['archivo']}</code>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight">
    {info['lectura']}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navegación")
modo = st.sidebar.radio(
    "Sección",
    [
        "Resumen del proyecto",
        "Exploración por figura",
        "Galería de resultados",
        "Narrativa analítica",
        "Lista de verificación"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Estado de archivos**")
for nombre, info in FIGURAS.items():
    status = "✅" if image_path(info["archivo"]).exists() else "⚠️"
    st.sidebar.write(f"{status} `{info['archivo']}`")

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
<h1>Vulnerabilidad Territorial y Violencia contra la Mujer en Lima Metropolitana</h1>
<p>Análisis distrital mediante minería de datos — Proyecto de investigación 2025</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Páginas
# -----------------------------
if modo == "Resumen del proyecto":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
        <h3>Objetivo</h3>
        <p>Examinar la relación entre vulnerabilidad territorial y violencia registrada contra la mujer a escala distrital en Lima Metropolitana.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
        <h3>Métodos</h3>
        <p>Tasa de violencia contra la mujer (TVM), índice de vulnerabilidad, análisis de correlación, PCA, NMF, K-Means y clustering jerárquico.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
        <h3>Hallazgo central</h3>
        <p>La relación entre vulnerabilidad estructural y denuncia registrada no es lineal: los distritos con mayor precariedad no siempre presentan tasas más altas.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Estructura del análisis")
    st.markdown("""
    El análisis parte del diagnóstico territorial mediante un mapa de distribución distrital,
    avanza hacia la exploración de la relación entre vulnerabilidad y TVM, y luego incorpora
    técnicas de reducción de dimensionalidad y clustering para identificar perfiles distritales diferenciados.
    La convergencia entre los métodos de agrupamiento —K-Means, NMF y Ward— refuerza la robustez de los resultados.
    """)

    st.markdown("### Vista de entrada")
    show_image_block("Mapa territorial", FIGURAS["Mapa territorial"])

elif modo == "Exploración por figura":
    st.markdown("## Exploración por figura")
    seleccion = st.selectbox("Seleccionar resultado", list(FIGURAS.keys()))
    show_image_block(seleccion, FIGURAS[seleccion])

elif modo == "Galería de resultados":
    st.markdown("## Galería de resultados")
    tabs = st.tabs(["Espacial", "Relación", "Correlación", "PCA", "Clustering", "Jerárquico"])

    with tabs[0]:
        show_image_block("Mapa territorial", FIGURAS["Mapa territorial"])
    with tabs[1]:
        show_image_block("Vulnerabilidad vs TVM", FIGURAS["Vulnerabilidad vs TVM"])
    with tabs[2]:
        show_image_block("Matriz de correlación", FIGURAS["Matriz de correlación"])
    with tabs[3]:
        show_image_block("Varianza PCA", FIGURAS["Varianza PCA"])
    with tabs[4]:
        show_image_block("Métricas K-Means", FIGURAS["Métricas K-Means"])
        st.divider()
        show_image_block("Clustering PCA", FIGURAS["Clustering PCA"])
        st.divider()
        show_image_block("Clustering NMF", FIGURAS["Clustering NMF"])
    with tabs[5]:
        show_image_block("Dendrograma Ward", FIGURAS["Dendrograma Ward"])

elif modo == "Narrativa analítica":
    st.markdown("## Narrativa analítica")
    st.markdown("""
    Esta vista presenta el proyecto como una secuencia analítica coherente,
    desde el diagnóstico territorial hasta la identificación de perfiles distritales.
    """)

    pasos = [
        ("El problema tiene una dimensión espacial", "Mapa territorial"),
        ("La vulnerabilidad no determina unívocamente la denuncia", "Vulnerabilidad vs TVM"),
        ("Las variables territoriales comparten estructura latente", "Matriz de correlación"),
        ("PCA reduce la complejidad sin perder información relevante", "Varianza PCA"),
        ("K-Means identifica cinco perfiles distritales diferenciados", "Clustering PCA"),
        ("El clustering jerárquico valida la partición de forma independiente", "Dendrograma Ward"),
    ]

    for titulo, key in pasos:
        st.markdown(f"### {titulo}")
        show_image_block(key, FIGURAS[key])
        st.divider()

elif modo == "Lista de verificación":
    st.markdown("## Lista de verificación")
    st.checkbox("La carpeta `graficos/` está al mismo nivel que `app.py`.")
    st.checkbox("Los nombres de los archivos de imagen coinciden exactamente con los esperados.")
    st.checkbox("Los resultados se presentan como patrones y asociaciones, sin afirmar causalidad.")
    st.checkbox("La baja TVM en distritos vulnerables se interpreta como posible barrera de denuncia, no como ausencia de violencia.")
    st.checkbox("El análisis cubre todas las etapas: diagnóstico, exploración, reducción dimensional y clustering.")

    st.markdown("---")
    st.markdown("""
    El dashboard traduce los resultados del análisis en una herramienta de lectura territorial:
    permite identificar dónde se concentra la violencia registrada, qué distritos comparten perfiles
    estructurales similares y dónde pueden operar mecanismos de subregistro vinculados a la vulnerabilidad.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Minería de Datos | Lima Metropolitana, 2025")