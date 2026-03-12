import socket
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT1_cliente", ruta_log("hit1_cliente.log"))

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


if __name__ == "__main__":
    cliente()