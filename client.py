import socket
import threading
import time 

# Configuración global
IP = "127.0.0.1"
PORT = 6869
BUFFER = 1024
DELAY = 3

# Socket actual del cliente
socket_client = None

# Variable bandera para saber si se da el cierre al programa
closing = False

def client_connect():
    global socket_client

    while socket_client is None and not closing:
        try:
            socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_client.connect((IP, PORT))
            print(f"[SISTEMA] Conectado al server: \nIP:{IP} \nPORT:{PORT}")
            return socket_client
        except ConnectionRefusedError:
            print(f"[SISTEMA] No se pudo conectar. Reintentando en {DELAY} segundos")
            time.sleep(DELAY)
        except OSError:
            if not closing:
                print(f"No se pudo conectar. Reintentando en {DELAY} segundos")
                time.sleep(DELAY)

def client_disconnect():
    global socket_client

    if socket_client is not None:
        try:
            socket_client.close()
        except OSError:
            print(f"Error al cerrar la conexión del cliente")

        socket_client = None

def receive_messages():
    global socket_client

    while True:
        if closing:
            break
        if socket_client is None:
            client_connect()
            continue
        try:
            message = socket_client.recv(BUFFER)
            if not message:
                raise ConnectionError
            print(message.decode("utf-8"))
        except (ConnectionError, OSError):
            if closing:
                break
            print("[SISTEMA] Se perdió la conexión con el server")
            client_disconnect()
            time.sleep(DELAY)
            