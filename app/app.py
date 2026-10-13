import streamlit as st

st.set_page_config(page_title="Inicio - Proyecto Nacimientos", layout="centered")

st.title("📊 Análisis de Condiciones de Nacimiento en Valparaíso")
st.subheader("Proyecto de Visualización de Datos - Avance 2")

st.markdown("---")

st.markdown("""
### 🎯 El Problema
La desigualdad socioeconómica impacta múltiples dimensiones de la vida, pero ¿comienza a afectar al ser humano incluso antes de nacer? 

### ❓ Pregunta de Investigación
**¿Cómo influye la vulnerabilidad socioeconómica y la red de apoyo de la madre en las condiciones de salud del recién nacido (peso y tiempo de gestación) en la Región de Valparaíso (2020-2023)?**

### 📂 Sobre los Datos
Utilizamos los registros abiertos del Departamento de Estadísticas e Información de Salud (DEIS). Tras un proceso de limpieza (Data Quality), analizamos más de 69.000 partos, enfocándonos en:
*   **Variables Predictoras (X):** Nivel Educacional y Estado Civil de la madre.
*   **Variables Objetivo (Y):** Semanas de Gestación y Riesgo de Bajo Peso al Nacer (< 2500g).

---
👈 **Usa el menú lateral para navegar por el Análisis Exploratorio (EDA).**
""")