# tcp_app.py
import socket

def iniciar_servidor(host="127.0.0.1", port=5000):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(1)

    conn, addr = servidor.accept()
    with conn:
        mensaje = conn.recv(1024).decode()
        respuesta = f"B recibió: {mensaje}"
        conn.sendall(respuesta.encode())

    servidor.close()


def cliente_saludar(host="127.0.0.1", port=5000, saludo="Hola B"):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))

    cliente.sendall(saludo.encode())
    respuesta = cliente.recv(1024).decode()

    cliente.close()
    return respuesta