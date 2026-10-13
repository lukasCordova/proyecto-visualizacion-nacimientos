import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Univariado", layout="wide")
st.title("Análisis Exploratorio Univariado")

# 1. Cargar el archivo procesado (ya viene limpio desde tu script)
df = pd.read_csv('data/processed/nacimientos_valpo_limpio.csv')

# Filtro interactivo para el profesor
anio_seleccionado = st.selectbox("Filtre los datos por Año de Nacimiento:", ["Todos", 2020, 2021, 2022, 2023])
if anio_seleccionado != "Todos":
    df = df[df['ANO_NAC'] == int(anio_seleccionado)]

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Distribución General de Semanas")
    fig_hist = px.histogram(df, x="SEMANAS", nbins=15, color_discrete_sequence=['#4C78A8'], marginal="violin")
    fig_hist.update_layout(xaxis_title="Semanas de Gestación", yaxis_title="Cantidad de Partos")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("2. Semanas según Nivel Educacional")
    orden_edu = ['Superior', 'Medio (Chilenas)', 'Secundario (Extranjeras)', 'Básico/Primario', 'Ninguno']
    fig_box = px.box(df, x="NIVEL_DESC", y="SEMANAS", color="NIVEL_DESC", category_orders={"NIVEL_DESC": orden_edu})
    fig_box.update_layout(xaxis_title="", yaxis_title="Semanas", showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

with st.expander("📌 Ver Interpretación de los Hallazgos"):
    st.write("""
    **La biología frente a la desigualdad:** 
    La distribución general demuestra que la biología actúa como un estabilizador. La inmensa mayoría de los partos ocurren de forma normativa entre las semanas 38 y 39, independiente del estrato educativo de la madre. 
    *Nota:* La categoría 'Secundario (Extranjeras)' presenta nula dispersión debido a que es una muestra estadísticamente pequeña en los registros de la región, ya que la mayoría de los estudios migrantes se homologan a nivel Medio o Superior.
    """)