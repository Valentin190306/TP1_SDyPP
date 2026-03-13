import os
import time
from flask import Flask, request, jsonify

def ruta_log(nombre_archivo):
    base = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, nombre_archivo)

from Logger import configurar_logging

app = Flask(__name__)

# registro en RAM
nodos = {}

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

    # lista de nodos existentes (antes de agregar el nuevo)
    nodos_existentes = list(nodos.values())

    # registrar el nodo nuevo
    nodos[clave] = {
        "ip": ip,
        "puerto": puerto
    }

    return jsonify({
        "nodos": nodos_existentes
    })


@app.route("/health", methods=["GET"])
def health():

    uptime = time.time() - start_time

    return jsonify({
        "status": "ok",
        "nodos_registrados": len(nodos),
        "uptime": uptime
    })


if __name__ == "__main__":
    logger = configurar_logging(nombre_app="NodoD", archivo_log=ruta_log("hit6_nodo_d.log"))
    logger.info("[NODO D] Servicio de registro iniciado en el puerto 8000")
    app.run(host="0.0.0.0", port=8000)

