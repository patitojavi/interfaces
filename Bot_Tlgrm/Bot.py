import matplotlib.pyplot as plt
import telepot
import requests 
import time  

TOKEN_BOT = '7872416495:AAE02tAoiDM76qw_RVK2le8xqW_ShyK3RAk'  #cambiar Token
ID_CHAT = '6023293202'  #Cambiar ID

URL_SERVIDOR = "http://127.0.0.1:5000/data"

def get_datos():
    """
    Obtiene los últimos 100 registros del nodo 'N2' desde el servidor Flask.
    """
    try:
        respuesta = requests.get(URL_SERVIDOR)  
        respuesta.raise_for_status() 
        datos = respuesta.json() 
        
        return datos[-100:]  # Retorna los últimos 100 registros

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        return []  

def grafica(datos):
    """
    Genera una gráfica de los datos de partículas PM del nodo 'N2'.
    """
    if not datos:
        print("No hay datos disponibles.")
        return None

    pm_01 = [registro['d01'] for registro in datos]
    pm_25 = [registro['d25'] for registro in datos]
    pm_10 = [registro['d10'] for registro in datos]

    ventana = 50  
    pm_01_ventana = pm_01[-ventana:]
    pm_25_ventana = pm_25[-ventana:]
    pm_10_ventana = pm_10[-ventana:]

    pm_01_ventana.reverse()
    pm_25_ventana.reverse()
    pm_10_ventana.reverse()

    plt.figure(figsize=(10, 6))
    plt.plot(pm_01_ventana, label="PM 0.1 (d01)", color="red", linestyle='-', marker='o')
    plt.plot(pm_25_ventana, label="PM 2.5 (d25)", color="green", linestyle='--', marker='x')
    plt.plot(pm_10_ventana, label="PM 10 (d10)", color="blue", linestyle='-.', marker='s')

    plt.title("Concentración de Partículas en Nodo 'N2'", fontsize=16)
    plt.xlabel("Índice de Muestra", fontsize=12)
    plt.ylabel("Concentración (µg/m³)", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    archivo_grafica = "grafica_nodo_n2.png"
    plt.savefig(archivo_grafica)
    plt.close() 
    return archivo_grafica

def enviar_telegram(archivo_grafica):
    """
    Envía la gráfica generada a un chat de Telegram.
    """
    try:
        bot = telepot.Bot(TOKEN_BOT)
        bot.sendPhoto(ID_CHAT, photo=open(archivo_grafica, "rb")) 
        print("Gráfica enviada exitosamente.")
    except Exception as e:
        print(f"Error al enviar la gráfica a Telegram: {e}")

if __name__ == "__main__":
    while True:
        datos = get_datos()  
        if datos:
            archivo_grafica = grafica(datos)  
            if archivo_grafica:
                enviar_telegram(archivo_grafica)  
        time.sleep(3)  
