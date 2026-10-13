import streamlit as st
import pandas as pd

st.set_page_config(page_title="Contexto y Datos", layout="wide")
st.title("Contexto y Calidad de los Datos")

# Leer el archivo limpio directamente
df = pd.read_csv('data/processed/nacimientos_valpo_limpio.csv')

st.markdown("### Limpieza y Preparación (Data Quality)")
st.write("- **Valores nulos ocultos:** Eliminamos los códigos '9' (Ignorado) en educación y estado civil.")
st.write("- **Descubrimiento de Metadatos:** Mantuvimos separada la categoría 'Secundario' al confirmar en el diccionario oficial que identifica exclusivamente a madres extranjeras.")
st.write("- **Nueva Variable Matemática (BAJO_PESO):** Transformamos los rangos de texto en una variable binaria (1 = Riesgo <2500g, 0 = Sano) para calcular porcentajes exactos.")
st.write("- **Filtros:** Solo Región de Valparaíso, años 2020 a 2023, y embarazos viables (20-45 semanas).")

col1, col2 = st.columns(2)
col1.metric("Registros Originales", "735.000")
col2.metric("Muestra Limpia Valparaíso", f"{len(df):,}")

st.markdown("### Vista del Dataset Procesado")
# Aquí agregamos BAJO_PESO a la lista de columnas que se muestran en pantalla
st.dataframe(df[['ANO_NAC', 'SEMANAS', 'RANGO_PESO', 'BAJO_PESO', 'NIVEL_DESC', 'CIVIL_AGRUPADO']].head())