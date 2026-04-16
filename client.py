import socket    # Para conectarse al servidor
import threading # Para hacer dos cosas a la vez: escribir y escuchar
import sys       # Para la salida de la terminal (limpiar líneas)

# Configuración
HOST = "127.0.0.1"
PORT = 6869

# Función que establece un hilo secundario "corriendo" siempre escuchando al servidor
def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024) # Se queda esperando recibir algo del servidor
            if not mensaje: # Si el servidor se apaga, recibiremos un paquete vacío
                print("\nConexión cerrada por el servidor.")
                break
            sys.stdout.write(f"\r{mensaje.decode('utf-8')}\nTú: ") # \r mueve el cursor al inicio de la línea
            sys.stdout.flush() # Fuerza a la terminal a mostrar el texto directo
        except: # Cualquier error de red rompe el bucle de recepción
            break
    print("Hilo de recepción terminado.")

# Hilo principal donde se maneja la conexión y el envío de mensajes
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket del cliente (TCP)
    try:
        sock.connect((HOST, PORT)) # Intenta conectar al servidor
        print(f"Conectado al servidor {HOST}:{PORT}")
        hilo_receptor = threading.Thread(target=recibir_mensajes, args=(sock,)) # Crea un hilo paralelo para ejecutar la función 'recibir_mensajes'
        hilo_receptor.daemon = True # Daemon=True hace que el hilo muera automáticamente si el programa principal se cierra
        hilo_receptor.start()

        # Bucle principal de interacción
        while True:
            mensaje = input("Tú: ") # Se queda pausado esperando que el usuario escriba algo
            if mensaje.lower() == "salir": # Si el usuario escribe 'salir', rompemos el bucle
                break
            if mensaje: # Solo enviamos si el mensaje tiene contenido
                try:
                    sock.sendall(mensaje.encode("utf-8")) # Codifica a UTF-8 y envía todo el contenido
                except (BrokenPipeError, ConnectionResetError):
                    print("Error: Se perdió la conexión con el servidor.")
                    break
    except ConnectionRefusedError:
        # Error si el servidor no está encendido o el puerto está cerrado
        print("No se pudo conectar: Servidor fuera de línea.")
    except KeyboardInterrupt:
        # Salida limpia con Ctrl+C
        print("\nSaliendo...")
    finally:
        # Asegura que el socket se cierre al terminar el programa
        sock.close()
        print("Socket del cliente cerrado.")

if __name__ == "__main__":
    main()