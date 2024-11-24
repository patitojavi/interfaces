from flask import Flask, request
import sqlite3
import cv2
import numpy as np
import io

app = Flask(__name__)

DB_PATH = "Imagenes.db"

def inicializar_bd():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS T_Img (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original BLOB NOT NULL,
                canal_r BLOB NOT NULL,
                canal_g BLOB NOT NULL,
                canal_b BLOB NOT NULL,
                canal_gris BLOB NOT NULL
            )
        """)
        conn.commit()

def convertir_a_blob(imagen):
    _, buffer = cv2.imencode('.jpg', imagen)
    return buffer.tobytes()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'imagen' not in request.files:
        return "No se encontró la imagen", 400

    archivo_imagen = request.files['imagen']
    imagen_nombre = archivo_imagen.filename

    file_bytes = np.frombuffer(archivo_imagen.read(), np.uint8)
    imagen = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    canal_b, canal_g, canal_r = cv2.split(imagen)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO T_Img (original, canal_r, canal_g, canal_b, canal_gris)
            VALUES (?, ?, ?, ?, ?)
        """, (
            convertir_a_blob(imagen),
            convertir_a_blob(canal_r),
            convertir_a_blob(canal_g),
            convertir_a_blob(canal_b),
            convertir_a_blob(imagen_gris)
        ))
        conn.commit()

    return f"Imagen {imagen_nombre} procesada y almacenada", 200

if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True)
