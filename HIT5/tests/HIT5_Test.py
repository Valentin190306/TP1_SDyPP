import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT5_NodoC import iniciar_servidor, iniciar_cliente, ruta_log
from Logger import configurar_logging

HOST_C1 = "127.0.0.1"
PORT_C1 = 5001

HOST_C2 = "127.0.0.1"
PORT_C2 = 5002



def levantar_servidor(host, port):
    nombre_nodo = f"HIT5_NodoC_{port}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{port}.log"))
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

    time.sleep(1)
    _servidores_iniciados = True



def validar_respuesta_json(respuesta):
    """Verifica que la respuesta tenga la estructura esperada."""
    assert isinstance(respuesta, dict), f"Respuesta no es JSON válido: {respuesta}"

    assert "tipo" in respuesta, "Falta campo 'tipo'"
    assert "nodo" in respuesta, "Falta campo 'nodo'"
    assert "mensaje" in respuesta, "Falta campo 'mensaje'"

    assert respuesta["tipo"] == "respuesta", f"Tipo inesperado: {respuesta}"


def test_c1_saluda_a_c2():
    """Canal rojo: C1 conecta al servidor de C2."""
    arrancar_servidores()

    nombre_nodo = f"HIT5_NodoC_{PORT_C1}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{PORT_C1}.log"))
    respuesta = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)

    assert respuesta is not None, "C1 no recibió respuesta de C2"
    validar_respuesta_json(respuesta)

    print(f"[OK] C1 -> C2: {respuesta}")


def test_c2_saluda_a_c1():
    """Canal azul: C2 conecta al servidor de C1."""
    arrancar_servidores()

    nombre_nodo = f"HIT5_NodoC_{PORT_C2}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{PORT_C2}.log"))
    respuesta = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, logger)

    assert respuesta is not None, "C2 no recibió respuesta de C1"
    validar_respuesta_json(respuesta)

    print(f"[OK] C2 -> C1: {respuesta}")


def test_ambos_canales_simultaneos():
    """Ambos nodos se saludan simultáneamente."""
    arrancar_servidores()

    resultado_c1 = {"respuesta": None}
    resultado_c2 = {"respuesta": None}

    def cliente_c1():
        nombre_nodo = f"HIT5_NodoC_{PORT_C1}"
        logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{PORT_C1}.log"))
        resultado_c1["respuesta"] = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)

    def cliente_c2():
        nombre_nodo = f"HIT5_NodoC_{PORT_C2}"
        logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{PORT_C2}.log"))
        resultado_c2["respuesta"] = iniciar_cliente(HOST_C2, PORT_C2, HOST_C1, PORT_C1, logger)

    t1 = threading.Thread(target=cliente_c1, daemon=True)
    t2 = threading.Thread(target=cliente_c2, daemon=True)

    t1.start()
    t2.start()

    t1.join(timeout=5)
    t2.join(timeout=5)

    assert resultado_c1["respuesta"] is not None, "C1 no recibió respuesta"
    assert resultado_c2["respuesta"] is not None, "C2 no recibió respuesta"

    validar_respuesta_json(resultado_c1["respuesta"])
    validar_respuesta_json(resultado_c2["respuesta"])

    print(f"[OK] Canal simultáneo C1->C2: {resultado_c1['respuesta']}")
    print(f"[OK] Canal simultáneo C2->C1: {resultado_c2['respuesta']}")


def test_reconexion():
    """
    Simula caída del cliente y reconexión.
    """
    arrancar_servidores()

    nombre_nodo = f"HIT5_NodoC_{PORT_C1}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit5_nodo_c_{PORT_C1}.log"))

    respuesta1 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)
    assert respuesta1 is not None, "Primera conexión falló"
    validar_respuesta_json(respuesta1)

    print(f"[OK] Primera conexión: {respuesta1}")

    time.sleep(1)

    respuesta2 = iniciar_cliente(HOST_C1, PORT_C1, HOST_C2, PORT_C2, logger)
    assert respuesta2 is not None, "Reconexión falló"
    validar_respuesta_json(respuesta2)

    print(f"[OK] Reconexión: {respuesta2}")

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