import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from HIT2_Servidor import iniciar_servidor
from HIT2_Cliente import cliente_saludar

HOST = "127.0.0.1"
PORT = 5001


def levantar_servidor():
    iniciar_servidor(HOST, PORT)


def test_reconexion_cliente():

    # levantar servidor
    servidor = threading.Thread(target=levantar_servidor, daemon=True)
    servidor.start()

    time.sleep(1)

    # primera conexión
    respuesta1 = cliente_saludar(HOST, PORT, "Hola")

    assert "Hola" in respuesta1

    # simulamos caída del servidor
    # si el servidor acepta solo una conexión, termina solo
    servidor.join(timeout=1)

    time.sleep(1)

    # levantar servidor nuevamente
    servidor2 = threading.Thread(target=levantar_servidor, daemon=True)
    servidor2.start()

    time.sleep(1)

    # el cliente debe reconectar
    respuesta2 = cliente_saludar(HOST, PORT, "Hola otra vez")

    assert "Hola otra vez" in respuesta2
    
if __name__ == "__main__":
    test_reconexion_cliente()
    print("Test de reconexión exitoso")