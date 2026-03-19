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

RUTA_SIG_SLOT = ruta_log("sig_slot.json")
RUTA_SLOT_ACTUAL = ruta_log("slot_actual.json")

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
    global slot_actual, sig_slot

    while True:
        time.sleep(60)

        slot_actual = sig_slot
        sig_slot = {}

        guardar_json(RUTA_SLOT_ACTUAL, slot_actual)
        guardar_json(RUTA_SIG_SLOT, sig_slot)

        logger.info("Rotación de ventana ejecutada. Nuevo slot_actual cargado.")

app = Flask(__name__)

# registro en RAM
slot_actual = {}
sig_slot = {}

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

    # registrar el nodo nuevo
    sig_slot[clave] = {
        "ip": ip,
        "puerto": puerto
    }

    logger.info(f"Nuevo nodo registrado: {sig_slot[clave]}")

    return jsonify({
        "nodos": list(slot_actual.values())
    })
    

@app.route("/health", methods=["GET"])
def health():

    uptime = time.time() - start_time

    logger.info(f"Salud del servicio - Uptime: {uptime}, Nodos en servicio: {len(slot_actual)}, Nodos esperando registro: {len(sig_slot)}")

    return jsonify({
        "status": "ok",
        "nodos_registrados_actual": len(slot_actual),
        "nodos_registrados_siguiente": len(sig_slot),
        "uptime": uptime
    })

def iniciar_servicio():
    guardar_json(RUTA_SLOT_ACTUAL, slot_actual)
    guardar_json(RUTA_SIG_SLOT, sig_slot)

    rotador = threading.Thread(target=rotar_slots, daemon=True)
    rotador.start()

if __name__ == "__main__":
    iniciar_servicio()
    app.run(host="0.0.0.0", port=8000)

