import googlemaps
import mysql.connector

# Configuración de la API de Google Maps
gmaps = googlemaps.Client(key='API_KEY_GOOGLE_MAPS')

# Conexión a la base de datos MySQL
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql',
    'database': 'etl'
}

#inicializamos la conexión a la base de datos con los parámetros de arriba
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Definir la región o país (en este caso, Colombia), el radio y el tipo de comercio
localidad = (4.711239189422248, -74.07692563419873)
radius = 1000
tipo_comercio = "restaurant"

# Extraer información de comercios de Google Maps
def extraer_comercios():
    resultados = []
    places = gmaps.places(location=localidad, radius=radius, type=tipo_comercio)
    print(places)

    #Recorrido para extraer los datos de los locales
    for place in places['results']:
        nombre = place['name']
        direccion = place['formatted_address']
        latitud = place['geometry']['location']['lat']
        longitud = place['geometry']['location']['lng']
        rating = place['rating']
        resultados.append((nombre, direccion, latitud, longitud, rating))

    return resultados

# Transformar los datos y almacenarlos en MySQL
def cargar_datos_en_mysql(data):
    insert_query = "INSERT INTO comercios (nombre, direccion, latitud, longitud, rating) VALUES (%s, %s, %s, %s, %s)"

    for comercio in data:
        cursor.execute(insert_query, comercio)
        conn.commit()

try:
    comercios_colombia = extraer_comercios()
    cargar_datos_en_mysql(comercios_colombia)
    print("Datos cargados exitosamente en MySQL.")
except Exception as e:
    print("Error:", str(e))
finally:
    cursor.close()
    conn.close()