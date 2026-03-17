"""
HIT8 - Nodo C con gRPC + Protocol Buffers
Reemplaza la comunicación JSON/TCP del HIT5

Uso:
    Terminal 1: python3 HIT8_NodoC.py 127.0.0.1 5001 127.0.0.1 5002
    Terminal 2: python3 HIT8_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
"""

import grpc
import time
import threading
import sys
import os
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import saludo_pb2
import saludo_pb2_grpc

def ruta_log(file):
    base = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, file)

from Logger import configurar_logging


# ── Servidor gRPC ─────────────────────────────────────────────────────────────

class NodoServicer(saludo_pb2_grpc.NodoServiceServicer):

    def __init__(self, host, port):
        self.host   = host
        self.port   = port
        # Cada instancia del servidor tiene su propio logger con su propio archivo
        self.logger = configurar_logging(
            f"HIT8_NodoC_{port}",
            ruta_log(f"hit8_nodo_c_{port}.log")
        )

    def Saludar(self, request, context):
        self.logger.info(f"[SERVIDOR] Saludo recibido de {request.nodo}: '{request.mensaje}'")

        respuesta = saludo_pb2.Respuesta(
            tipo    = "respuesta",
            nodo    = self.logger.name,
            mensaje = f"Hola {request.nodo}, soy el nodo en {self.host}:{self.port} y recibí tu saludo"
        )

        self.logger.info(f"[SERVIDOR] Respuesta enviada a {request.nodo}")
        return respuesta


def iniciar_servidor(host, port):
    """Levanta el servidor gRPC. El logger se configura internamente por puerto."""
    servicer = NodoServicer(host, port)
    server   = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_pb2_grpc.add_NodoServiceServicer_to_server(servicer, server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    servicer.logger.info(f"[SERVIDOR] Escuchando en {host}:{port}")
    return server


# ── Cliente gRPC ──────────────────────────────────────────────────────────────

def saludar(host, port, host_remoto, puerto_remoto):
    """Envía un saludo gRPC al nodo remoto. El logger se configura internamente por puerto."""
    logger = configurar_logging(
        f"HIT8_NodoC_{port}",
        ruta_log(f"hit8_nodo_c_{port}.log")
    )

    canal = grpc.insecure_channel(f"{host_remoto}:{puerto_remoto}")
    stub  = saludo_pb2_grpc.NodoServiceStub(canal)

    mensaje = saludo_pb2.Saludo(
        tipo    = "saludo",
        nodo    = logger.name,
        mensaje = f"Hola! Soy el nodo en {host}:{port}"
    )

    try:
        logger.info(f"[CLIENTE] Enviando saludo a {host_remoto}:{puerto_remoto}")
        respuesta = stub.Saludar(mensaje)
        logger.info(f"[CLIENTE] Respuesta recibida de {host_remoto}:{puerto_remoto}: '{respuesta.mensaje}'")
        return respuesta

    except grpc.RpcError as e:
        logger.error(f"[CLIENTE] Error gRPC: {e.code()} - {e.details()}")
        return None

    finally:
        canal.close()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 5:
        print("Uso: python3 HIT8_NodoC.py <mi_host> <mi_puerto> <host_remoto> <puerto_remoto>")
        sys.exit(1)

    mi_host       = sys.argv[1]
    mi_puerto     = int(sys.argv[2])
    host_remoto   = sys.argv[3]
    puerto_remoto = int(sys.argv[4])

    logger = configurar_logging(
        f"HIT8_NodoC_{mi_puerto}",
        ruta_log(f"hit8_nodo_c_{mi_puerto}.log")
    )
    logger.info(f"Iniciando nodo HIT8_NodoC_{mi_puerto}")

    server = iniciar_servidor(mi_host, mi_puerto)

    time.sleep(1)

    threading.Thread(
        target=saludar,
        args=(mi_host, mi_puerto, host_remoto, puerto_remoto),
        daemon=True,
        name=f"HIT8_NodoC_{mi_puerto}-cliente"
    ).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"Nodo HIT8_NodoC_{mi_puerto} apagado por el usuario")
        server.stop(0)
        print(f"\nNodo HIT8_NodoC_{mi_puerto} apagado.")


if __name__ == "__main__":
    main()