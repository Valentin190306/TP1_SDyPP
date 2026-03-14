import threading
import time
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT4_NodoC import iniciar_servidor, iniciar_cliente, ruta_log
from Logger import configurar_logging

HOST_C1 = "127.0.0.1"
PORT_C1 = 5001

HOST_C2 = "127.0.0.1"
PORT_C2 = 5002



def make_logger_silencioso(nombre):
    """Logger silencioso para el cliente en tests: no imprime nada en consola."""
    logger = logging.getLogger(f"test_{nombre}")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.NullHandler())
    return logger


def levantar_servidor(host, port):
    """Usa configurar_logging igual que main() para que se genere el archivo de log."""
    nombre_nodo = f"NodoC_{port}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"nodo_c_{port}.log"))
    iniciar_servidor(host, port, logger)


_servidores_iniciados = False

def arrancar_servidores():
    """Levanta C1 y C2 como servidores en threads daemon (solo una vez)."""
    global _servidores_iniciados
    if _servidores_iniciados:
        return
    t1 = threading.Thread(target=levantar_servidor, args=(HOST_C1, PORT_C1), daemon=True)
    t2 = threading.Thread(target=levantar_servidor, args=(HOST_C2, PORT_C2), daemon=True)
    t1.start()
    t2.start()
    time.sleep(1)  # esperar a que ambos bindeen su puerto
    _servidores_iniciados = True


# Tests

def test_c1_saluda_a_c2():
    """Canal rojo del diagrama: C1 conecta al servidor de C2 y recibe respuesta."""
    arrancar_servidores()

    logger = make_logger_silencioso("NodoC_5001")
    respuesta = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)

    assert respuesta is not None, "C1 no recibió respuesta de C2"
    assert "recibí" in respuesta, f"Respuesta inesperada: {respuesta}"
    print("[OK] C1 -> C2")


def test_c2_saluda_a_c1():
    """Canal azul del diagrama: C2 conecta al servidor de C1 y recibe respuesta."""
    arrancar_servidores()

    logger = make_logger_silencioso("NodoC_5002")
    respuesta = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, logger)

    assert respuesta is not None, "C2 no recibió respuesta de C1"
    assert "recibí" in respuesta, f"Respuesta inesperada: {respuesta}"
    print("[OK] C2 -> C1")


def test_ambos_canales_simultaneos():
    """Ambos nodos se saludan al mismo tiempo (escenario real del Hit #4)."""
    arrancar_servidores()

    resultado_c1 = {"respuesta": None}
    resultado_c2 = {"respuesta": None}

    def cliente_c1():
        logger = make_logger_silencioso("NodoC_5001")
        resultado_c1["respuesta"] = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)

    def cliente_c2():
        logger = make_logger_silencioso("NodoC_5002")
        resultado_c2["respuesta"] = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, logger)

    t1 = threading.Thread(target=cliente_c1, daemon=True)
    t2 = threading.Thread(target=cliente_c2, daemon=True)

    t1.start()
    t2.start()
    t1.join(timeout=5)
    t2.join(timeout=5)

    assert resultado_c1["respuesta"] is not None, "C1 no recibió respuesta en canal simultáneo"
    assert resultado_c2["respuesta"] is not None, "C2 no recibió respuesta en canal simultáneo"
    print(f"[OK] Canal simultáneo C1->C2: '{resultado_c1['respuesta']}'")
    print(f"[OK] Canal simultáneo C2->C1: '{resultado_c2['respuesta']}'")


def test_reconexion():
    """
    Simula la caída del cliente: C1 saluda, espera, y vuelve a saludar.
    El servidor de C2 debe seguir funcionando y responder ambas veces.
    """
    arrancar_servidores()

    logger = make_logger_silencioso("NodoC_5001")

    # Primera conexión
    respuesta1 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)
    assert respuesta1 is not None, "Primera conexión falló"
    print(f"[OK] Primera conexión: '{respuesta1}'")

    # Simula caída del cliente (iniciar_cliente ya cerró el socket al terminar)
    time.sleep(1)

    # Segunda conexión: el servidor de C2 debe seguir en pie
    respuesta2 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)
    assert respuesta2 is not None, "Reconexión falló — el servidor no respondió"
    print(f"[OK] Reconexión: '{respuesta2}'")

    time.sleep(0.5)



if __name__ == "__main__":
    print("=" * 50)
    print("Test 1: C1 saluda a C2")
    test_c1_saluda_a_c2()

    print("=" * 50)
    print("Test 2: C2 saluda a C1")
    test_c2_saluda_a_c1()

    print("=" * 50)
    print("Test 3: Ambos canales simultáneos")
    test_ambos_canales_simultaneos()

    print("=" * 50)
    print("Test 4: Reconexión")
    test_reconexion()

    print("=" * 50)
    print("Todos los tests pasaron OK")