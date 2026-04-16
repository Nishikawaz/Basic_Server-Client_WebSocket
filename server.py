import socket  # Librería para comunicaciones de red 
import select  # Librería para monitorear múltiples sockets simultáneamente

# Configuración
HOST = "127.0.0.1" # Localhost
PORT = 6869        # Puerto de escucha (debe ser el mismo en el cliente)
BUFFER = 1024      # Tamaño máximo de datos (en bytes) a recibir por vez

# Lista global que almacenará todos los sockets activos (servidor + clientes)
listado_cliente = [] 

# Función para configuración del servidor
def setup_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket: AF_INET (IPv4), SOCK_STREAM (TCP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reiniciar el servidor rápido si se cae, evitando el error "Address already in use"
        server_socket.bind((host, port)) # Vincula el socket a la IP y Puerto definidos
        server_socket.listen() # Pone al servidor en modo escucha para detectar intentos de conexión
        server_socket.setblocking(False) # Hace que el socket no se detenga a esperar (select maneja las conexiones) [NO BLOQUEANTE]
        print(f"Servidor escuchando en {host}:{port}")
        return server_socket
    except OSError as e:
        print(f"Error al configurar servidor: {e}")
        exit(1) 

# Función de envío de mensajes (menos al remitente)
def broadcast(emisor, mensaje, clientes, server_ref):
    for cliente in clientes[:]:  # Iteramos sobre una copia [:] para que si alguien se desconecta, no rompa el bucle
        if cliente != emisor and cliente != server_ref: # No enviamos el mensaje al emisor original ni al socket del servidor
            try:
                cliente.sendall(mensaje.encode("utf-8")) # sendall garantiza que se envíe el paquete completo sin cortes
            except:
                disconnect(cliente, clientes) # Si falla el envío, se asume que el cliente cayó y lo sacamos

# Función que cierra conexión de socket y lo elimina de la lista
def disconnect(sock, clientes):
    if sock in clientes:
        try:
            clientes.remove(sock) # Lo quita de las búsquedas del "select"
            sock.close()          # Libera el recurso en el Sistema Operativo
            print("Cliente desconectado y socket cerrado.")
        except Exception as e:
            print(f"Error al desconectar: {e}")

# Función que maneja nuevas conexiones de clientes al servidor
def handle_new_connection(server, clientes):
    try: 
        client_socket, client_address = server.accept() # accept() devuelve el nuevo socket para el cliente y su IP/Puerto
        client_socket.setblocking(False) # Evitamos que este nuevo socket bloquee el programa al leer
        clientes.append(client_socket) # Lo añadimos a la lista para que el "select" lo vigile
        print(f"Conexión aceptada de {client_address}")
    except Exception as e:
        print(f"Error al aceptar conexión: {e}")

# Función que recepciona datos de un cliente ya conectado
def handle_client_message(sock, clientes, server_ref):
    try:
        mensaje = sock.recv(BUFFER) # Intenta leer datos del buffer
        if not mensaje: # Si recv devuelve nada, es que el cliente cerró la conexión limpiamente
            disconnect(sock, clientes)
            return
        texto = mensaje.decode("utf-8") # Decodifica los bytes a texto legible
        print(f"Mensaje recibido: {texto}") 
        broadcast(sock, texto, clientes, server_ref) # Reenvía el mensaje a los demás clientes
    except (ConnectionResetError, BrokenPipeError):
        disconnect(sock, clientes) # Si el cliente se desconecta forzosamente (ej: cerró la terminal)
    except Exception as e:
        print(f"Error al recibir: {e}")
        disconnect(sock, clientes)

# Bucle del servidor
def main():
    server = setup_server(HOST, PORT) # Seteo del servidor(localhost, Puerto designado) en este caso
    listado_cliente.append(server) # El servidor también se vigila a sí mismo
    try:
        while True:
            # select.select examina qué sockets tienen datos listos para leer
            readable, _, _ = select.select(listado_cliente, [], [])
            # Se queda pausado aquí hasta que pase algo (ahorra CPU)
            for sock in readable:
                if sock is server:
                    # Si el socket listo es el server, hay un cliente nuevo pidiendo entrar
                    handle_new_connection(server, listado_cliente)
                else:
                    # Si es cualquier otro, es un cliente enviando un mensaje
                    handle_client_message(sock, listado_cliente, server)

    except KeyboardInterrupt: # Captura Ctrl+C para un cierre ordenado
        print("\nServidor detenido manualmente.")
    finally:
        for sock in listado_cliente: # Al cerrar, recorre todos los sockets y los cierra
            sock.close()

if __name__ == "__main__":
    main() 