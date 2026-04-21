# Recordando la teoría para esta consigna, del lado del cliente [1 solo cliente]
# El cliente crea su socket (Directo)
# El cliente trata de conectarse (En teoría el server_socket utiliza listen y accept)
# El listen del server_socket debería estar en un bucle para ir captando posibles peticiones de los clientes. 
# El cliente es aceptado y se conecta
# El cliente manda un mensaje

# Caso del cliente
import socket

HOST = "127.0.0.1" # Se usa localhost
PORT = 6869 # Puerto designado

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_cliente: # Se crea al socket_cliente(IPv4, TCP), viene a ser el "cliente_conn" del lado de mi servidor 
    socket_cliente.connect((HOST,PORT)) # Se indica para iniciar la conexión del socket_cliente = cliente_conn(server) asociado a (HOST, PORT) = "addr" del lado de mi servidor
    data = (b"Mensaje de confirmacion") # Por los errores que me saltaban sin "b" calculo que es para que traduzca a bytes mi texto en formato "str" [Un encode rápido]
    socket_cliente.sendall(data) # Por lo visto sí, porque cuando traté de darle tilde en "confirmación" me tiró el error "Non-ASCII character not allowed in bytes string literal" 