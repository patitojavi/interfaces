import requests
import json
import random
import time

def generate_data():
    data = {
        'N1': [{'d01': random.randint(1, 10), 'd25': random.randint(1, 10), 'd10': random.randint(1, 10)}],
        'N2': [{'d01': random.randint(1, 10), 'd25': random.randint(1, 10), 'd10': random.randint(1, 10)}],
        'N3': [{'d01': random.randint(1, 10), 'd25': random.randint(1, 10), 'd10': random.randint(1, 10)}]
    }
    return data
SERVER_URL = "http://127.0.0.1:5000/data"

for i in range(100):
    json_data = generate_data()
    try:
        response = requests.post(SERVER_URL, json=json_data)
        print(f"Envío {i+1}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al enviar datos: {e}")
    time.sleep(3)  
