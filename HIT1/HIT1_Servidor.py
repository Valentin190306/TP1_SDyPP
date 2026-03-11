# #Fuente: ChatGPT

import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Logger import configurar_logging
logger = configurar_logging("HIT1_servidor", "hit1_servidor.log")

def iniciar_servidor(host="127.0.0.1", port=5001):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.bind((host, port))
        servidor.listen()

        logger.info(f"Servidor iniciado en {host}:{port}")

        conn, addr = servidor.accept()

        with conn:
            logger.info(f"Cliente conectado desde {addr}")

            mensaje = conn.recv(1024).decode()
            logger.info(f"Mensaje recibido: {mensaje}")

            respuesta = f"B recibió: {mensaje}"

            conn.sendall(respuesta.encode())

            logger.info("Respuesta enviada al cliente")