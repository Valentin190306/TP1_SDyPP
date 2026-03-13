import socket
import threading
import time
import sys
import os
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, nombre_archivo)

from Logger import configurar_logging


# ---------------- SERVIDOR ----------------

def manejar_cliente(conn, addr, logger):
    logger.info(f"[SERVIDOR] Cliente conectado: {addr}")

    try:
        data = conn.recv(1024)

        if data:
            mensaje_json = json.loads(data.decode())

            logger.info(f"[SERVIDOR] JSON recibido: {mensaje_json}")

            respuesta = {
                "tipo": "respuesta",
                "nodo": logger.name,
                "mensaje": f"Hola {mensaje_json['nodo']}, recibí tu saludo"
            }

            conn.sendall(json.dumps(respuesta).encode())

    finally:
        conn.close()
        logger.info(f"[SERVIDOR] Conexión cerrada con {addr}")


def iniciar_servidor(host, logger):

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # puerto aleatorio
    servidor.bind((host, 0))
    puerto = servidor.getsockname()[1]

    servidor.listen()

    logger.info(f"[SERVIDOR] Escuchando en {host}:{puerto}")
    print(f"[SERVIDOR] Escuchando en {host}:{puerto}")

    def aceptar():
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(
                target=manejar_cliente,
                args=(conn, addr, logger),
                daemon=True
            )
            thread.start()

    threading.Thread(target=aceptar, daemon=True).start()

    return puerto


# ---------------- CLIENTE ----------------

def conectar(host_remoto, puerto_remoto, logger):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_remoto, puerto_remoto))
        logger.info(f"[CLIENTE] Conectado a {host_remoto}:{puerto_remoto}")
        return sock

    except ConnectionRefusedError:
        logger.warning(f"[CLIENTE] {host_remoto}:{puerto_remoto} no disponible")
        return None


def saludar(host_remoto, puerto_remoto, logger):

    sock = conectar(host_remoto, puerto_remoto, logger)

    if not sock:
        return

    try:
        mensaje = {
            "tipo": "saludo",
            "nodo": logger.name,
            "mensaje": "Hola!"
        }

        sock.sendall(json.dumps(mensaje).encode())

        logger.info(f"[CLIENTE] Saludo enviado a {host_remoto}:{puerto_remoto}")

        respuesta = sock.recv(1024)

        if respuesta:
            respuesta_json = json.loads(respuesta.decode())
            logger.info(f"[CLIENTE] Respuesta recibida: {respuesta_json}")
            print(f"[CLIENTE] Respuesta de {host_remoto}:{puerto_remoto}: {respuesta_json}")

    finally:
        sock.close()


# ---------------- REGISTRY ----------------

def registrarse_en_D(host_D, puerto_D, mi_ip, mi_puerto, logger):

    url = f"http://{host_D}:{puerto_D}/register"

    payload = {
        "ip": mi_ip,
        "puerto": mi_puerto
    }

    try:
        r = requests.post(url, json=payload)

        if r.status_code != 200:
            logger.error(f"Error registrándose en D: {r.status_code}")
            return []

        data = r.json()

        logger.info(f"Nodos recibidos del registry: {data}")

        return data.get("nodos", [])

    except requests.RequestException as e:
        logger.error(f"No se pudo contactar a D: {e}")
        return []


# ---------------- MAIN ----------------

def main():

    if len(sys.argv) != 3:
        print("Uso: python nodo_c.py <ip_registry_D> <puerto_registry_D>")
        sys.exit(1)

    host_D = sys.argv[1]
    puerto_D = int(sys.argv[2])

    mi_host = "127.0.0.1"

    logger = configurar_logging("NodoC", ruta_log("nodo_c.log"))

    # iniciar servidor en puerto aleatorio
    mi_puerto = iniciar_servidor(mi_host, logger)

    time.sleep(1)

    # registrarse en D
    nodos = registrarse_en_D(host_D, puerto_D, mi_host, mi_puerto, logger)

    # conectarse a todos los nodos existentes
    for nodo in nodos:
        if (nodo["ip"] == mi_host and nodo["puerto"] == mi_puerto):
            continue

        host = nodo["ip"]
        puerto = nodo["puerto"]

        threading.Thread(
            target=saludar,
            args=(host, puerto, logger),
            daemon=True
        ).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Nodo C detenido")


if __name__ == "__main__":
    main()