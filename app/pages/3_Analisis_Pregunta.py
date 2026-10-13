import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis de la Pregunta", layout="wide")
st.title("Resolviendo la Hipótesis Socioeconómica")

# 1. Cargar el archivo procesado (con la columna BAJO_PESO lista)
df = pd.read_csv('data/processed/nacimientos_valpo_limpio.csv')

st.markdown("Como el tiempo de gestación resultó biológicamente estable, redirigimos la variable objetivo **(Y)** hacia el **Riesgo de Bajo Peso al Nacer (<2500g)**.")
st.markdown("---")

col1, col2 = st.columns(2)
orden_edu = ['Superior', 'Medio (Chilenas)', 'Secundario (Extranjeras)', 'Básico/Primario', 'Ninguno']

with col1:
    st.subheader("3. Bajo Peso vs. Educación")
    # Calculamos directamente el promedio de la columna de unos y ceros
    df_edu = df.groupby('NIVEL_DESC')['BAJO_PESO'].mean().reset_index()
    df_edu['BAJO_PESO'] = df_edu['BAJO_PESO'] * 100
    
    fig_edu = px.bar(df_edu, x='NIVEL_DESC', y='BAJO_PESO', text_auto='.2f',
                     category_orders={"NIVEL_DESC": orden_edu}, color='BAJO_PESO', color_continuous_scale='Reds')
    fig_edu.update_layout(yaxis_title="% de Bajo Peso", xaxis_title="")
    st.plotly_chart(fig_edu, use_container_width=True)

with col2:
    st.subheader("4. Bajo Peso vs. Estado Civil")
    df_civ = df.groupby('CIVIL_AGRUPADO')['BAJO_PESO'].mean().reset_index()
    df_civ['BAJO_PESO'] = df_civ['BAJO_PESO'] * 100
    
    fig_civ = px.bar(df_civ, x='CIVIL_AGRUPADO', y='BAJO_PESO', text_auto='.2f',
                     color='BAJO_PESO', color_continuous_scale='Oranges')
    fig_civ.update_layout(yaxis_title="% de Bajo Peso", xaxis_title="")
    st.plotly_chart(fig_civ, use_container_width=True)

st.markdown("---")
st.subheader("5. Evolución Temporal del Riesgo (Factor T)")
tendencia = df.groupby('ANO_NAC')['BAJO_PESO'].mean().reset_index()
tendencia['BAJO_PESO'] = tendencia['BAJO_PESO'] * 100

fig_line = px.line(tendencia, x='ANO_NAC', y='BAJO_PESO', markers=True, color_discrete_sequence=['#ff4b4b'])
fig_line.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
fig_line.update_layout(xaxis=dict(tickmode='linear', dtick=1), yaxis_range=[0, 10], 
                       xaxis_title="Año de Nacimiento", yaxis_title="Tasa de Bajo Peso (%)")
st.plotly_chart(fig_line, use_container_width=True)

with st.expander("📌 Conclusiones Finales y Refinamiento de la Pregunta"):
    st.warning("""
    **El verdadero rostro de la desigualdad:**
    1. **Impacto Educacional:** Existe una correlación directa. Las madres sin educación formal presentan casi un 11% de riesgo de bajo peso, prácticamente duplicando la tasa frente a madres universitarias.
    2. **El Estado Civil no influye:** Las madres casadas, solteras y convivientes presentan exactamente el mismo nivel de riesgo (~6.2%). Esto nos confirma que la amenaza neonatal es estrictamente socioeconómica (educación/recursos), no familiar. *(La categoría 'Otra' registra 0% debido a la escasez de registros de madres viudas/separadas).*
    3. **La Gravedad del Factor Temporal:** La tasa general de riesgo experimentó un alza sostenida e ininterrumpida entre 2020 y 2023 en Valparaíso.
    """)