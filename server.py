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
        print(f"Servidor escuchando - {ip}:{port}")
        return socket_server
    except OSError as e:
        print(f"Error al configurar servidor: {e}")
        exit(1)
