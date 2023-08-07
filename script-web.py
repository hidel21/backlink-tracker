import streamlit as st
import pandas as pd
import pickle
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import nltk
import base64
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from utils import Utils

utils = Utils()


nltk.download('stopwords')

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CREDENTIALS_FILE = 'client_secret_key.json'
URI_REDIRECCIONAMIENTO = [
    'http://localhost:8501/'
     ]

class BacklinkTracker:
    def __init__(self, gsc_service):
        self.gsc_service = gsc_service

    def get_backlink_type(self, url, backlink):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            if a['href'] == backlink:
                if 'rel' in a.attrs and 'nofollow' in a['rel']:
                    return 'nofollow'
                else:
                    return 'follow'
        return 'Unknown'

    def get_backlinks_data_gsc(self, property_uri, start_date, end_date):
        # Convierte el datetime a string
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Utiliza Utils.date_interval para obtener intervalos de fechas mensuales
        date_intervals = utils.date_interval(start_date_str, end_date_str, date_interval='P1M')

        # Inicializar un diccionario para almacenar los resultados de cada mes
        monthly_data = {}

        # Realizar una consulta para cada intervalo de fechas
        for interval in date_intervals:
            start = interval['inicio']
            end = interval['fin']

            # Prepara la solicitud
            request = {
                'startDate': start,
                'endDate': end,
                'dimensions': ['date', 'query'],
                'dimensionFilterGroups': [
                    {
                        'filters': [
                            {
                                'dimension': 'page',
                                'operator': 'equals',
                                'expression': property_uri
                            }
                        ]
                    }
                ]
            }

            # Realiza la consulta
            response = self.gsc_service.searchanalytics().query(siteUrl=property_uri, body=request).execute()

            # Convertir la respuesta en un DataFrame
            data = []
            for row in response['rows']:
                date = row['keys'][0]
                query = row['keys'][1]
                clicks = row['clicks']
                impressions = row['impressions']
                ctr = row['ctr']
                position = row['position']
                #backlink_type = self.get_backlink_type(url, query)
                data.append([date, query, clicks, impressions, ctr, position])
            df = pd.DataFrame(data, columns=['Date', 'Query', 'Clicks', 'Impressions', 'CTR', 'Position', 'Backlink Type'])

            # Almacenar el DataFrame en el diccionario
            monthly_data[f'{start} to {end}'] = df

            # Guardar el DataFrame en un archivo Excel
            df.to_excel(f'consulta-base-{start}-{end}.xlsx', index=False)

        return monthly_data

def leer_urls_desde_archivo(archivo):
    # Determinar el formato del archivo
    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo)
    elif archivo.endswith('.xlsx'):
        df = pd.read_excel(archivo)
    else:
        print(f"Formato de archivo no soportado: {archivo}")
        return None

    # Asegurarse de que el DataFrame tiene una columna llamada 'URL'
    if 'URL' not in df.columns:
        print("El archivo no tiene una columna 'URL'")
        return None

    # Devolver la lista de URLs
    return df['URL'].tolist()

nltk.download('stopwords')

# Función para guardar las credenciales en un archivo pickle
def guardar_credenciales(credenciales):
    with open('credenciales.pickle', 'wb') as f:
        pickle.dump(credenciales, f)

# Función para cargar las credenciales desde un archivo pickle
def cargar_credenciales():
    try:
        with open('credenciales.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Función para autenticar o cargar las credenciales
def autenticar():
    credenciales = cargar_credenciales()

    if credenciales:
        return build('webmasters', 'v3', credentials=credenciales)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri=URI_REDIRECCIONAMIENTO[0])
        credenciales = flow.run_local_server(port=8501)

        guardar_credenciales(credenciales)
        return build('webmasters', 'v3', credentials=credenciales)

# Autenticar a la API de Google Search Console
gsc_service = autenticar()

# Inicializar el rastreador de backlinks
tracker = BacklinkTracker(gsc_service)
# Define the Streamlit app

def app():
    st.title('Backlink Tracker')
    
    # Add a file uploader to allow the user to upload a CSV or Excel file with URLs
    archivo = st.file_uploader('Cargar archivo de URLs', type=['csv', 'xlsx'])
    
    # If a file has been uploaded, read the URLs from the file
    if archivo is not None:
        urls = leer_urls_desde_archivo(archivo)
        
        # If URLs were successfully read from the file, display them in a table
        if urls is not None:
            st.write('URLs cargadas:')
            df = pd.DataFrame({'URL': urls})
            st.write(df)
            
            # Add date pickers to allow the user to select a date range
            st.write('Seleccionar rango de fechas:')
            start_date = st.date_input('Fecha de inicio')
            end_date = st.date_input('Fecha de fin')
            
            # Add a button to start the backlink tracking process
            if st.button('Iniciar seguimiento de backlinks'):
                # Call the get_backlinks_data_gsc method of the BacklinkTracker class to get backlink data from Google Search Console
                st.write('Obteniendo datos de backlinks...')
                data = tracker.get_backlinks_data_gsc(urls[0], start_date, end_date)
                
                # Display the backlink data in a table for each month
                for key, value in data.items():
                    st.write(key)
                    st.write(value)
    else:
        st.write('Por favor, cargue un archivo de URLs.')
if __name__ == '__main__':
    app()