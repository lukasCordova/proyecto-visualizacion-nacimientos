import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, average_precision_score

st.set_page_config(page_title="Rendimiento", layout="wide")

st.title("📊 Evaluación de Rendimiento")
st.subheader("Clasificador Focalizado (Umbral Calibrado: 0.54)")

st.write("La clase de interés (positiva) es **BAJO_PESO = 1**. Las métricas reflejan el rendimiento del modelo aplicando el umbral óptimo del 54% (0.54), calibrado según los límites predictivos de los datos sociodemográficos.")
st.divider()

if "modelos_listos" not in st.session_state:
    st.warning("⚠️ Inicia desde la página principal para cargar los datos.")
    st.stop()

# Umbral calibrado real
UMBRAL = 0.54

def calc(modelo, X, y, umbral):
    prob = modelo.predict_proba(X)[:, 1]
    pred = (prob >= umbral).astype(int)
    return {
        "Detección (Recall)": f"{recall_score(y, pred, zero_division=0):.1%}",
        "Certeza (Precision)": f"{precision_score(y, pred, zero_division=0):.1%}",
        "ROC-AUC": f"{roc_auc_score(y, prob):.3f}",
        "AP (Precision-Recall)": f"{average_precision_score(y, prob):.3f}"
    }

df_comp = pd.DataFrame([
    calc(st.session_state.m_base, st.session_state.X_test, st.session_state.y_test, UMBRAL),
    calc(st.session_state.m_final, st.session_state.X_test, st.session_state.y_test, UMBRAL)
], index=["Baseline (Logística 1 variable)", "Modelo Final (Logística 6 variables)"])

st.table(df_comp)
st.info("💡 **Conclusión:** El modelo multivariable supera al baseline simple. Al integrar todo el núcleo familiar, mejora la discriminación global del riesgo (mayor ROC-AUC y AP). Aunque la detección (Recall) y Certeza (Precision) son modestas, esto es coherente con un modelo de *triage* poblacional basado exclusivamente en factores sociales, sin apoyo clínico.")