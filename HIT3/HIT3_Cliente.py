import socket
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT3_cliente", ruta_log("hit3_cliente.log"))

HOST = "127.0.0.1"
PORT = 5001


def conectar():

    while True:

        try:

            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))

            logger.info("Conectado al servidor")

            return cliente

        except ConnectionRefusedError:

            logger.warning("Servidor no disponible, reintentando...")
            time.sleep(2)


def cliente():

    cliente = conectar()

    while True:

        try:

            mensaje = input("Mensaje: ")

            cliente.sendall(mensaje.encode())

            respuesta = cliente.recv(1024)

            if not respuesta:
                raise ConnectionResetError

            logger.info("Servidor: %s", respuesta.decode())

        except (ConnectionResetError, BrokenPipeError):

            logger.error("Conexión perdida. Reconectando...")

            cliente.close()
            cliente = conectar()

def cliente_saludar(host, port, mensaje):

    logger.info(f"Intentando conectar a {host}:{port}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

            cliente.connect((host, port))
            logger.info("Conexión establecida con el servidor")

            logger.info(f"Enviando mensaje: {mensaje}")
            cliente.sendall(mensaje.encode())

            respuesta = cliente.recv(1024).decode()

            logger.info(f"Respuesta recibida del servidor: {respuesta}")

            return respuesta

    except ConnectionRefusedError:
        logger.error("No se pudo conectar al servidor")
        raise

    except Exception as e:
        logger.error(f"Error durante la comunicación: {e}")
        raise


if __name__ == "__main__":
    cliente()