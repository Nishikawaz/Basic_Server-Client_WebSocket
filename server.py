import socket
import select

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
        print(f"[SISTEMA] Servidor configurado y en modo escucha \nIP: {ip} \nPORT: {port}")
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
        print(f"[SERVER] Conexión establecida con el cliente - Conexión desde: {client_address[0]}:{client_address[1]}")
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
def broadcast(message, socket_sender, socket_server):
    for client in SOCKETS:
        if client != socket_sender and client != socket_server:
            try:
                client.send(message)
            except:
                disconnect(client)

# Función de gestión de los socket_clients. Verifica el envío de mensajes o confirma la desconexión
def client_management(socket_client):
    try: 
        message = socket_client.recv(BUFFER)
        if not message:
            disconnect(socket_client)
            return

        print(f"[LOG] Mensaje recibido: {message.decode('utf-8').strip()}")
        broadcast(message, socket_client)
        
    except Exception:
        disconnect(socket_client)

# Función para "prender" el socket_server
def server_on(socket_server):
    SOCKETS.append(socket_server)
    print("[SISTEMA] El protocolo de comunicación se ha instanciado")

    try:
        while True:
            ready, _, _ = select.select(SOCKETS, [], [])
            for socket in ready:
                if socket == socket_server:
                    accept_client(socket_server)
                else:
                    client_management(socket)

    except KeyboardInterrupt:
        print("[SISTEMA] Apagando el servidor de forma manual")

    finally:
        for socket in SOCKETS:
            socket.close()
# Iniciando el server
socket_server = setup_server(IP, PORT)
server_on(socket_server)