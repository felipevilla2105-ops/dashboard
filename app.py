import pandas as pd
import streamlit as st

url = "https://github.com/felipevilla2105-ops/curso-talento-t/raw/refs/heads/main/datos_generales_ficticios.xlsx"
df = pd.read_excel(url)


seleccion_columnas = ['FECHA_HECHOS', 'DELITO', 'ETAPA','FISCAL_ASIGNADO', 'DEPARTAMENTO', 'MUNICIPIO_HECHOS']
df = df[seleccion_columnas].sort_values(by='FECHA_HECHOS', ascending=True).reset_index(drop=True)

df['FECHA_HECHOS'] = pd.to_datetime(df['FECHA_HECHOS'], errors='coerce')

#construir la pagina
st.set_page_config(page_title="Análisis de Delitos", layout="centered")
st.header("Análisis de Delitos") 
st.dataframe(df)

st.subheader("Tipo de Delito")
delitos = df['DELITO'].value_counts()
st.bar_chart(delitos)
