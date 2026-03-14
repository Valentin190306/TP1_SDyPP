import threading
import time
import requests
import sys
import os  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT6_NodoC import iniciar_servidor, registrarse_en_D, ruta_log
from HIT6_NodoD import app
from Logger import configurar_logging

HOST_D = "127.0.0.1"
HOST_C = "127.0.0.1"
PORT_D = 8000

puertos = []

def levantar_nodo_c(id):
    nombre_nodo = f"HIT6_NodoC_{id}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit6_nodo_c_{id}.log"))
    puertos[id] = iniciar_servidor(HOST_D, logger)


_servidores_iniciados = False

def arrancar_nodos():
    """Levanta C1 y C2 como servidores en threads daemon (solo una vez)."""
    global _servidores_iniciados
    if _servidores_iniciados:
        return

    t_registry = threading.Thread(target=app.run, kwargs={"host": HOST_D, "port": PORT_D})
    t_registry.daemon = True
    t_registry.start()

    for id in range(1, 3):
        t = threading.Thread(target=levantar_nodo_c, args=(id,), daemon=True)
        t.start()
    
    time.sleep(1)
    _servidores_iniciados = True


def validar_respuesta_json(respuesta):
    """Verifica que la respuesta tenga la estructura esperada."""
    assert isinstance(respuesta, dict), f"Respuesta no es JSON válido: {respuesta}"

    assert "tipo" in respuesta, "Falta campo 'tipo'"
    assert "nodo" in respuesta, "Falta campo 'nodo'"
    assert "mensaje" in respuesta, "Falta campo 'mensaje'"

    assert respuesta["tipo"] == "respuesta", f"Tipo inesperado: {respuesta}"


def recepcion_registro_nodos():
    """Canal rojo: C1 conecta al servidor de C2."""

    for id in range(1, 3):
        nombre_nodo = f"HIT6_NodoC_{id}"
        logger = configurar_logging(nombre_nodo, ruta_log(f"hit6_nodo_c_{id}.log"))
        respuesta = registrarse_en_D(HOST_D, PORT_D, HOST_C, puertos[id], logger)

        assert respuesta is not None, f"C{id} no recibió respuesta de D"
        validar_respuesta_json(respuesta)

        print(f"[OK] Registro recibido en Nodo C{id}: {respuesta}")


def consulta_endpoint_health():
    """Canal verde: consulta el endpoint /health de D."""
    url = f"http://{HOST_D}:{PORT_D}/health"
    try:
        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            print.error(f"Error consultando /health: {r.status_code}")
            return None

        data = r.json()
        print.info(f"Respuesta de /health: {data}")
        return data

    except requests.RequestException as e:
        print.error(f"No se pudo contactar a D: {e}")
        return None
   


if __name__ == "__main__":
    arrancar_nodos()
    
    print("=" * 50)
    print("Test 1: los nodos se registran en D y reciben la lista de nodos existentes")
    recepcion_registro_nodos()

    print("=" * 50)
    print("Test 2: consulta al endpoint health del registry")
    consulta_endpoint_health()

    print("=" * 50)
    print("Todos los tests pasaron OK")