import os
import time
import requests


IMG_FOLDER = "IMG"
SERVER_URL = "http://127.0.0.1:5000/upload"  

def enviar_imagenes():
    for imagen_nombre in os.listdir(IMG_FOLDER):
        imagen_ruta = os.path.join(IMG_FOLDER, imagen_nombre)
        if os.path.isfile(imagen_ruta):
            with open(imagen_ruta, 'rb') as archivo_imagen:
                files = {'imagen': (imagen_nombre, archivo_imagen, 'image/jpeg')}
                response = requests.post(SERVER_URL, files=files)
                print(f"Enviando {imagen_nombre}: {response.status_code}")
            time.sleep(3)  

if __name__ == "__main__":
    enviar_imagenes()
