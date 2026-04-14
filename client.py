import socket
import threading

# Configuración del servidor al que se conectará el cliente
HOST = "127.0.0.1"   # Dirección del servidor (localhost)
PORT = 6869          # Puerto del servidor

# Función para recibir mensajes del servidor
def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024)                                   # Recibe datos del servidor
            if not mensaje:                                             # Si no hay datos, el servidor cerró la conexión
                print("Conexión cerrada por el servidor.")
                break
            print("\n" + mensaje.decode("utf-8"))                       # Muestra el mensaje recibido
        except ConnectionResetError:
            print("Conexión reiniciada por el servidor.")               # A menos que se presenta un error de conexión
            break
        except OSError as e:                                            # A menos que se presente un error por Sistema operativo
            print(f"Error de red al recibir: {e}")
            break
        except KeyboardInterrupt:                                       # A menos que se presenta un error por interrupción manual
            print("Cliente detenido manualmente.")
            break


