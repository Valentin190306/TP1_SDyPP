# test_tcp.py

import sys
import os
import unittest
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from HIT1_Cliente import cliente_saludar
from HIT1_Servidor import iniciar_servidor


class TestTCP(unittest.TestCase):

    def test_comunicacion_cliente_servidor(self):
        servidor_thread = threading.Thread(
            target=iniciar_servidor,
            kwargs={"host": "127.0.0.1", "port": 5001}
        )

        servidor_thread.start()

        # pequeño delay para que el servidor arranque
        time.sleep(0.5)

        respuesta = cliente_saludar("127.0.0.1", 5001, "Hola B")

        self.assertEqual(respuesta, "B recibió: Hola B")

        servidor_thread.join()


if __name__ == "__main__":
    unittest.main()