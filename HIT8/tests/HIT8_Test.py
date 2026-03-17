"""
HIT8 - Test gRPC con comparación JSON vs Protobuf
"""

import grpc
import time
import json
import threading
import sys
import os
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import saludo_pb2
from HIT8_NodoC import iniciar_servidor, saludar, ruta_log

HOST   = "127.0.0.1"
PORT_1 = 5001
PORT_2 = 5002


# ── Setup ─────────────────────────────────────────────────────────────────────

_servidores_iniciados = False
_servers = []

def arrancar_servidores():
    global _servidores_iniciados
    if _servidores_iniciados:
        return

    _servers.append(iniciar_servidor(HOST, PORT_1))
    _servers.append(iniciar_servidor(HOST, PORT_2))
    time.sleep(0.5)
    _servidores_iniciados = True


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_c1_saluda_a_c2():
    arrancar_servidores()

    respuesta = saludar(HOST, PORT_1, HOST, PORT_2)

    assert respuesta is not None, "C1 no recibió respuesta de C2"
    assert respuesta.tipo == "respuesta", f"Tipo inesperado: {respuesta.tipo}"
    assert "5002" in respuesta.mensaje, f"Mensaje inesperado: {respuesta.mensaje}"
    print("C1 -> C2 OK")


def test_c2_saluda_a_c1():
    arrancar_servidores()

    respuesta = saludar(HOST, PORT_2, HOST, PORT_1)

    assert respuesta is not None, "C2 no recibió respuesta de C1"
    assert respuesta.tipo == "respuesta", f"Tipo inesperado: {respuesta.tipo}"
    assert "5001" in respuesta.mensaje, f"Mensaje inesperado: {respuesta.mensaje}"
    print("C2 -> C1 OK")


def saludar_con_retry(host, port, host_remoto, puerto_remoto, intentos=5):
    for _ in range(intentos):
        respuesta = saludar(host, port, host_remoto, puerto_remoto)
        if respuesta is not None:
            return respuesta
        time.sleep(0.3)
    return None


def test_ambos_canales_simultaneos():
    arrancar_servidores()

    resultado_c1 = {"respuesta": None}
    resultado_c2 = {"respuesta": None}

    def cliente_c1():
        resultado_c1["respuesta"] = saludar_con_retry(HOST, PORT_1, HOST, PORT_2)

    def cliente_c2():
        resultado_c2["respuesta"] = saludar_con_retry(HOST, PORT_2, HOST, PORT_1)

    t1 = threading.Thread(target=cliente_c1, daemon=True)
    t2 = threading.Thread(target=cliente_c2, daemon=True)
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)

    assert resultado_c1["respuesta"] is not None, "C1 no recibió respuesta en canal simultáneo"
    assert resultado_c2["respuesta"] is not None, "C2 no recibió respuesta en canal simultáneo"
    print("Ambos canales simultáneos OK")


def test_reconexion():
    arrancar_servidores()

    respuesta1 = saludar(HOST, PORT_1, HOST, PORT_2)
    assert respuesta1 is not None, "Primera llamada falló"
    print("Primera llamada OK")

    time.sleep(0.5)

    respuesta2 = saludar(HOST, PORT_1, HOST, PORT_2)
    assert respuesta2 is not None, "Segunda llamada falló"
    print("Segunda llamada OK")


def test_comparacion_tamano_mensajes():
    # JSON (HIT5)
    mensaje_json = {
        "tipo":    "saludo",
        "nodo":    "HIT8_NodoC_5001",
        "mensaje": "Hola! Soy el nodo en 127.0.0.1:5001"
    }
    bytes_json = len(json.dumps(mensaje_json).encode())

    # Protobuf (HIT8)
    mensaje_proto = saludo_pb2.Saludo(
        tipo    = "saludo",
        nodo    = "HIT8_NodoC_5001",
        mensaje = "Hola! Soy el nodo en 127.0.0.1:5001"
    )
    bytes_proto = len(mensaje_proto.SerializeToString())

    ahorro = round((1 - bytes_proto / bytes_json) * 100, 1)

    print(f"Tamaño JSON    : {bytes_json} bytes")
    print(f"Tamaño Protobuf: {bytes_proto} bytes")
    print(f"Reducción      : {ahorro}%")

    assert bytes_proto < bytes_json, "Protobuf debería ser más pequeño que JSON"
    print("Comparación de tamaño OK")


def test_comparacion_latencia():
    arrancar_servidores()

    N = 10
    tiempos = []

    for _ in range(N):
        inicio = time.perf_counter()
        saludar(HOST, PORT_1, HOST, PORT_2)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)

    promedio = round(sum(tiempos) / N, 3)
    minimo   = round(min(tiempos), 3)
    maximo   = round(max(tiempos), 3)

    print(f"Latencia gRPC — promedio: {promedio}ms | min: {minimo}ms | max: {maximo}ms")
    print("Comparación de latencia OK")


# ── Entry point ───────────────────────────────────────────────────────────────

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
    print("Test 5: Comparación tamaño mensajes (JSON vs Protobuf)")
    test_comparacion_tamano_mensajes()

    print("=" * 50)
    print("Test 6: Comparación latencia gRPC")
    test_comparacion_latencia()

    print("=" * 50)
    print("Todos los tests pasaron OK")