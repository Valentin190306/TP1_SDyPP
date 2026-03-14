import socket
import threading
import time
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(file):
    base = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, file)

from Logger import configurar_logging

# Servidor: escucha y responde saludos entrantes

def manejar_cliente(conn, addr, logger, host, port):
    logger.info(f"[SERVIDOR] Cliente conectado: {addr}")

    try:
        data = conn.recv(1024)

        if data:
            mensaje_json = json.loads(data.decode())

            logger.info(f"[SERVIDOR] JSON recibido: {mensaje_json}")

            respuesta = {
                "tipo": "respuesta",
                "nodo": logger.name,
                "mensaje": f"Hola {mensaje_json['nodo']}, soy el nodo en {host}:{port} y recibí tu saludo"
            }

            conn.sendall(json.dumps(respuesta).encode())

    except (ConnectionResetError, BrokenPipeError):
        logger.warning(f"[SERVIDOR] Cliente {addr} se desconectó abruptamente")

    except OSError as e:
        logger.error(f"[SERVIDOR] Error de socket con {addr}: {e}")

    finally:
        try:
            conn.close()
        except OSError:
            pass
        logger.info(f"[SERVIDOR] Conexión cerrada con {addr}")


def iniciar_servidor(host, port, logger):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, port))
        servidor.listen()

        logger.info(f"[SERVIDOR] Escuchando en {host}:{port}")
        print(f"[SERVIDOR] Escuchando en {host}:{port}")

        while True:
            try:
                conn, addr = servidor.accept()
                thread = threading.Thread(
                    target=manejar_cliente,
                    args=(conn, addr, logger, host, port),
                    daemon=True
                )
                thread.start()

            except OSError as e:
                logger.error(f"[SERVIDOR] Error en accept(): {e}")


# Cliente: conecta y manda saludo automáticamente

def conectar(remote_host, remote_port, logger):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((remote_host, remote_port))
            logger.info(f"[CLIENTE] Conectado a {remote_host}:{remote_port}")
            return sock

        except ConnectionRefusedError:
            logger.warning(f"[CLIENTE] {remote_host}:{remote_port} no disponible, reintentando en 2s...")
            time.sleep(2)


def iniciar_cliente(host, port, remote_host, remote_port, logger):
    sock = conectar(remote_host, remote_port, logger)

    respuesta_json = None

    try:
        # Construir mensaje JSON
        mensaje = {
            "tipo": "saludo",
            "nodo": logger.name,
            "mensaje": f"Hola! Soy el nodo en {host}:{port}"
        }

        # Serializar a JSON y enviar
        sock.sendall(json.dumps(mensaje).encode())

        logger.info(f"[CLIENTE] Saludo enviado: {mensaje}")
        print(f"[CLIENTE] Saludo enviado a {remote_host}:{remote_port}: {mensaje}")

        # Esperar respuesta
        respuesta = sock.recv(1024)

        if respuesta:
            respuesta_json = json.loads(respuesta.decode())

            logger.info(f"[CLIENTE] Respuesta recibida: {respuesta_json}")
            print(f"[CLIENTE] Respuesta de {remote_host}:{remote_port}: {respuesta_json}")

    except (ConnectionResetError, BrokenPipeError):
        logger.error("[CLIENTE] Conexión perdida al saludar")

    except OSError as e:
        logger.error(f"[CLIENTE] Error de red: {e}")

    finally:
        sock.close()

    return respuesta_json


def main():
    if len(sys.argv) != 5:
        print("Uso: python nodo_c.py <mi_host> <mi_puerto> <host_remoto> <puerto_remoto>")
        print("Ejemplo:")
        print("  Terminal 1: python nodo_c.py 127.0.0.1 5001 127.0.0.1 5002")
        print("  Terminal 2: python nodo_c.py 127.0.0.1 5002 127.0.0.1 5001")
        sys.exit(1)

    mi_host       = sys.argv[1]
    mi_puerto     = int(sys.argv[2])
    host_remoto   = sys.argv[3]
    puerto_remoto = int(sys.argv[4])

    nombre_nodo = f"HIT5_NodoC_{mi_puerto}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{mi_puerto}.log"))

    logger.info(f"Iniciando nodo {nombre_nodo}")

    # Thread del servidor: escucha conexiones entrantes
    hilo_servidor = threading.Thread(
        target=iniciar_servidor,
        args=(mi_host, mi_puerto, logger),
        daemon=True,
        name=f"{nombre_nodo}-servidor"
    )
    hilo_servidor.start()

    # Pequeña espera para que ambos servidores estén listos antes de conectar
    time.sleep(1)

    # Thread del cliente: conecta, saluda y termina
    hilo_cliente = threading.Thread(
        target=iniciar_cliente,
        args=(mi_host, mi_puerto, host_remoto, puerto_remoto, logger),
        daemon=True,
        name=f"{nombre_nodo}-cliente"
    )
    hilo_cliente.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"Nodo {nombre_nodo} apagado por el usuario")
        print(f"\nNodo {nombre_nodo} apagado.")


if __name__ == "__main__":
    main()