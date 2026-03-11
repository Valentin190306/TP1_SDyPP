# #Fuente: ChatGPT

import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT1_cliente", ruta_log("hit1_cliente.log"))

def cliente_saludar(host, port, mensaje):

     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        logger.info(f"Intentando conectar a {host}:{port}")

        cliente.connect((host, port))

        logger.info(f"Enviando mensaje: {mensaje}")

        cliente.sendall(mensaje.encode())

        respuesta = cliente.recv(1024).decode()

        logger.info(f"Respuesta recibida: {respuesta}")

        return respuesta
     
