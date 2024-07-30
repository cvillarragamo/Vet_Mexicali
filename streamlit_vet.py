import pandas as pd
import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


#Exel file Path
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
            "text": "{Nombre}\nTeléfono: {Telefono}\n{Direccion}\nHorario: {Horario}\nAtiende urgencias: {Atiende urgencias}\nTarifa preferencial: {Tarifa preferencial animales rescatados}\nServicio a domicilio: {Servicio a domicilio}"
        }
    )
    st.pydeck_chart(deck)
else:
    st.write("El archivo Excel no contiene columnas de latitud y longitud.")



####### Visit Counter ##### 
#This is just for fun. It is not persistent, so it would restart each re-run of the app.

if 'visitas' not in st.session_state:
    st.session_state.visitas = 1
else:
    st.session_state.visitas += 1

#Counter Container
with st.container():
    st.write("---")  # horizontal line for visual separation
    col1, col2 = st.columns([1, 1])  # Divide into columns for better visual distribution

    # Emoji for the "First" column
    with col1:
        st.markdown("""
            <h3 style='text-align: center; color: blue;'>
                👀🐶
            </h3>
        """, unsafe_allow_html=True)

    # visit counter in the other column
    with col2:
        st.markdown(f"""
            <h5 style='text-align: center; color: grey;'>
                Esta aplicación ha sido visitada {st.session_state.visitas} veces en esta sesión.
            </h5>
        """, unsafe_allow_html=True)
    st.write("---")  # horizontal line for aesthetics


####### Footer section for contributions ############
st.markdown("""
#### ¿Quieres contribuir?
<i>Si tienes más información o sugerencias, no dudes en escribirme a:</i> <a href="mailto:cvillarragamo@gmail.com"><b><i>Enviar Email</i></b></a>
""", unsafe_allow_html=True)