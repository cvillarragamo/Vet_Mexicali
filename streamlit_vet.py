import pandas as pd
import streamlit as st
import pydeck as pdk

# URL del archivo Excel en GitHub
# Vet = 'https://github.com/cvillarramo/Vet_Mexicali/raw/main/Vet.xlsx'
Vet ="Vet.xlsx"

def fetch_veterinarias():
    df = pd.read_excel(Vet)
    return df
 
st.title('Buscador de Veterinarias')

# Cargar datos
df = fetch_veterinarias()

# Agregar filtros
st.sidebar.header('Filtros')
atencion_urgencias = st.sidebar.checkbox('Atiende urgencias')
tarifa_rescatados = st.sidebar.checkbox('Tarifa preferencial animales rescatados')
servicio_domicilio = st.sidebar.checkbox('Servicio a domicilio')

# Aplicar filtros
if atencion_urgencias:
    df = df[df['Atiende urgencias'] == 'Si']
if tarifa_rescatados:
    df = df[df['Tarifa preferencial animales rescatados'] == 'Si']
if servicio_domicilio:
    df = df[df['Servicio a domicilio'] == 'Si']

# Mapa
st.subheader('Mapa de Veterinarias')
st.write('Haz clic en los marcadores para ver más información.')

# Suponiendo que las columnas 'latitud' y 'longitud' están disponibles
# Si no están, usa una librería de geocodificación para obtenerlas
if 'latitud' in df.columns and 'longitud' in df.columns:
    # Crear mapa
    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df['latitud'].mean(),
            longitude=df['longitud'].mean(),
            zoom=10
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position=['longitud', 'latitud'],
                get_fill_color=[255, 0, 0],
                get_radius=200,
                # radius_scale=10,
                # radius_min_max=[1,1000],
                pickable=True,
                auto_highlight=True
            )
        ],
        tooltip={
            "text": "{Nombre}\n{Telefono}\n{Direccion}\nHorario: {Horario}\nAtiende urgencias: {Atiende urgencias}\nTarifa preferencial: {Tarifa preferencial animales rescatados}\nServicio a domicilio: {Servicio a domicilio}"
        }
    )
    st.pydeck_chart(deck)
else:
    st.write("El archivo Excel no contiene columnas de latitud y longitud.")

