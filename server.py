import socket

# Configuración global
IP = "127.0.0.1"
PORT = 6869
BUFFER = 1024

SOCKETS = [] 

# Función para configurar inicialmente el socket_servidor
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

# Función para aceptar sockets_clientes desde el socket_servidor
def accept_client(socket_server):
    try:
        (socket_client, client_address) = socket_server.accept()
        socket_client.setblocking(False)
        SOCKETS.append(socket_client)
        print(f"Conexión establecida con el cliente - Conexión desde: {client_address[0]}:{client_address[1]}")
    except Exception as e:
        print(f"Error al aceptar conexión: {e}")

# Función para desconectar al socket_cliente 
def disconnect(socket_client):
    if socket_client in SOCKETS:
        SOCKETS.remove(socket_client)
    try:
        socket_client.close()
    except:
        pass
    print(f"[SERVER] Cliente desconectado")

# Función de envío de mensaje tipo broadcast (a todos menos al emisor)
def broadcast(message, socket_sender):
    for client in SOCKETS:
        if client != socket_sender:
            try:
                client.send(message.encode("utf-8"))
            except:
                disconnect(client)

# Función de gestión de los socket_clients. Verifica el envío de mensajes o desconexión
def client_management(socket_client):
    try: 
        message = socket_client.recv(BUFFER)
    except OSError:
        disconnect(socket_client)
        return
    
    if not message:
        disconnect(socket_client)
        return
    
    broadcast(message, socket_client)