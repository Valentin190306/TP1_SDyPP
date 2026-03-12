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

    print("Primera conexión OK")

    # simulamos caída esperando un poco
    time.sleep(1)

    # segunda conexión (como si el cliente reconectara)
    respuesta2 = cliente_saludar(HOST, PORT, "Hola otra vez")

    assert "Hola otra vez" in respuesta2

    print("Reconexión OK")
    
    
    
if __name__ == "__main__":
    test_reconexion_cliente()
    print("Test de reconexión exitoso")