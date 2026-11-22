import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="Criterio Clínico", layout="wide")

st.title("🧠 Criterio Clínico y Ajuste de Sensibilidad")
st.write("Mueve el selector para ajustar la exigencia del modelo. El rango refleja la ventana de probabilidad operativa real de este modelo sociodemográfico.")

if "modelos_listos" not in st.session_state:
    st.warning("⚠️ Vuelve a Inicio para cargar los datos.")
    st.stop()

# Slider ajustado al rango real del modelo (0.45 a 0.60)
umbral_elegido = st.slider(
    "Umbral de Alerta Clínica (Demostración)", 
    min_value=0.45, 
    max_value=0.60, 
    value=st.session_state.get("umbral", 0.54), 
    step=0.01, 
    key="umbral"
)

st.divider()
st.subheader("El Impacto Clínico de esta Decisión (Trade-off)")

m_final = st.session_state.m_final
X_test = st.session_state.X_test
y_test = st.session_state.y_test

probabilidades = m_final.predict_proba(X_test)[:, 1]
predicciones = (probabilidades >= umbral_elegido).astype(int)

tn, fp, fn, tp = confusion_matrix(y_test, predicciones).ravel()
total_reales_bajo_peso = fn + tp

col_met1, col_met2 = st.columns(2)

with col_met1:
    st.metric(label="Detección (Recall)", value=f"{(tp / total_reales_bajo_peso if total_reales_bajo_peso > 0 else 0):.1%}")
    st.error(f"**Falsos Negativos (Omitidos):** {fn} bebés en riesgo no detectados.")

with col_met2:
    st.metric(label="Certeza (Precision)", value=f"{(tp / (tp + fp) if (tp + fp) > 0 else 0):.1%}")
    st.warning(f"**Falsos Positivos (Sanos Alertados):** {fp} familias alertadas innecesariamente.")

st.divider()
st.info("💡 **Conclusión del Criterio:** Como el modelo carece de datos clínicos (ecografías, peso previo), su probabilidad máxima rara vez supera el 60%. Por ello, fijar un umbral mayor (ej. 0.65) 'apaga' el sistema (Recall 0%). Para garantizar la estabilidad y utilidad del sistema, las siguientes páginas operarán con un umbral calibrado fijo de **0.54**, buscando el equilibrio entre capturar el riesgo extremo y no saturar el sistema con alertas falsas.")