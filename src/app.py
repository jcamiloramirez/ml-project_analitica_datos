import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import scipy.stats as stats
from sklearn.feature_selection import mutual_info_regression

# Configuracion de pagina con estetica minimalista
st.set_page_config(
    page_title="Analitica de Datos - Universidad de Antioquia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyeccion de CSS para estilo Github Capsule (Sin bordes en titulos)
st.markdown("""
    <style>
        .main {
            background-color: #f6f8fa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        /* Estilo de capsula para contenedores */
        .github-capsule {
            background-color: #ffffff;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 0 rgba(27,31,35,0.04);
        }
        /* Ajuste de titulos - Eliminacion de lineas blancas */
        h1, h2, h3 {
            color: #1f2328;
            border-bottom: none !important;
            padding-bottom: 0px !important;
            margin-bottom: 16px !important;
        }
        /* Tablas y DataFrame */
        .stDataFrame, .stTable {
            border-radius: 6px;
        }
        hr {
            border: 0;
            border-top: 1px solid #d0d7de;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Gestion de Base de Datos
DB_PATH = os.path.join("database", "analitica_data.db")

def load_data(table_name):
    if not os.path.exists(DB_PATH):
        st.error(f"Error: No se encontro el archivo en {DB_PATH}")
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error al conectar con la tabla {table_name}: {e}")
        return None

# Navegacion Lateral
st.sidebar.title("Laboratorio 3")
st.sidebar.markdown("Analisis Integral de Datos")

base_datos = st.sidebar.selectbox(
    "Dataset Seleccionado",
    ["Vivienda (housing)", "Credito (credit)"]
)

tabla_activa = "housing" if "housing" in base_datos else "credit"
df = load_data(tabla_activa)

if df is not None:
    menu = st.sidebar.radio(
        "Secciones del Proyecto",
        ["Dashboard Descriptivo", "Visualizacion EDA", "Tratamiento de Nulos", "Pruebas de Dependencia"]
    )

    # --- SECCION 1: ESTADISTICAS DESCRIPTIVAS ---
    if menu == "Dashboard Descriptivo":
        st.header("Estadisticas Descriptivas")
        
        # Tabla de Metadatos (Reemplazo de df.info)
        st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
        st.subheader("Informacion General del Dataset (Metadatos)")
        
        info_df = pd.DataFrame({
            "Columna": df.columns,
            "Tipo de Dato": df.dtypes.values,
            "Valores Presentes": df.count().values,
            "Valores Nulos": df.isnull().sum().values,
            "Memoria (bytes)": [df[col].memory_usage(index=False, deep=True) for col in df.columns]
        })
        st.table(info_df)
        st.markdown('</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Primeras 10 Observaciones")
            st.dataframe(df.head(10), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_b:
            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Resumen Estadistico de Variables")
            st.write(df.describe())
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SECCION 2: VISUALIZACION EDA ---
    elif menu == "Visualizacion EDA":
        st.header("Analisis Exploratorio de Datos")

        if tabla_activa == "housing":
            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Distribuciones y Medidas de Tendencia Central")
            cols_dist = ["price", "sqft_living", "grade", "bathrooms"]
            fig_dist, axes_dist = plt.subplots(2, 2, figsize=(16, 12))
            axes_dist = axes_dist.flatten()

            for i, col in enumerate(cols_dist):
                sns.histplot(df[col], bins=50 if col != "grade" else 13, kde=True if col != "grade" else False, ax=axes_dist[i])
                axes_dist[i].axvline(df[col].mean(), color="red", linestyle="--", label=f"Media")
                axes_dist[i].axvline(df[col].median(), color="green", linestyle="-", label=f"Mediana")
                axes_dist[i].set_title(f"Distribucion de {col}")
                axes_dist[i].legend()
            
            plt.tight_layout()
            st.pyplot(fig_dist)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Identificacion de Valores Atipicos")
            fig_box, axes_box = plt.subplots(2, 2, figsize=(14, 8))
            sns.boxplot(x=df["price"], ax=axes_box[0, 0]).set_title("Precio")
            sns.boxplot(x=df["sqft_living"], ax=axes_box[0, 1]).set_title("Area habitable")
            sns.boxplot(x=df["bathrooms"], ax=axes_box[1, 0]).set_title("Banos")
            sns.boxplot(x=df["bedrooms"], ax=axes_box[1, 1]).set_title("Habitaciones")
            plt.tight_layout()
            st.pyplot(fig_box)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Matriz de Correlacion Lineal (Pearson)")
            cols_corr = ["price", "sqft_living", "grade", "bathrooms", "bedrooms", "sqft_lot", "floors", "view", "condition", "lat", "long"]
            fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
            sns.heatmap(df[cols_corr].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax_corr)
            st.pyplot(fig_corr)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Exploracion de Relaciones Multivariadas")
            fig_grid, axes_g = plt.subplots(3, 3, figsize=(20, 18))
            sns.scatterplot(data=df, x="sqft_living", y="price", alpha=0.3, color="#2E86C1", ax=axes_g[0, 0]).set_title("Precio vs Area")
            sns.boxplot(data=df, x="grade", y="price", palette="viridis", showfliers=False, ax=axes_g[0, 1]).set_title("Precio vs Calidad")
            sns.scatterplot(data=df, x="sqft_above", y="price", alpha=0.3, color="#28B463", ax=axes_g[0, 2]).set_title("Precio vs Area Suelo")
            sns.scatterplot(data=df, x="sqft_living15", y="price", alpha=0.3, color="#884EA0", ax=axes_g[1, 0]).set_title("Precio vs Vecinos")
            sns.scatterplot(data=df, x="bathrooms", y="price", alpha=0.3, color="#D35400", ax=axes_g[1, 1]).set_title("Precio vs Banos")
            sns.boxplot(data=df, x="bedrooms", y="price", palette="Set2", showfliers=False, ax=axes_g[1, 2]).set_title("Precio vs Habitaciones")
            sns.boxplot(data=df, x="view", y="price", palette="magma", showfliers=False, ax=axes_g[2, 0]).set_title("Precio vs Vista")
            sns.boxplot(data=df, x="waterfront", y="price", palette="coolwarm", showfliers=False, ax=axes_g[2, 1]).set_title("Precio vs Frente Agua")
            sns.boxplot(data=df, x="condition", y="price", palette="YlOrBr", showfliers=False, ax=axes_g[2, 2]).set_title("Precio vs Condicion")
            plt.tight_layout()
            st.pyplot(fig_grid)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
            st.subheader("Analisis Geografico y Temporal")
            df_neighborhood = df.groupby('zipcode')['price'].median().reset_index()
            repo_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/wa_washington_zip_codes_geo.min.json'
            fig_map = px.choropleth_map(
                df_neighborhood, geojson=repo_url, locations='zipcode',
                featureidkey='properties.ZCTA5CE10', color='price',
                color_continuous_scale="Viridis", range_color=(300000, 1000000),
                map_style="carto-positron", zoom=9, center={"lat": 47.5, "lon": -122.1}, opacity=0.5
            )
            fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

            df_temp = df.copy()
            df_temp['decade_built'] = (df_temp['yr_built'] // 10) * 10
            df_temp['is_renovated'] = df_temp['yr_renovated'].apply(lambda x: 'Renovada' if x > 0 else 'Original')
            fig_time, ax_time = plt.subplots(figsize=(14, 7))
            sns.lineplot(data=df_temp, x='decade_built', y='price', hue='is_renovated', estimator=np.median, marker='o', palette={'Original': '#E74C3C', 'Renovada': '#2ECC71'}, ax=ax_time)
            ax_time.set_title("Evolucion de Precios por Decada de Construccion")
            st.pyplot(fig_time)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SECCION 3: TRATAMIENTO DE NULOS ---
    elif menu == "Tratamiento de Nulos":
        st.header("Validacion de Metodos de Imputacion")
        
        st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
        st.subheader("Benchmark: Error Medio Absoluto (MAE)")
        results_imp = {
            "Escenario": ["1% de Nulos", "5% de Nulos", "10% de Nulos"],
            "Nulos Simulados": [20, 100, 200],
            "MAE - Mediana": [783.8, 790.0, 770.2],
            "MAE - KNN": [393.7, 533.9, 486.2],
            "MAE - Iterative": [350.5, 370.3, 351.7]
        }
        st.table(pd.DataFrame(results_imp).set_index("Escenario"))
        st.markdown("**Analisis:** El metodo Iterative Imputer minimiza sistematicamente el error en la reconstruccion de la variable sqft_living.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SECCION 4: PRUEBAS DE DEPENDENCIA ---
    elif menu == "Pruebas de Dependencia":
        st.header("Pruebas de Asociacion y Dependencia")

        st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.subheader("Dependencia Numerica (Area vs Precio)")
            p_r, p_p = stats.pearsonr(df['sqft_living'], df['price'])
            s_r, s_p = stats.spearmanr(df['sqft_living'], df['price'])
            res_num = pd.DataFrame({
                "Prueba": ["Pearson r", "Spearman rho"],
                "Coeficiente": [p_r, s_r],
                "p-value": [p_p, s_p]
            })
            st.table(res_num)

        with col_r2:
            st.subheader("Dependencia Mixta (Precio vs Grade)")
            grupos = [g['price'].values for _, g in df.groupby('grade')]
            h, p_k = stats.kruskal(*grupos)
            st.write(f"Estadistico H: **{h:.2f}**")
            st.write(f"p-value: **{p_k:.2e}**")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="github-capsule">', unsafe_allow_html=True)
        col_r3, col_r4 = st.columns(2)
        with col_r3:
            st.subheader("Asociacion Categorial (Chi-Cuadrado)")
            tab = pd.crosstab(df['waterfront'], df['view'])
            chi, p_c, _, _ = stats.chi2_contingency(tab)
            st.write(f"Estadistico Chi2: **{chi:.2f}**")
            st.write(f"p-value: **{p_c:.2e}**")

        with col_r4:
            st.subheader("Aporte Informativo (Mutual Information)")
            X_s = df[['sqft_living', 'bathrooms', 'grade', 'view', 'lat', 'long']]
            mi = mutual_info_regression(X_s, df['price'], random_state=42)
            st.bar_chart(pd.Series(mi, index=X_s.columns).sort_values(ascending=False))
        st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.text("Juan Camilo Ramirez Diaz")
st.sidebar.text("Matematicas - UdeA")