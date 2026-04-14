import socket
import select # Permite vigilar múltiples conexiones de socket sin usar hilos para cada uno

# configuraciones 
HOST = "127.0.0.1" # Localhost
PORT = 6869        # Puerto donde se escucharán las conexiones del servidor

# Envío de mensajes a todos los clientes conectados excepto al remitente
def broadcast(emisor, mensaje, cliente):
    for clientes in cliente:             # Itera sobre la lista de clientes conectados
        if cliente != emisor:            # Si el cliente no es el remitente del mensaje:
            try:                         
                cliente.send(mensaje)    # Envía el mensaje al cliente
            except:                      # Si ocurre un error al enviar el mensaje, se asume que el cliente se ha desconectado
                cliente.close()          # Se cierra la conexión del cliente
                cliente.remove(cliente)  # Se elimina al cliente de la lista de clientes

