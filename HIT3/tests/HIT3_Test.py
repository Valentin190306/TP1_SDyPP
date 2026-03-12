import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HIT3_Servidor import iniciar_servidor
from HIT3_Cliente import cliente_saludar

HOST = "127.0.0.1"
PORT = 5001


def levantar_servidor():
    iniciar_servidor(HOST, PORT)


def test_reconexion_cliente():

    # levantar servidor en background
    servidor = threading.Thread(target=levantar_servidor, daemon=True)
    servidor.start()

    # esperar a que el servidor arranque
    time.sleep(1)

    # primera conexión
    respuesta1 = cliente_saludar(HOST, PORT, "Hola")

    assert "Hola" in respuesta1
    print("Primera conexión OK")

    # simulamos caída del cliente (simplemente dejamos que termine)
    time.sleep(1)

    # segunda conexión (reconexión)
    respuesta2 = cliente_saludar(HOST, PORT, "Hola otra vez")

    assert "Hola otra vez" in respuesta2
    print("Reconexión OK")

    # pequeño delay para que el servidor procese cierre de sockets
    time.sleep(0.5)


if __name__ == "__main__":
    test_reconexion_cliente()
    print("Test de reconexión exitoso")