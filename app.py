import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.signal import find_peaks
import plotly.graph_objects as go

# Cargar datos desde el archivo Excel en GitHub
url = "https://github.com/felipevilla2105-ops/curso-talento-t/raw/refs/heads/main/generales_ficticios.csv"
df = pd.read_csv(url)

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

#construir la pagina le damos una imagen al titulo 
st.set_page_config(page_title="Dashboard de Delitos - Fiscalia", layout="wide")
st.markdown(
    """
    <style>
    .block-container {
        padding: 3rem 2rem 2rem 2rem;
        max-width: 1200px;
        }
        </style>
    """, 
    unsafe_allow_html=True 
)   
st.image('img\encabezado.png', use_container_width=True)

st.markdown(" # <font color='#9C99F2'> DASHBOARD DELITOS </font> ", unsafe_allow_html=True)   


# Gráfico de barras para la columna 'DELITO'
st.subheader("Tipo de Delito")
delitos = df['DELITO'].value_counts()
st.bar_chart(delitos)


st.subheader("COMPORTAMIENTO DELITOS")
delitos = df['DELITO'].value_counts()
st.bar_chart(delitos)

st.subheader("DEPARTAMENTOS CON MAS CASOS")
departamentos_mas_casos = df['DEPARTAMENTO'].value_counts()
st.bar_chart(departamentos_mas_casos)

#calculos municipio con mas delitos
max_municipio = df['MUNICIPIO_HECHOS'].value_counts().index[0].upper()
max_cantidad_municipio = df['MUNICIPIO_HECHOS'].value_counts().iloc[0]


# mostrar los municipios y conteo delitos
st.set_page_config(page_title="Análisis de Delitos", layout="centered")
st.header("Análisis de Delitos")
conteo_municipios = df['MUNICIPIO_HECHOS'].value_counts()
st.write(conteo_municipios)

#crear 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    # TARJETAS
    st.markdown(f""" <h3 style=
                'color:#F2A88D;
                background-color:#F0F2F6;
                border: 2px solid #9C99F2;
                border-radius: 10px; padding: 10px;
                text-align: center'>
                Municipio con mas delitos<br>:{max_municipio} </h3><br>""", 
                unsafe_allow_html=True)

with col2:
# TARJETA 2
    st.markdown(f""" <h3 style=
                'color:#F2A88D;
                background-color:#F0F2F6;
                border: 2px solid #9C99F2;
                border-radius: 10px; padding: 10px;
                text-align: center'>
                Delito reportado<br> {max_cantidad_municipio} </h3><br>""", 
                unsafe_allow_html=True)



st.subheader(f"Municipio con mas delitos: {max_cantidad_municipio} con {delitos} reportes")
#Gráfico de pastel para la distribución de delitos por departamento, requiero la libreria plotly
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

# Etapa del proceso con más casos
st.subheader("Etapa del Proceso")
max_etapa = df['ETAPA'].value_counts()
st.write(max_etapa)
max_etapa = df['ETAPA'].value_counts().index[0].upper()
etapa_mas_frecuente = df['ETAPA'].value_counts().iloc[0]
st.write((f"La etapa con más casos es: **{max_etapa}**"),
         (f"Con un total de: **{etapa_mas_frecuente}**"))

