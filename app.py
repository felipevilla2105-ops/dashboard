import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.signal import find_peaks
import plotly.graph_objects as go

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


# Municipio con más delitos el .upper() para poner en mayusculas
max_municipio = df['MUNICIPIO_HECHOS'].value_counts().index[0].upper()
st.write(f"El municipio con más delitos es: **{max_municipio}**")

# Etapa del proceso con más casos
st.subheader("Etapa del Proceso")
max_etapa = df['ETAPA'].value_counts()
st.write(max_etapa)
max_etapa = df['ETAPA'].value_counts().index[0].upper()
etapa_mas_frecuente = df['ETAPA'].value_counts().iloc[0]
st.write((f"La etapa con más casos es: **{max_etapa}**"),
         (f"Con un total de: **{etapa_mas_frecuente}**"))

st.subheader("COMPORTAMIENTO DELITOS")
delitos = df['DELITO'].value_counts()
st.bar_chart(delitos)

st.subheader("DEPARTAMENTOS CON MAS CASOS")
departamentos_mas_casos = df['DEPARTAMENTO'].value_counts()
st.bar_chart(departamentos_mas_casos)

#construir la pagina
st.set_page_config(page_title="Análisis de Delitos", layout="centered")
st.header("Análisis de Delitos")
conteo_municipios = df['MUNICIPIO_HECHOS'].value_counts()
st.write(conteo_municipios)

# Gráfico de pastel para la distribución de delitos por departamento, requiero la libreria plotly
st.subheader("DISTRIBUCION POR DELITOS")    
fig = px.pie(
    values=departamentos_mas_casos.values,
    names=departamentos_mas_casos.index)
# Mostrar el gráfico en Streamlit, con ajustes en el diseño, tamaño y leyenda
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False, height=500)      
st.plotly_chart(fig)


st.subheader("COMPORTAMIENTO DELITOS")
fig2 = px.pie(
    values=delitos.values,
    names=delitos.index)
fig2.update_layout(height=500)  
st.plotly_chart(fig2)

#gráfico 3d de lineas para los departamentos con mas casos  
st.subheader("DEPARTAMENTOS CON MAS CASOS")
fig3 = px.line_3d(
    x=departamentos_mas_casos.index,
    y=departamentos_mas_casos.values,
    z=departamentos_mas_casos.values)    
fig3.update_layout(height=500)  
st.plotly_chart(fig3)   



st.subheader("Picos de delitos por ciudad")

# Agrupa por ciudad y fecha, cuenta delitos
conteo = df.groupby(['MUNICIPIO_HECHOS', 'FECHA_HECHOS']).size().reset_index(name='cantidad')

# Selecciona una ciudad para mostrar (puedes usar un selectbox de streamlit)
ciudades = conteo['MUNICIPIO_HECHOS'].unique()
ciudad = st.selectbox("Selecciona una ciudad", ciudades, key="selectbox_picos_ciudad")

# Filtra por la ciudad seleccionada
datos_ciudad = conteo[conteo['MUNICIPIO_HECHOS'] == ciudad]
fechas = datos_ciudad['FECHA_HECHOS']
valores = datos_ciudad['cantidad'].values

# Encuentra los picos
picos, _ = find_peaks(valores)

# Gráfica
fig = go.Figure()
fig.add_trace(go.Scatter(x=fechas, y=valores, mode='lines+markers', name='Delitos'))
fig.add_trace(go.Scatter(x=fechas.iloc[picos], y=valores[picos], mode='markers', name='Picos', marker=dict(color='red', size=12)))
fig.update_layout(title=f'Cantidad de delitos y picos en {ciudad}', xaxis_title='Fecha', yaxis_title='Cantidad de delitos')
st.plotly_chart(fig)


st.subheader("Cantidad de delitos por tipo y ciudad")

# Agrupa por ciudad y tipo de delito
conteo_delitos = df.groupby(['MUNICIPIO_HECHOS', 'DELITO']).size().reset_index(name='cantidad')

# Selecciona una ciudad
ciudades = conteo_delitos['MUNICIPIO_HECHOS'].unique()
ciudad = st.selectbox("Selecciona una ciudad", ciudades, key="selectbox_tipo_ciudad")

# Filtra por la ciudad seleccionada
datos_ciudad = conteo_delitos[conteo_delitos['MUNICIPIO_HECHOS'] == ciudad]

# Gráfico de barras
fig = px.bar(datos_ciudad, x='DELITO', y='cantidad', title=f'Cantidad de delitos por tipo en {ciudad}')
st.plotly_chart(fig)



