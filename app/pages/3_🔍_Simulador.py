import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador", layout="wide")

st.title("🔍 Simulador de Riesgo Clínico")
st.info("**Criterio Activo:** Clasificador focalizado operando con un umbral de decisión calibrado del **0.54**. Levantará alerta si el perfil supera este valor porcentual.")

if "modelos_listos" not in st.session_state:
    st.warning("⚠️ Inicia desde la página principal para cargar los modelos.")
    st.stop()

df = st.session_state.df
# Umbral calibrado real
UMBRAL = 0.54

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Perfil de la Madre")
    edad_m = st.selectbox("Grupo Etario (Madre)", sorted(df["GRUPO_ETARIO_MADRE"].astype(str).unique()), index=4)
    edu_m = st.selectbox("Nivel Educacional (Madre)", sorted(df["NIVEL_DESC"].astype(str).unique()), index=2)
    act_m = st.selectbox("Actividad (Madre)", sorted(df["ACTIV_MADRE"].astype(str).unique()))
    
with col2:
    st.markdown("#### Perfil del Padre")
    edad_p = st.selectbox("Grupo Etario (Padre)", sorted(df["GRUPO_ETARIO_PADRE"].astype(str).unique()), index=4)
    edu_p = st.selectbox("Nivel Educacional (Padre)", sorted(df["NIVEL_PADRE"].astype(str).unique()), index=2)
    act_p = st.selectbox("Actividad (Padre)", sorted(df["ACTIV_PADRE"].astype(str).unique()))

input_df = pd.DataFrame({
    "NIVEL_DESC": [edu_m], "NIVEL_PADRE": [edu_p], 
    "GRUPO_ETARIO_MADRE": [edad_m], "GRUPO_ETARIO_PADRE": [edad_p], 
    "ACTIV_MADRE": [act_m], "ACTIV_PADRE": [act_p]
})

prob = st.session_state.m_final.predict_proba(input_df)[0, 1]

st.divider()
c1, c2 = st.columns([1, 2])
c1.metric("Probabilidad Estimada del Caso", f"{prob:.1%}")

if prob >= UMBRAL:
    c2.error(f"⚠️ **RIESGO ALTO (Alerta Clínico-Social)**\nSupera el umbral crítico ({UMBRAL:.2f}). Se recomienda priorizar derivación a red de apoyo.")
else:
    c2.success(f"✅ **SIN ALERTA**\nDebajo del umbral de riesgo estricto ({UMBRAL:.2f}).")