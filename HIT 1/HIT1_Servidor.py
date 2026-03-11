#Fuente: ChatGPT

import socket

HOST = "0.0.0.0"   # Escucha en todas las interfaces
PORT = 5000        # Puerto del servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()

    print("Servidor B esperando conexión...")

    conn, addr = servidor.accept()
    with conn:
        print("Conectado por:", addr)

        mensaje = conn.recv(1024).decode()
        print("Saludo recibido:", mensaje)

        respuesta = "Hola A, aquí B. Saludo recibido."
        conn.sendall(respuesta.encode())