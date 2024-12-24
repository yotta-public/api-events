import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os  # Importar el módulo os para trabajar con rutas de archivos

# Función para obtener los datos de un día específico y transformar la fecha
def obtener_datos_dia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    eventos = []
    for item in soup.find_all('li', class_='dailyevent'):
        deporte = item.find('span', class_='dailyday').text
        hora = item.find('strong', class_='dailyhour').text
        dia_texto = item.find_previous('span', class_='title-section-widget').text.strip()
        
        dia_texto_partes = dia_texto.split()
        if len(dia_texto_partes) >= 5:
            dia_numerico = dia_texto_partes[0]
            dia_numerico = ''.join(filter(str.isdigit, dia_numerico))  # Eliminar el día de la semana (Ejemplo: Miércoles25)
            mes_nombre = dia_texto_partes[2]  # Este es el nombre del mes (por ejemplo, "Diciembre")
            año = dia_texto_partes[4]
            mes_actual = mes_a_numero(mes_nombre)  # Convertimos el nombre del mes a número Diciembre -> 12
            dia_texto_formateado = f"{dia_numerico} {mes_actual} {año}"
        
            # Usamos el formato correcto (día, mes numérico, año)
            dia = datetime.strptime(dia_texto_formateado, "%d %m %Y").strftime("%d/%m/%Y")  # Transformar la fecha a dd/mm/yyyy
        else:
            dia = "Fecha no válida"
        
        canal = item.find('span', class_='dailychannel').text.strip()
        encuentro = item.find('h4', class_='dailyteams').text.strip()
        
        eventos.append({
            'deporte': deporte,
            'hora': hora,
            'dia': dia,
            'canal': canal,
            'encuentro': encuentro
        })
    
    return eventos

def mes_a_numero(mes):
    meses = {
        "Enero": "01",
        "Febrero": "02",
        "Marzo": "03",
        "Abril": "04",
        "Mayo": "05",
        "Junio": "06",
        "Julio": "07",
        "Agosto": "08",
        "Septiembre": "09",
        "Octubre": "10",
        "Noviembre": "11",
        "Diciembre": "12"
    }
    
    mes = mes.capitalize()  # Asegura que la primera letra esté en mayúscula
    
    # Obtener el número del mes en formato de dos dígitos
    return meses.get(mes, "Mes no válido")

# URL de la página web
url = "https://www.marca.com/programacion-tv.html"

# Obtener los datos
datos = obtener_datos_dia(url)

# Obtener la ruta del directorio donde se encuentra el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Crear la ruta completa para el archivo JSON
ruta_json = os.path.join(directorio_actual, 'eventos.json')

# Guardar los datos en un archivo JSON en el mismo directorio
with open(ruta_json, 'w') as json_file:
    json.dump(datos, json_file, indent=4)

print(json.dumps(datos, indent=4))
