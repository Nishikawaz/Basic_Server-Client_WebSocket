import socket

# Configuración global
IP = "127.0.0.1"
PORT = 6869
BUFFER = 1024

CLIENTES = []

# Configuración inicial del servidor
def setup_server(ip, port):
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((ip, port))
        socket_server.listen()
        socket_server.setblocking(False)
        print(f"[SISTEMA] Servidor configurado y en modo escucha - {ip}:{port}")
        return socket_server
    except OSError as e:
        print(f"Error al configurar servidor: {e}")
        exit(1)

def handle_new_connection(server, cliente):
    try:
        (socket_client, client_address) = server.accept()
        socket_client.setblocking(False)
        CLIENTES.append(socket_client)
        print(f"Conexión aceptado - Conexión desde: {client_address[0]}:{client_address[1]}")
    except Exception as e:
        print(f"Error al aceptar conexión: {e}")

