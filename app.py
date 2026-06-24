# app.py
# Dashboard de presentación: Vulnerabilidad territorial y violencia contra la mujer en Lima Metropolitana, 2025
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
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.2rem 1.4rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #3b0a45 0%, #6d2a7a 55%, #9b4bb3 100%);
    color: white;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: 2rem;
    margin-bottom: 0.2rem;
}
.hero p {
    font-size: 1rem;
    opacity: 0.93;
}
.card {
    padding: 1rem;
    border-radius: 18px;
    border: 1px solid #e8e8e8;
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    min-height: 122px;
}
.card h3 {
    font-size: 1rem;
    margin-bottom: 0.4rem;
}
.card p {
    font-size: 0.92rem;
    color: #4b4b4b;
}
.insight {
    padding: 0.9rem 1rem;
    border-left: 6px solid #6d2a7a;
    background: #faf4fd;
    border-radius: 12px;
    margin-top: 0.7rem;
}
.warningbox {
    padding: 0.9rem 1rem;
    border-left: 6px solid #e67e22;
    background: #fff7ed;
    border-radius: 12px;
}
.small {
    font-size: 0.86rem;
    color: #666;
}
.figure-title {
    font-weight: 700;
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Configuración de imágenes
# -----------------------------
GRAFICOS_DIR = Path("notebooks")

FIGURAS = {
    "Mapa territorial": {
        "archivo": "mapa_violencia_lima.png",
        "descripcion": "Distribución distrital de la TVM y principales modalidades de violencia.",
        "lectura": "La violencia registrada no se distribuye de manera homogénea en Lima Metropolitana. La violencia física y psicológica presentan mayor presencia territorial, mientras que la violencia sexual aparece más focalizada.",
        "uso": "Úsalo para abrir la exposición y demostrar que el problema tiene una dimensión territorial."
    },
    "Vulnerabilidad vs TVM": {
        "archivo": "correlacion_vulnerabilidad_tvm.png",
        "descripcion": "Relación entre índice de vulnerabilidad territorial y TVM.",
        "lectura": "Los distritos aparecen dispersos y no muestran una tendencia lineal positiva clara. Esto indica que una mayor vulnerabilidad territorial no siempre coincide con una mayor tasa de denuncias registradas.",
        "uso": "Úsalo para explicar el hallazgo central: la relación entre vulnerabilidad y denuncia registrada es compleja."
    },
    "Matriz de correlación": {
        "archivo": "matriz_correlacion.png",
        "descripcion": "Asociaciones entre variables territoriales y modalidades de violencia.",
        "lectura": "Se observan asociaciones entre indicadores de vivienda, servicios básicos, educación y conectividad. Varias variables capturan dimensiones similares de vulnerabilidad territorial.",
        "uso": "Úsalo para justificar PCA y NMF, ya que ayudan a resumir información correlacionada."
    },
    "Varianza PCA": {
        "archivo": "varianza_explicada_acumulada.png",
        "descripcion": "Varianza explicada acumulada por componentes principales.",
        "lectura": "Los primeros componentes concentran una proporción relevante de la variabilidad de la base, permitiendo reducir la dimensionalidad sin perder gran parte de la información.",
        "uso": "Úsalo para explicar por qué los componentes PCA sirven como base para clustering."
    },
    "Métricas K-Means": {
        "archivo": "metricas_kmeans.png",
        "descripcion": "Método del codo, Silhouette y Davies-Bouldin para seleccionar K.",
        "lectura": "Las métricas permiten evaluar distintos valores de K y respaldan la selección de una partición de cinco clústeres para el análisis distrital.",
        "uso": "Úsalo para demostrar que el número de clústeres no fue elegido al azar."
    },
    "Clustering PCA": {
        "archivo": "cluster_pca_3d.png",
        "descripcion": "Agrupamiento de distritos sobre componentes PCA.",
        "lectura": "Se identifican grupos diferenciados de distritos según dimensiones de vulnerabilidad socioeconómica, educación, condiciones del hogar y conectividad.",
        "uso": "Úsalo para presentar los perfiles territoriales diferenciados."
    },
    "Clustering NMF": {
        "archivo": "clustering_nmf_3d.png",
        "descripcion": "Agrupamiento de distritos sobre componentes NMF.",
        "lectura": "La representación NMF complementa el PCA al construir perfiles a partir de combinaciones aditivas de variables territoriales.",
        "uso": "Úsalo si deseas reforzar la interpretación de perfiles territoriales."
    },
    "Dendrograma Ward": {
        "archivo": "dendrograma_ward.png",
        "descripcion": "Clustering jerárquico aglomerativo con método de Ward.",
        "lectura": "El dendrograma muestra cómo los distritos se agrupan progresivamente según similitud territorial y permite contrastar la estructura encontrada con K-Means.",
        "uso": "Úsalo para cerrar la parte de agrupamiento con una técnica complementaria."
    },
    "Pairplot opcional": {
        "archivo": "pairplot_variables_alta_correlacion.png",
        "descripcion": "Relaciones bivariadas entre variables con alta correlación.",
        "lectura": "Permite observar patrones visuales entre variables relacionadas, aunque puede ocupar mucho espacio para el paper.",
        "uso": "Úsalo solo en el dashboard, no necesariamente en el documento final."
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
        No se encontró la imagen <b>{info['archivo']}</b> dentro de la carpeta <b>GRAFICOS</b>.<br>
        Coloca el archivo en: <code>GRAFICOS/{info['archivo']}</code>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight">
    <b>Lectura del gráfico:</b> {info['lectura']}<br><br>
    <b>Cómo presentarlo:</b> {info['uso']}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📌 Panel")
modo = st.sidebar.radio(
    "Elige una vista",
    [
        "Inicio ejecutivo",
        "Modo exposición",
        "Galería de gráficos",
        "Storytelling del análisis",
        "Checklist para presentar"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Archivos esperados")
for nombre, info in FIGURAS.items():
    status = "✅" if image_path(info["archivo"]).exists() else "⚠️"
    st.sidebar.write(f"{status} `{info['archivo']}`")

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
<h1>Observatorio de Vulnerabilidad Silenciosa - Lima 2025</h1>
<p>Dashboard de presentación para explicar la relación entre vulnerabilidad territorial y violencia contra la mujer usando minería de datos.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Páginas
# -----------------------------
if modo == "Inicio ejecutivo":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
        <h3>🎯 Objetivo</h3>
        <p>Analizar la relación entre vulnerabilidad territorial y violencia registrada contra la mujer a nivel distrital.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
        <h3>🧠 Técnicas</h3>
        <p>TVM, índice de vulnerabilidad, correlación, PCA, NMF, K-Means y clustering jerárquico.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
        <h3>💡 Hallazgo clave</h3>
        <p>La relación entre vulnerabilidad territorial y denuncia registrada no es lineal ni homogénea entre distritos.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Ruta de lectura del dashboard")
    st.markdown("""
    1. Primero se muestra el **mapa** para ubicar el problema territorialmente.  
    2. Luego se analiza la relación entre **vulnerabilidad y TVM**.  
    3. Después se justifica la reducción de dimensionalidad con **correlación y PCA**.  
    4. Finalmente se presentan **clústeres**, NMF y dendrograma para evidenciar perfiles distritales diferenciados.
    """)

    st.markdown("### Gráfico recomendado para iniciar")
    show_image_block("Mapa territorial", FIGURAS["Mapa territorial"])

elif modo == "Modo exposición":
    st.markdown("## Modo exposición")
    st.markdown("Selecciona el gráfico y tendrás una lectura breve para decirlo en clase.")
    seleccion = st.selectbox("Gráfico a presentar", list(FIGURAS.keys()))
    show_image_block(seleccion, FIGURAS[seleccion])

    st.markdown("### Guion corto")
    st.markdown(f"""
    **Este gráfico muestra:** {FIGURAS[seleccion]['descripcion']}  
    **La lectura principal es:** {FIGURAS[seleccion]['lectura']}  
    **La idea para la profe:** {FIGURAS[seleccion]['uso']}
    """)

elif modo == "Galería de gráficos":
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

elif modo == "Storytelling del análisis":
    st.markdown("## Storytelling del análisis")
    st.markdown("""
    Esta vista presenta el proyecto como una historia analítica, ideal para exponer en 3 a 5 minutos.
    """)

    pasos = [
        ("1. El problema no es uniforme", "Mapa territorial"),
        ("2. La vulnerabilidad no explica todo por sí sola", "Vulnerabilidad vs TVM"),
        ("3. Las variables territoriales están conectadas", "Matriz de correlación"),
        ("4. Se resume la complejidad con PCA", "Varianza PCA"),
        ("5. Se forman perfiles distritales", "Clustering PCA"),
        ("6. Se valida con una mirada jerárquica", "Dendrograma Ward"),
    ]

    for titulo, key in pasos:
        st.markdown(f"### {titulo}")
        show_image_block(key, FIGURAS[key])
        st.divider()

elif modo == "Checklist para presentar":
    st.markdown("## Checklist final")
    st.checkbox("Tengo la carpeta GRAFICOS al mismo nivel que app.py.")
    st.checkbox("Los nombres de las imágenes coinciden exactamente con los esperados.")
    st.checkbox("Puedo explicar en una frase qué muestra cada gráfico.")
    st.checkbox("No digo que el modelo prueba causalidad; solo patrones y asociaciones.")
    st.checkbox("Menciono que la baja TVM en distritos vulnerables puede sugerir barreras de denuncia, pero lo dejo como interpretación.")
    st.checkbox("Cierro con el valor del dashboard: orientar análisis territorial y focalización pública.")

    st.markdown("### Frase de cierre sugerida")
    st.markdown("""
    > El valor del dashboard es convertir los resultados del paper en una herramienta visual de decisión:
    permite observar dónde se concentra la violencia registrada, qué distritos comparten perfiles territoriales
    y dónde podrían existir señales de vulnerabilidad silenciosa.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Proyecto de Data Mining | Lima Metropolitana 2025")
