# Recordando la teoría para esta consigna, del lado del server [1 solo cliente]
# El server crea su socket (Directo)
# El server tiene que asociar la IP y el Puerto (Directo)
# El listen del server se activa para ir captando la solicitud de conexión por parte del cliente (1)
# El server "escucha" la petición y acepta al cliente 
# El server recibe mensaje del cliente

# Caso del server 
import socket

HOST = "127.0.0.1" # Se usa localhost
PORT = 6869 # Puerto designado

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Se crea la variable server_socket con el objeto de la clase socket (IPv4, TCP)
server_socket.bind((HOST,PORT)) # Se bindea la IP local y un puerto designado 
server_socket.listen() # Se permite la escucha
(client_conn, addr)= server_socket.accept() # "cliente_conn" = (El objeto: socket_cliente) & "addr" = (Las direcciones: (IP, PORT) )
with client_conn:
    print(f"Client connected: {addr}") # Indicando que si se conecta el objeto socket_cliente --> haga print referenciando las direcciones.
    while True:
        data = client_conn.recv(1024) # Se define la variable "data" donde se alojan los valores recibidos
        if not data: break # Luego de que reciba los datos, rompe el bucle forzadando algo similar a un .close
        print(f"Received {repr(data)} from {(addr)}") # Leyendo la descripción built-in de "repr" parece que emula el decode