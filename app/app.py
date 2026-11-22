import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Alerta Neonatal", layout="wide")

st.title("👶 Sistema de Alerta Temprana")
st.subheader("Clasificador Focalizado - Bajo Peso al Nacer")

st.info("🎯 **Objetivo:** Detectar perfiles sociodemográficos de alto riesgo mediante un filtro estricto.")

@st.cache_resource
def entrenar_modelos():
    try:
        df = pd.read_csv("data/nacimientos_valpo_avance3_limpio.csv", low_memory=False)
    except:
        df = pd.DataFrame({
            "NIVEL_DESC": ["Básico/Primario", "Superior", "Ninguno"] * 50,
            "NIVEL_PADRE": ["Básico/Primario", "Superior", "Ninguno"] * 50,
            "GRUPO_ETARIO_MADRE": ["40 A 44 AÑOS", "25 A 29 AÑOS", "15 A 19 AÑOS"] * 50,
            "GRUPO_ETARIO_PADRE": ["45 A 49 AÑOS", "25 A 29 AÑOS", "20 A 24 AÑOS"] * 50,
            "ACTIV_MADRE": ["Inactivo", "Activo", "Inactivo"] * 50,
            "ACTIV_PADRE": ["Inactivo", "Activo", "Inactivo"] * 50,
            "BAJO_PESO": [1, 0, 1] * 50
        })
    
    PREDICTORES = ["NIVEL_DESC", "NIVEL_PADRE", "GRUPO_ETARIO_MADRE", "GRUPO_ETARIO_PADRE", "ACTIV_MADRE", "ACTIV_PADRE"]
    X = df[PREDICTORES].astype(str)
    y = df["BAJO_PESO"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    prep = ColumnTransformer([("cat", Pipeline([("imputar", SimpleImputer(strategy="constant", fill_value="No informado")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), PREDICTORES)])
    modelo_final = Pipeline([("preparar", prep), ("clasificador", LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000))])
    modelo_final.fit(X_train, y_train)
    
    prep_base = ColumnTransformer([("cat", Pipeline([("imputar", SimpleImputer(strategy="constant", fill_value="No informado")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), ["NIVEL_DESC"])])
    modelo_base = Pipeline([("preparar", prep_base), ("clasificador", LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000))])
    modelo_base.fit(X_train, y_train)

    return modelo_base, modelo_final, X_test, y_test, df

if "modelos_listos" not in st.session_state:
    st.session_state.m_base, st.session_state.m_final, st.session_state.X_test, st.session_state.y_test, st.session_state.df = entrenar_modelos()
    st.session_state.modelos_listos = True

st.write("👈 Navega por el menú lateral para ajustar el umbral, evaluar el modelo y simular perfiles.")
