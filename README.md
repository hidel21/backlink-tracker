# Backlink Tracker
Este es un script de Python que utiliza la biblioteca Streamlit para crear una aplicación web que permite realizar un seguimiento de los backlinks de un sitio web utilizando la API de Google Search Console. El script también utiliza otras bibliotecas de Python, como pandas, pickle, os, nltk, base64, datetime, requests, BeautifulSoup y googleapiclient.
## Funcionalidades
1. Importa las bibliotecas necesarias para la aplicación web y para interactuar con la API de Google Search Console.
2. Define una clase llamada BacklinkTracker que contiene métodos para obtener datos de backlinks de Google Search Console y para determinar el tipo de backlink (follow o nofollow) de una URL.
3. Define una función llamada leer_urls_desde_archivo que lee una lista de URLs desde un archivo CSV o Excel.
4. Define funciones para guardar y cargar las credenciales de la API de Google Search Console en un archivo pickle.
5. Define una función llamada autenticar que autentica al usuario con la API de Google Search Console y devuelve un objeto de servicio que se puede utilizar para realizar consultas a la API.
6. Define una función llamada app que crea la aplicación web utilizando Streamlit. La aplicación permite al usuario cargar un archivo CSV o Excel con una lista de URLs, seleccionar un rango de fechas y realizar un seguimiento de los backlinks de las URLs utilizando la API de Google Search Console. Los datos de backlinks se muestran en una tabla para cada mes del rango de fechas seleccionado.
7. Descarga los datos de stopwords de NLTK.
## Instalación y Configuración
Para utilizar la aplicación, sigue estos pasos:
* Clona el repositorio: `git clone https://github.com/tu-usuario/tu-proyecto.git`
* Instala las dependencias: `pip install -r requirements.txt`
* Crea un archivo `client_secret_key.json` con las credenciales de la API de Google Search Console.
* Ejecuta el script utilizando el siguiente comando en la terminal: `streamlit run backlink_tracker.py`
* Cargue un archivo CSV o Excel con una lista de URLs que desea realizar un seguimiento de los backlinks.
* Seleccione un rango de fechas.
* Haga clic en el botón "Iniciar seguimiento de backlinks".
* Los datos de backlinks se mostrarán en una tabla para cada mes del rango de fechas seleccionado.

Creado por [Hidelberg Martinez](https://www.linkedin.com/in/hidelberg-martnez-espitia/)
