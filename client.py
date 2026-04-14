import socket
import threading

# Configuración del servidor al que se conectará el cliente
HOST = "127.0.0.1"   # Dirección del servidor (localhost)
PORT = 6869          # Puerto del servidor

# Función para recibir mensajes del servidor
def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024)                                           # Recibe datos del servidor
            if not mensaje:                                                     # Si no hay datos, el servidor cerró la conexión
                print("Conexión cerrada por el servidor")
                break
            print("\n" + mensaje.decode("utf-8"))                               # Muestra el mensaje recibido
        except ConnectionResetError:
            print("Conexión reiniciada por el servidor")                       # A menos que se presenta un error de conexión
            break
        except OSError as e:                                                    # A menos que se presente un error por Sistema operativo
            print(f"Error de red al recibir: {e}")
            break
        except KeyboardInterrupt:                                               # A menos que se presenta un error por interrupción manual
            print("Cliente detenido manualmente")
            break

# Función principal del cliente
def main():
    try:
        # Crear socket del cliente
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))                                              # Conecta al servidor
        print(f"Conectado al servidor {HOST}:{PORT}")

        # Hilo para escuchar mensajes del servidor en paralelo
        hilo_receptor = threading.Thread(target=recibir_mensajes, args=(sock,))
        hilo_receptor.daemon = True                                             # Se cierra automáticamente al terminar el programa
        hilo_receptor.start()

        # Bucle para enviar mensajes
        while True:
            try:
                mensaje = input("Tú: ")                                         # Captura mensaje del usuario
                if mensaje.lower() == "salir":                                  # Comando para salir
                    print("Cerrando conexión...")
                    sock.close()
                    break
                sock.send(mensaje.encode("utf-8"))                              # Envía mensaje al servidor
            except BrokenPipeError:                                             # A menos de que sea un error de BrokenPipe
                print("Error: conexión rota con el servidor")
                break
            except ConnectionResetError:
                print("Error: el servidor reinició la conexión")
                break
            except OSError as e:
                print(f"Error de red al enviar: {e}")
                break
            except KeyboardInterrupt:
                print("Cliente detenido manualmente")
                sock.close()
                break

    except ConnectionRefusedError:                                              # Mientras no sea rechazado 
        print("No se pudo conectar al servidor (rechazado)")
    except OSError as e:                                    
        print(f"Error al crear socket: {e}")
    except KeyboardInterrupt:
        print("Cliente detenido manualmente")

# Punto de entrada
if __name__ == "__main__":
    main()

