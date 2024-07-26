import pandas as pd
import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# URL path GitHub
# Vet = 'https://github.com/cvillarramo/Vet_Mexicali/raw/main/Vet.xlsx'
# URL Path working local
Vet ="Vet.xlsx"

#### Functions ######

def fetch_veterinarias():
    """Load data from Excel File"""
    df = pd.read_excel(Vet)
    return df
 
def geocode_address(address, geolocator): 
   """Geocode the address when needed to get lat and long. 
   Geopy has a precision around 2.7 km, don't like it, think about and improvement for next iteration"""
   
   try:
        location = geolocator.geocode(address,timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
   except GeocoderTimedOut:
        return geocode_address(address, geolocator) 
   except Exception as e:
        print('Error geocodificandola direccion {address}: {e}')
        return None, None


##### Streamlit #####
st.title('Buscador de Veterinarias')

# Load Data
df = fetch_veterinarias()

# Apply filters by user
st.sidebar.header('Filtros')
atencion_urgencias = st.sidebar.checkbox('Atiende urgencias')
tarifa_rescatados = st.sidebar.checkbox('Tarifa preferencial animales rescatados')
servicio_domicilio = st.sidebar.checkbox('Servicio a domicilio')

if atencion_urgencias:
    df = df[df['Atiende urgencias'] == 'Si']
if tarifa_rescatados:
    df = df[df['Tarifa preferencial animales rescatados'] == 'Si']
if servicio_domicilio:
    df = df[df['Servicio a domicilio'] == 'Si']

####### Display Map #########
st.subheader('Mapa de Veterinarias')
st.write('Haz clic en los marcadores para ver más información.')

# Initialize geolocator
geolocator = Nominatim(user_agent="MyVetApp")

# Filter and filling missing coordinates
df_missing_coords = df[df['latitud'].isna() | df['longitud'].isna()]

for index, row in df_missing_coords.iterrows():
    address=row['Direccion']
    lat,lon = geocode_address(address, geolocator)
    df.at[index,'latitud'] = lat
    df.at[index,'longitud']= lon

if 'latitud' in df.columns and 'longitud' in df.columns:
    # Create Map
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

