import socket
import threading
import sys
import os

HOST = "127.0.0.1"
PORT = 5001

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "logs", nombre_archivo)

from Logger import configurar_logging
logger = configurar_logging("HIT3_servidor", ruta_log("hit3_servidor.log"))

def manejar_cliente(conn, addr):

    logger.info(f"Cliente conectado: {addr}")

    try:
        while True:

            data = conn.recv(1024)

            if not data:
                logger.info(f"Cliente {addr} cerró la conexión")
                break

            mensaje = data.decode()
            logger.info(f"{addr} -> {mensaje}")

            respuesta = f"Servidor recibió: {mensaje}"
            conn.sendall(respuesta.encode())

    except (ConnectionResetError, BrokenPipeError):
        logger.warning(f"Cliente {addr} se desconectó abruptamente")

    except OSError as e:
        logger.error(f"Error de socket con {addr}: {e}")

    finally:
        try:
            conn.close()
        except OSError:
            pass

        logger.info(f"Conexión cerrada {addr}")


def iniciar_servidor(HOST="127.0.0.1", PORT=5001):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST, PORT))
        servidor.listen()

        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:

            conn, addr = servidor.accept()

            thread = threading.Thread(
                target=manejar_cliente,
                args=(conn, addr),
                daemon=True
            )

            thread.start()


if __name__ == "__main__":
    iniciar_servidor()