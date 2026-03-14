import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT4_NodoC import iniciar_servidor, iniciar_cliente

HOST_C1 = "127.0.0.1"
PORT_C1 = 5001

HOST_C2 = "127.0.0.1"
PORT_C2 = 5002
 

import logging

# creo un log nulo para pasarlo por parametro porque las funciones lo piden

def _logger_nulo(nombre):
    """Logger interno sin handlers: no imprime ni loguea nada."""
    logger = logging.getLogger(f"test_{nombre}")
    logger.addHandler(logging.NullHandler())
    return logger


_servidores_iniciados = False

def levantar_servidores():
    global _servidores_iniciados
    if _servidores_iniciados:
        return

    from HIT4_NodoC import ruta_log
    from Logger import configurar_logging

    def _srv(host, port):
        nombre = f"NodoC_{port}"
        logger = configurar_logging(nombre, ruta_log(f"nodo_c_{port}.log"))
        iniciar_servidor(host, port, logger)

    threading.Thread(target=_srv, args=(HOST_C1, PORT_C1), daemon=True).start()
    threading.Thread(target=_srv, args=(HOST_C2, PORT_C2), daemon=True).start()
    time.sleep(1)
    _servidores_iniciados = True


# Tests 

def test_c1_saluda_a_c2():
    levantar_servidores()

    respuesta = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, _logger_nulo("c1"))

    assert respuesta is not None, "C1 no recibió respuesta de C2"
    assert "recibí" in respuesta, f"Respuesta inesperada: {respuesta}"
    print("C1 -> C2 OK")


def test_c2_saluda_a_c1():
    levantar_servidores()

    respuesta = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, _logger_nulo("c2"))

    assert respuesta is not None, "C2 no recibió respuesta de C1"
    assert "recibí" in respuesta, f"Respuesta inesperada: {respuesta}"
    print("C2 -> C1 OK")


def test_ambos_canales_simultaneos():
    levantar_servidores()

    resultado_c1 = {"respuesta": None}
    resultado_c2 = {"respuesta": None}

    def cliente_c1():
        resultado_c1["respuesta"] = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, _logger_nulo("c1"))

    def cliente_c2():
        resultado_c2["respuesta"] = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, _logger_nulo("c2"))

    t1 = threading.Thread(target=cliente_c1, daemon=True)
    t2 = threading.Thread(target=cliente_c2, daemon=True)
    t1.start()
    t2.start()
    t1.join(timeout=5)
    t2.join(timeout=5)

    assert resultado_c1["respuesta"] is not None, "C1 no recibió respuesta en canal simultáneo"
    assert resultado_c2["respuesta"] is not None, "C2 no recibió respuesta en canal simultáneo"
    print("Ambos canales simultáneos OK")


def test_reconexion():
    levantar_servidores()

    # Primera conexión
    respuesta1 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, _logger_nulo("c1"))
    assert respuesta1 is not None, "Primera conexión falló"
    print("Primera conexión OK")

    # Simula caída del cliente (iniciar_cliente ya cerró el socket al terminar)
    time.sleep(1)

    # Segunda conexión: el servidor de C2 debe seguir en pie
    respuesta2 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, _logger_nulo("c1"))
    assert respuesta2 is not None, "Reconexión falló — el servidor no respondió"
    print("Reconexión OK")

    time.sleep(0.5)


if __name__ == "__main__":
    test_c1_saluda_a_c2()
    test_c2_saluda_a_c1()
    test_ambos_canales_simultaneos()
    test_reconexion()
    print("Todos los tests pasaron OK")