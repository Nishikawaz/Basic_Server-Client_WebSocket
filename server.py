import socket
import select 

# Variables de configuración del servidor 
HOST = "127.0.0.1"   # Localhost
PORT = 6869          # Puerto donde se escucharán las conexiones del servidor
BUFFER = 1024        # Memoria intermedia que permite acumular datos entrantes/salientes en conexión de red

listado_cliente = {} # Listado de sockets activos (incluyendo al server)

# Configuración inicial del servidor
def setup_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Crea un objeto "server_socket" [con AF_INET=IPv4] [SOCK_STREAM = TCP/IP]
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección del socket [SOL_SOCKET = Nivel base de opciones] [SO_REUSADDR = permite reuse para evitar errores de OS "Address already in use"] [1 = True -- Activación del SO_REUSEADDR]
    server_socket.bind((HOST, PORT))                                     # Asocia el socket a la dirección y puerto especificados
    server_socket.listen()                                               # Comienza a escuchar conexiones entrantes
    print(f"Servidor escuchando en {HOST}:{PORT}")
    return server_socket                                                 # Devolución del socket ya configurado

# Envío de mensajes a todos los clientes conectados excepto al remitente
def broadcast(emisor, mensaje, cliente):
    for cada_cliente in listado_cliente:                # Itera sobre la lista de clientes conectados
        if cliente != emisor:                           # Si el cliente no es el remitente del mensaje:
            try:                         
                cliente.send(mensaje.encode("utf-8"))   # Envía el mensaje al cliente
            except:                                     # Si ocurre un error al enviar el mensaje, se asume que el cliente se ha desconectado
                disconnect(cliente)                     # Se desconecta al cliente

# Función de desconexión con remove y close para dar un cierra limpio
def disconnect(socket):
    if socket in listado_cliente:
        listado_cliente.remove(socket)
    try:
        socket.close()
    except:
        pass
    print("Cliente desconectado")

def handle_new_connection(server, socket_list, clientes):
    client_socket, client_address = server.accept()
    socket_list.append(client_socket)
    clientes.append(client_socket)
    print(f"Conexión aceptada de {client_address}")

def handle_client_message(socket, socket_list, clientes):
    try:
        mensaje = socket.recv(BUFFER)
        if not mensaje:
            socket_list.remove(socket)
            clientes.remove(socket)
            socket.close()
            return
        broadcast(socket, mensaje, clientes)
    except:
        socket_list.remove(socket)
        clientes.remove(socket)
        socket.close()

