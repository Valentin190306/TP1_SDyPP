# #Fuente: ChatGPT

import socket

def iniciar_servidor(host="127.0.0.1", port=5001):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.bind((host, port))
        servidor.listen()

        print("Servidor B esperando conexión...")

        conn, addr = servidor.accept()

        with conn:
            print("Conectado por:", addr)

            mensaje = conn.recv(1024).decode()
            print("Saludo recibido:", mensaje)

            respuesta = f"B recibió: {mensaje}"

            conn.sendall(respuesta.encode())