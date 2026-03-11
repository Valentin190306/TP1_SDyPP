# #Fuente: ChatGPT

# import socket

# HOST = "127.0.0.1"  # IP del servidor B
# PORT = 5000

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
#     cliente.connect((HOST, PORT))

#     saludo = "Hola B, te saluda A."
#     cliente.sendall(saludo.encode())

#     respuesta = cliente.recv(1024).decode()
#     print("Respuesta del servidor:", respuesta)

import socket

def cliente_saludar(host, port, mensaje):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        cliente.connect((host, port))

        cliente.sendall(mensaje.encode())

        respuesta = cliente.recv(1024).decode()

    return respuesta