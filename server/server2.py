from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import sqlite3

app = Flask(__name__)

DATABASE = "contaminacion.db" ## nombre base de datos

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS T_Conta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nodo TEXT,
            d01 INTEGER,
            d25 INTEGER,
            d10 INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Datos recibidos:", data) 
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        for nodo, valores in data.items():
            for lectura in valores:
                cursor.execute(
                    "INSERT INTO T_Conta (nodo, d01, d25, d10) VALUES (?, ?, ?, ?)",
                    (nodo, lectura['d01'], lectura['d25'], lectura['d10'])
                )
        conn.commit()
        conn.close()
        return jsonify({"message": "Datos almacenados exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM T_Conta ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        # enviarlos como JSON
        data = [
            {"id": row[0], "nodo": row[1], "d01": row[2], "d25": row[3], "d10": row[4], "timestamp": row[5]}
            for row in rows
        ]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
