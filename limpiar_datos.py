import pandas as pd

print("1. Cargando el dataset crudo...")
df = pd.read_csv('data/raw/Serie_Nacimientos_2020_2023.csv', sep=';', low_memory=False)

print("2. Filtrando alcance geográfico...")
# Filtramos solo la Región de Valparaíso (el año no es necesario filtrarlo porque el dataset ya es 2020-2023)
df_valpo = df[df['GLOSA_REGION_RESIDENCIA'].str.contains('De Valparaíso', na=False, case=False)]

print("3. Aplicando limpieza de datos (Avance 2)...")
df_limpio = df_valpo[(df_valpo['NIVEL_MADRE'] != 9) & (df_valpo['EST_CIV_MADRE'] != 9)].copy()
df_limpio = df_limpio[df_limpio['GRUPO_ETARIO_MADRE'] != 'no especificado']
df_limpio = df_limpio[(df_limpio['SEMANAS'] >= 20) & (df_limpio['SEMANAS'] <= 45)]

print("4. Transformando variables para Streamlit...")
# Mapeo de Educación separando a las madres extranjeras (Secundario)
mapa_educacion = {
    1: 'Superior', 
    2: 'Medio (Chilenas)', 
    3: 'Secundario (Extranjeras)', 
    4: 'Básico/Primario', 
    5: 'Ninguno'
}
df_limpio['NIVEL_DESC'] = df_limpio['NIVEL_MADRE'].map(mapa_educacion)

# Agrupar Estado Civil
mapa_civil = {1: 'Soltera', 2: 'Casada', 3: 'Otra', 4: 'Otra', 5: 'Otra', 6: 'Conviviente Civil'}
df_limpio['CIVIL_AGRUPADO'] = df_limpio['EST_CIV_MADRE'].map(mapa_civil)

# Crear variable binaria de Bajo Peso (NUEVO)
df_limpio['BAJO_PESO'] = df_limpio['RANGO_PESO'].apply(lambda x: 1 if x in ['< 1500', '1500 - 2499'] else 0)

print("5. Guardando archivo procesado...")
df_limpio.to_csv('data/processed/nacimientos_valpo_limpio.csv', index=False)
print("¡Éxito! Archivo guardado listo para usar en Streamlit.")