import socket
import select 

# Variables de configuración del servidor 
HOST = "127.0.0.1"   # Localhost
PORT = 6869          # Puerto donde se escucharán las conexiones del servidor
BUFFER = 1024        # Memoria intermedia que permite acumular datos entrantes/salientes en conexión de red

listado_cliente = [] # Listado de sockets activos (incluyendo al server)

# Configuración inicial del servidor
def setup_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Crea un objeto "server_socket" [con AF_INET=IPv4] [SOCK_STREAM = TCP/IP]
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar la dirección del socket [SOL_SOCKET = Nivel base de opciones] [SO_REUSADDR = permite reuse para evitar errores de OS "Address already in use"] [1 = True -- Activación del SO_REUSEADDR]
        server_socket.bind((HOST, PORT))                                     # Asocia el socket a la dirección y puerto especificados
        server_socket.listen()                                               # Comienza a escuchar conexiones entrantes
        print(f"Servidor escuchando en {host}:{port}")
        return server_socket                                                 # Devolución del socket ya configurado
    except OSError as e:
        print(f"Error al configurar servidor: {e}")                          # Caso de error de Sistema Operativo
    except KeyboardInterrupt:
        print(f"Servidor detenido manualmente")                              # Caso de error con teclado
        exit(0)

# Envío de mensajes a todos los clientes conectados excepto al remitente
def broadcast(emisor, mensaje, clientes):
    for cliente in clientes:                                                 # Itera sobre la lista de clientes conectados
        if cliente != emisor:                                                # Si el cliente no es el remitente del mensaje:
            try:                         
                cliente.send(mensaje.encode("utf-8"))                        # Envía el mensaje al cliente
            except BrokenPipeError:
                print(f"Cliente desconectado [BrokenPipe]")                  # A menos que sea error del tipo "BrokenPipe" y se tenga que desconectar
                disconnect(cliente, clientes)
            except ConnectionResetError:
                print(f"El cliente reinició la conexión")                    # A menos que sea error del tipo "ConnectionReset" y se tenga que desconectar
                disconnect(cliente, clientes)
            except ConnectionRefusedError:
                print(f"Se ha rechazado la conexión con el cliente")         # A menos que sea error del tipo "ConnectionRefused" y se tenga que desconectar
                disconnect(cliente, clientes)
            except ConnectionAbortedError:
                print(f"Se ha abortado la conexión con el cliente")          # A menos que sea error del tipo "ConnectionAborted" y se tenga que desconectar
                disconnect(cliente, clientes)
            except OSError as e:                                    
                print(f"Error de red al enviar: {e}")                        # A menos que sea error del Sistema Operativo y se tenga que desconectar
                disconnect(cliente, clientes)
            except KeyboardInterrupt:
                print(f"Servidor detenido manualmente")                      # A menos de que sea un error de interrupción manual con el teclado
                exit(0)                                                       


# Función de desconexión con remove y close para dar un cierra limpio
def disconnect(socket, clientes):
    if socket in clientes:                                                   # Verifica si socket está en la lista de clientes activos
        try:
            clientes.remove(socket)                                          # Se remueve el socket del listado de clientes
        except ValueError:
            print("Error: socket no listado")                                # A menos que no esté listado el socket
    try:
        socket.close()                                                       # Se trata de cerrar el socket
    except OSError as e:                    
        print(f"Error al cerrar socket: {e}")                                
    print("cliente desconectado")

# Función para manejo de nuevo cliente al servidor
def handle_new_connection(server, clientes):
    try:
        client_socket, client_address = server.accept()                      # Acepta la conexión entrante y devuelve el socket y la dirección del cliente 
        clientes.append(client_socket)                                       # Agrega el socket también a la lista de clientes
        print(f"Conexión aceptada de {client_address}")                      # Mensaje de conexión con la dirección del cliente
    except BlockingIOError:
        print("No hay conexiones pendientes (modo no bloqueante)")           # A menos que presente Error por blocking de Input/Output 
    except OSError as e:
        print(f"Error al aceptar conexión: {e}")
    except KeyboardInterrupt:
        print("Servidor detenido manualmente.")
        exit(0)

# Función para manejo de los mensajes de los clientes
def handle_client_message(socket, clientes):
    try:
        mensaje = socket.recv(BUFFER)                                        # Intenta recibir datos del cliente, usando el tamaño del buffer definido
        if not mensaje:
            disconnect(socket, clientes)   
            return
        try:
            texto = mensaje.decode("utf-8")   
            broadcast(socket, texto, clientes)                               # Se difunde el mensaje recibido a los demás clientes
        except UnicodeDecodeError:
            print("Error al decodificar mensaje (no UTF-8).")                # Error al decodificar mensaje utf-8
    except ConnectionResetError:
        print("Cliente cerró la conexión abruptamente.")
        disconnect(socket, clientes)
    except TimeoutError:                                                     # Error por tiempo de espera
        print("Tiempo de espera agotado al recibir datos.")
    except OSError as e:
        print(f"Error de red al recibir: {e}")
        disconnect(socket, clientes)
    except KeyboardInterrupt:
        print("Servidor detenido manualmente.")
        exit(0)

def main():
    # Configuración del servidor y lo agrega a la lista de sockets activos
    server = setup_server(HOST, PORT)                                        # Inicializa el socket servidor con localhost y puerto definido
    listado_cliente.append(server)                                           # Incluye el servidor en la lista para que select lo monitoree

    while True:                                                              # Bucle infinito para mantener el servidor activo
        try:
            readable, _, _ = select.select(listado_cliente, [], [])          # select.select monitorea múltiples sockets a la vez y "readable" indica la lista de sockets para la lectura

            for sock in readable:                                            # Itera sobre los sockets listos
                if sock is server:                                           
                    handle_new_connection(server, listado_cliente)           # Si el socket es el servidor, significa que hay nueva conexión
                else:                                                        
                    handle_client_message(sock, listado_cliente)             # Si no es así, significa que un cliente envió datos

        except KeyboardInterrupt:                                            # Permite detener el servidor con "Ctrl + C"
            print("Servidor detenido manualmente.")
            break                                                            # Mensaje de que se detiene manualmente y se sale del bucle principal

    # Al salir del bucle, se cierran todos los sockets activos
    for sock in listado_cliente:
        try:
            sock.close()                                                     # Cierra cada socket para liberar recursos
        except OSError as e:
            print(f"Error al cerrar socket: {e}")                     