# #Fuente: ChatGPT
import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT2_servidor", ruta_log("hit2_servidor.log"))


def iniciar_servidor(host="127.0.0.1", port=5001):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, port))
        servidor.listen()

        logger.info(f"Servidor iniciado en {host}:{port}")

        while True:

            conn, addr = servidor.accept()
            logger.info(f"Cliente conectado desde {addr}")

            try:
                with conn:
                    while True:

                        data = conn.recv(1024)

                        if not data:
                            logger.info("Cliente desconectado")
                            break

                        mensaje = data.decode()
                        logger.info(f"Mensaje recibido: {mensaje}")

                        respuesta = f"B recibió: {mensaje}"

                        conn.sendall(respuesta.encode())
                        logger.info("Respuesta enviada")

            except Exception as e:
                logger.error(f"Error durante la conexión: {e}")