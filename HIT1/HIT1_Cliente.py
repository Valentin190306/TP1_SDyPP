# #Fuente: ChatGPT

import socket

def cliente_saludar(host, port, mensaje):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        cliente.connect((host, port))

        cliente.sendall(mensaje.encode())

        respuesta = cliente.recv(1024).decode()

    return respuesta