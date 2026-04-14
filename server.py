import socket
import select # Permite vigilar múltiples conexiones de socket sin usar hilos para cada uno

# Variables de configuración del servidor 
HOST = "127.0.0.1" # Localhost
PORT = 6869        # Puerto donde se escucharán las conexiones del servidor
listado_cliente = {}

# Configuración inicial del servidor
def setup_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Crea un objeto "server_socket" [con AF_INET=IPv4] [SOCK_STREAM = TCP/IP]
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección del socket [SOL_SOCKET = Nivel base de opciones] [SO_REUSADDR = permite reuse para evitar errores de OS "Address already in use"] [1 = True -- Activación del SO_REUSEADDR]
    server_socket.bind((HOST, PORT))                                     # Asocia el socket a la dirección y puerto especificados
    server_socket.listen()                                               # Comienza a escuchar conexiones entrantes
    print(f"Servidor escuchando en {HOST}:{PORT}")
    return server_socket                                                 # Devolución del socket ya configurado

# Función de desconexión con remove y close para dar un cierra limpio
def desconnect(socket):
    if socket in listado_cliente:
        listado_cliente.remove(socket)
    try:
        socket.close()
    except:
        pass
    print("Cliente desconectado")

# Envío de mensajes a todos los clientes conectados excepto al remitente
def broadcast(emisor, mensaje, cliente):
    for cada_cliente in listado_cliente: # Itera sobre la lista de clientes conectados
        if cliente != emisor:            # Si el cliente no es el remitente del mensaje:
            try:                         
                cliente.send(mensaje)    # Envía el mensaje al cliente
            except:                      # Si ocurre un error al enviar el mensaje, se asume que el cliente se ha desconectado
                desconnect(cliente)

