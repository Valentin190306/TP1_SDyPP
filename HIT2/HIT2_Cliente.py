# #Fuente: ChatGPT

import socket
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT2_cliente", ruta_log("hit2_cliente.log"))


def cliente_con_reconexion(host="127.0.0.1", port=5001):

    while True:

        try:
            logger.info(f"Intentando conectar a {host}:{port}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

                cliente.connect((host, port))
                logger.info("Conectado al servidor")

                while True:

                    mensaje = input("Mensaje: ")

                    cliente.sendall(mensaje.encode())
                    logger.info(f"Mensaje enviado: {mensaje}")

                    data = cliente.recv(1024)

                    if not data:
                        raise ConnectionError("Servidor cerró la conexión")

                    respuesta = data.decode()

                    logger.info(f"Respuesta recibida: {respuesta}")
                    print(respuesta)

        except Exception as e:

            logger.warning(f"Conexión perdida: {e}")
            logger.info("Reintentando en 3 segundos...")

            time.sleep(3)