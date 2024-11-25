import os
import time
import requests


IMG_FOLDER = "IMG"
SERVER_URL = "http://127.0.0.1:5000/upload"  

def send_images():
    for img_name in os.listdir(IMG_FOLDER):
        img_ruta = os.path.join(IMG_FOLDER, img_name)
        if os.path.isfile(img_ruta):
            with open(img_ruta, 'rb') as archivo:
                files = {'imagen': (img_name, archivo, 'image/jpeg')}
                response = requests.post(SERVER_URL, files=files)
                print(f"Enviando {img_name}: {response.status_code}")
            time.sleep(3)  

if __name__ == "__main__":
    send_images()
