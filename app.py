import pandas as pd
import streamlit as st

# Cargar datos desde el archivo Excel en GitHub
url = "https://github.com/felipevilla2105-ops/curso-talento-t/raw/refs/heads/main/datos_generales_ficticios.xlsx"
df = pd.read_excel(url)

#selecciono las columnas que me interesan y ordeno por fecha
seleccion_columnas = ['FECHA_HECHOS', 'DELITO', 'ETAPA','FISCAL_ASIGNADO', 'DEPARTAMENTO', 'MUNICIPIO_HECHOS']
#ordeno el dataframe por fecha de hechos, y las ordene de forma ascedente y reseteo el indice
df = df[seleccion_columnas].sort_values(by='FECHA_HECHOS', ascending=True).reset_index(drop=True)

#muestro la informacion del dataframe
print(df.info())

#convierto la columna de fecha a formato datetime
df['FECHA_HECHOS'] = pd.to_datetime(df['FECHA_HECHOS'], errors='coerce')
#extraigo solo la fecha sin la hora
df['FECHA_HECHOS'] = df['FECHA_HECHOS'].dt.date


# Configuración de la página y título
st.set_page_config(page_title="Análisis de Delitos", layout="centered")
st.header("Análisis de Delitos") 

# Mostrar el DataFrame
st.dataframe(df)

# Gráfico de barras para la columna 'DELITO'
st.subheader("Tipo de Delito")
delitos = df['DELITO'].value_counts()
st.bar_chart(delitos)


# Municipio con más delitos
max_municipio = df['MUNICIPIO_HECHOS'].value_counts().index[1].upper()
st.write(f"El municipio con más delitos es: **{max_municipio}**")

#construir la pagina
st.set_page_config(page_title="Análisis de Delitos", layout="centered")
st.header("Análisis de Delitos")






