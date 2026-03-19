import threading
import time
import requests
import sys
import os  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT7_NodoC import iniciar_servidor, registrarse_en_D, ruta_log
from HIT7_NodoD import app, iniciar_servicio
from Logger import configurar_logging

HOST_D = "127.0.0.1"
HOST_C = "127.0.0.1"
PORT_D = 8000

puertos = {}

def levantar_nodo_c(id):
    nombre_nodo = f"HIT7_NodoC_{id}"
    logger = configurar_logging(nombre_nodo, ruta_log(f"hit7_nodo_c_{id}.log"))
    puertos[id] = iniciar_servidor(HOST_D, logger)


_servidores_iniciados = False

def esperar_registry():
    for _ in range(20):
        try:
            r = requests.get(f"http://{HOST_D}:{PORT_D}/health", timeout=1)
            if r.status_code == 200:
                return
        except:
            pass
        time.sleep(0.2)

def arrancar_nodos():
    """Levanta C1 y C2 como servidores en threads daemon (solo una vez)."""
    global _servidores_iniciados
    if _servidores_iniciados:
        return

    iniciar_servicio()

    t_registry = threading.Thread(
        target=app.run,
        kwargs={"host": HOST_D, "port": PORT_D},
        daemon=True
    )
    t_registry.start()

    for id in range(1, 4):
        t = threading.Thread(target=levantar_nodo_c, args=(id,), daemon=True)
        t.start()
    
    time.sleep(1)
    _servidores_iniciados = True


def validar_respuesta_json(respuesta):
    assert isinstance(respuesta, dict), f"Respuesta no es JSON válido: {respuesta}"

    assert "nodos" in respuesta, "Falta campo 'nodos'"
    assert isinstance(respuesta["nodos"], list), "El campo 'nodos' debe ser una lista"


def test_recepcion_registro_nodos():
    for id in range(1, 4):
        
        if (id == 3):
            print("[INFO] esperando rotación para que C3 se registre en la siguiente ventana...")
            time.sleep(65)
        
        nombre_nodo = f"HIT7_NodoC_{id}"
        logger = configurar_logging(nombre_nodo, ruta_log(f"hit7_nodo_c_{id}.log"))

        respuesta = registrarse_en_D(HOST_D, PORT_D, HOST_C, puertos[id], logger)

        assert respuesta is not None, f"C{id} no recibió respuesta de D"

        validar_respuesta_json(respuesta)

        print(f"[OK] Registro recibido en Nodo C{id}: {respuesta}")

    nodos = respuesta["nodos"]
    
    assert len(nodos) == 2, f"Esperaba 2 nodos registrados en D, pero recibí {len(nodos)}"



if __name__ == "__main__":
    esperar_registry()
    arrancar_nodos()
    
    print("=" * 50)
    print("Test: los nodos se registran en D en diferentes ventanas y reciben la lista de nodos registrados correctamente")
    test_recepcion_registro_nodos()

    print("=" * 50)
    print("Todos los tests pasaron OK")