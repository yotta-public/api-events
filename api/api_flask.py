from flask import Flask, jsonify
from api import obtener_datos_dia  # Asegúrate de que api.py esté en el mismo directorio

app = Flask(__name__)

@app.route('/eventos', methods=['GET'])
def eventos():
    url = "https://www.marca.com/programacion-tv.html"  # La URL desde la que obtienes los datos
    datos = obtener_datos_dia(url)
    return jsonify(datos)  # Devuelve los datos como una respuesta JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # El servidor escuchará en el puerto 5000
