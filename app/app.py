import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, average_precision_score

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Alerta de Riesgo Neonatal", layout="wide")
st.title("👶 Sistema de Alerta Temprana: Bajo Peso al Nacer")
st.markdown("Herramienta de triage sociodemográfico para la Región de Valparaíso (2020-2023).")

# 2. MOTOR DE DATOS Y MODELADO (Caché para que no se recargue en cada clic)
@st.cache_resource
def preparar_modelos():
    # Cargar datos
    df = pd.read_csv("data/nacimientos_valpo_avance3_limpio.csv", low_memory=False)
    
    # Definir variables
    PREDICTORES = ["NIVEL_DESC", "NIVEL_PADRE", "GRUPO_ETARIO_MADRE", "GRUPO_ETARIO_PADRE", "ACTIV_MADRE", "ACTIV_PADRE"]
    OBJETIVO = "BAJO_PESO"
    
    # Asegurar tipos
    df[PREDICTORES] = df[PREDICTORES].astype(str)
    df[OBJETIVO] = pd.to_numeric(df[OBJETIVO], errors="coerce").fillna(0).astype(int)
    
    # Partición exacta del Avance 3 (Test reservado del 20%)
    X = df[PREDICTORES]
    y = df[OBJETIVO]
    X_desarrollo, X_test, y_desarrollo, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # --- MODELO BASELINE (Solo Educación de la Madre) ---
    prep_base = ColumnTransformer([
        ("cat", Pipeline([
            ("imputar", SimpleImputer(strategy="constant", fill_value="No informado")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]), ["NIVEL_DESC"])
    ])
    modelo_base = Pipeline([
        ("preparar", prep_base),
        ("clasificador", LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000))
    ])
    modelo_base.fit(X_desarrollo, y_desarrollo)
    
    # --- MODELO FINAL (6 Variables) ---
    prep_final = ColumnTransformer([
        ("cat", Pipeline([
            ("imputar", SimpleImputer(strategy="constant", fill_value="No informado")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]), PREDICTORES)
    ])
    modelo_final = Pipeline([
        ("preparar", prep_final),
        ("clasificador", LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000))
    ])
    modelo_final.fit(X_desarrollo, y_desarrollo)
    
    return modelo_base, modelo_final, X_test, y_test, df

# Ejecutar carga y entrenamiento
modelo_base, modelo_final, X_test, y_test, df_original = preparar_modelos()

# 3. INTERFAZ DE USUARIO CON PESTAÑAS
tab1, tab2 = st.tabs(["📊 Comparación de Rendimiento", "🔍 Clasificador Focalizado (Simulador)"])

# ==========================================
# PESTAÑA 1: MÉTRICAS (Rúbrica Sección A)
# ==========================================
with tab1:
    st.subheader("Evaluación de Modelos frente a Solución Base")
    st.write("La clase de interés (positiva) es **BAJO_PESO = 1**. Evaluado sobre el conjunto de prueba (20% reservado).")
    
    def calcular_metricas(modelo, X_eval, y_eval):
        probabilidades = modelo.predict_proba(X_eval)[:, 1]
        predicciones = (probabilidades >= 0.50).astype(int)
        return {
            "Accuracy": f"{accuracy_score(y_eval, predicciones):.1%}",
            "Precision": f"{precision_score(y_eval, predicciones, zero_division=0):.2%}",
            "Recall": f"{recall_score(y_eval, predicciones, zero_division=0):.1%}",
            "ROC-AUC": f"{roc_auc_score(y_eval, probabilidades):.3f}",
            "AP (Precision-Recall)": f"{average_precision_score(y_eval, probabilidades):.3f}"
        }

    metricas_base = calcular_metricas(modelo_base, X_test, y_test)
    metricas_final = calcular_metricas(modelo_final, X_test, y_test)
    
    tabla_comparativa = pd.DataFrame([metricas_base, metricas_final], 
                                     index=["Baseline (Solo Educación Madre)", "Modelo Final (6 Factores)"])
    
    st.table(tabla_comparativa)
    st.info("💡 **Conclusión de Valor:** El modelo multivariable supera al baseline simple. Al integrar la información del núcleo familiar completo (incluyendo al padre y edades), el modelo aumenta la capacidad de detectar casos reales (Recall) y discriminar el riesgo global (ROC-AUC y AP), justificando la adición de complejidad frente a una solución de un solo factor.")

# ==========================================
# PESTAÑA 2: DEMOSTRACIÓN (Rúbrica Sección B)
# ==========================================
with tab2:
    st.subheader("Simulador de Casos Específicos")
    st.write("Modifique los controles para observar cómo la combinación de factores altera la probabilidad de riesgo neonatal.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Perfil de la Madre")
        edad_m = st.selectbox("Grupo Etario (Madre)", sorted(df_original["GRUPO_ETARIO_MADRE"].dropna().unique()), index=4)
        edu_m = st.selectbox("Nivel Educacional (Madre)", sorted(df_original["NIVEL_DESC"].dropna().unique()), index=2)
        act_m = st.selectbox("Actividad (Madre)", sorted(df_original["ACTIV_MADRE"].dropna().unique()))
        
    with col2:
        st.markdown("#### Perfil del Padre")
        edad_p = st.selectbox("Grupo Etario (Padre)", sorted(df_original["GRUPO_ETARIO_PADRE"].dropna().unique()), index=4)
        edu_p = st.selectbox("Nivel Educacional (Padre)", sorted(df_original["NIVEL_PADRE"].dropna().unique()), index=2)
        act_p = st.selectbox("Actividad (Padre)", sorted(df_original["ACTIV_PADRE"].dropna().unique()))

    # Crear DataFrame con el input en vivo
    input_usuario = pd.DataFrame({
        "NIVEL_DESC": [edu_m],
        "NIVEL_PADRE": [edu_p],
        "GRUPO_ETARIO_MADRE": [edad_m],
        "GRUPO_ETARIO_PADRE": [edad_p],
        "ACTIV_MADRE": [act_m],
        "ACTIV_PADRE": [act_p]
    })
    
    st.divider()
    
    # PREDICCIÓN EN VIVO
    probabilidad_riesgo = modelo_final.predict_proba(input_usuario)[0, 1]
    clase_predicha = 1 if probabilidad_riesgo >= 0.50 else 0
    
    col_res1, col_res2, col_res3 = st.columns([1, 1, 2])
    
    with col_res1:
        st.metric(label="Clase Predicha", value="Riesgo Alto (1)" if clase_predicha == 1 else "Riesgo Base (0)")
    with col_res2:
        st.metric(label="Probabilidad Estimada", value=f"{probabilidad_riesgo:.1%}")
        
    with col_res3:
        if clase_predicha == 1:
            st.error(f"⚠️ **Alerta:** La combinación de estos factores sociodemográficos eleva la probabilidad a un **{probabilidad_riesgo:.1%}** (muy superior al 7.3% habitual de la población). Este es un perfil donde el modelo actúa como clasificador focalizado para priorizar apoyo social o derivación clínica temprana.")
        else:
            st.success(f"✅ **Sin alerta:** Con un **{probabilidad_riesgo:.1%}**, este perfil se mantiene bajo el umbral crítico (50%).")
            
    st.markdown("---")
    st.caption("🚨 **Limitación de Uso:** Esta herramienta se basa exclusivamente en 6 variables sociodemográficas (sin datos clínicos ni biométricos). Su objetivo es el triage poblacional en salud pública, no el diagnóstico médico clínico autónomo. Posee una tasa considerable de Falsos Positivos derivada del desbalance poblacional natural.")
