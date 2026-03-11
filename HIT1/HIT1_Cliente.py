# #Fuente: ChatGPT

import socket

from Logger import configurar_logging
logger = configurar_logging("HIT1_cliente", "hit1_cliente.log")

def cliente_saludar(host, port, mensaje):

     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        logger.info(f"Intentando conectar a {host}:{port}")

        cliente.connect((host, port))

        logger.info(f"Enviando mensaje: {mensaje}")

        cliente.sendall(mensaje.encode())

        respuesta = cliente.recv(1024).decode()

        logger.info(f"Respuesta recibida: {respuesta}")

        return respuesta