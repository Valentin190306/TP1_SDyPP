import os
import time
import json
import threading
from flask import Flask, request, jsonify

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, nombre_archivo)

from Logger import configurar_logging

logger = configurar_logging(
    nombre_app="NodoD",
    archivo_log=ruta_log("hit7_nodo_d.log")
)

RUTA_NODOS_SUBSCRIPTOS = ruta_log("nodos_subscriptos.json")
RUTA_NODOS_EN_ESPERA = ruta_log("nodos_en_espera.json")

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def rotar_slots():
    global nodos_esperando, nodos_subcriptos

    while True:
        time.sleep(60)

        with nodos_lock:
            nodos_subcriptos |= nodos_esperando
            nodos_esperando = {} 
            
            guardar_json(RUTA_NODOS_EN_ESPERA, nodos_esperando)
            guardar_json(RUTA_NODOS_SUBSCRIPTOS, nodos_subcriptos)

        logger.info("Rotación de ventana ejecutada. Nuevo slot_actual cargado.")


app = Flask(__name__)

# registro en RAM
nodos_esperando = {}
nodos_subcriptos = {}
nodos_lock = threading.Lock()  # para asegurar acceso concurrente seguro a las estructuras de nodos

# tiempo de inicio del servicio
start_time = time.time()


@app.route("/register", methods=["POST"])
def register():

    data = request.json or {}

    ip = data.get("ip")
    puerto = data.get("puerto")

    if not ip or not puerto:
        return jsonify({"error": "ip y puerto requeridos"}), 400

    clave = f"{ip}:{puerto}"

    with nodos_lock:
        # registrar el nodo nuevo
        nodos_esperando[clave] = {
            "ip": ip,
            "puerto": puerto
        }

    logger.info(f"Nuevo nodo registrado en espera: {nodos_esperando[clave]}")
    
    return jsonify({
        "nodos": list(nodos_subcriptos.values())
    })


@app.route("/nodos_subscriptos", methods=["GET"])    
def nodos_subscriptos():
    with nodos_lock:
        return jsonify({"nodos": list(nodos_subcriptos.values())})


@app.route("/health", methods=["GET"])
def health():

    uptime = time.time() - start_time

    logger.info(f"Salud del servicio - Uptime: {uptime}, Nodos en servicio: {len(nodos_esperando)}, Nodos esperando registro: {len(nodos_subcriptos)}")

    with nodos_lock:
        return jsonify({
            "status": "ok",
            "nodos_en_espera": len(nodos_esperando),
            "nodos_registrados": len(nodos_subcriptos),
            "uptime": uptime
        })


def iniciar_servicio():
    guardar_json(RUTA_NODOS_EN_ESPERA, nodos_esperando)
    guardar_json(RUTA_NODOS_SUBSCRIPTOS, nodos_subcriptos)

    rotador = threading.Thread(target=rotar_slots, daemon=True)
    rotador.start()

if __name__ == "__main__":
    iniciar_servicio()
    app.run(host="0.0.0.0", port=8000)

