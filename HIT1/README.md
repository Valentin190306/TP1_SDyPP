### HIT 1

# Enunciado:
Elabore un código de servidor TCP para B que espere el saludo de A y lo responda.
Elabore un código de cliente TCP para A que se conecte con B y lo salude.

## Instrucciones de ejecución

### 1. Requisitos

Software necesario para ejecutar el proyecto.

* Sistema operativo: Linux / macOS / Windows
* Lenguaje: Python 3.13.5

Comandos según sistema operativo:

| Sistema | Comando Python  |
| ------- | --------------- |
| Linux   | `python3`       |
| macOS   | `python3`       |
| Windows | `python` o `py` |

---

### 2. Estructura de fichero del ejercicio

Descripción breve de los archivos necesarios para ejecutar el HIT.

```
HIT1/
├── logs/
├── tests/
|   └── HIT1_Test.py
├── HIT1_Cliente.py
├── HIT1_Servidor.py
├── README.md
```

Archivos principales:
* HIT1_Cliente.py — nodo cliente (A).
* HIT1_Servidor.py — nodo servidor (B).
* tests/HIT1_Test.py — script de pruebas automáticas.

---

### 3. Ejecución del Nodo B

Iniciar el nodo servidor:

Linux / macOS
```bash
python3 HIT1_Servidor.py
```

Windows
```bash
python HIT1_Servidor.py
```

El servidor escucha en:
```
127.0.0.1:5001
```

### 5. Ejecución del Nodo A

Iniciar un nodo cliente.

Linux / macOS
```bash
python3 HIT1_Cliente.py
```
Windows
```bash
python HIT1_Cliente.py
```

---

### 6. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT1_Test.py
```
Windows
```bash
python tests/HIT1_Test.py
```

---

### 7. Resultado esperado del test

* El cliente A se conecta al servidor B.
* A envía el mensaje "Hola B".
* B responde "B recibió: Hola B".
* El test verifica que la respuesta sea correcta.

---

## Conclusión

Primer acercamiento a la lógica de uso de mensajes TCP por medio de sockets en una arquitectura cliente - servidor. Un proceso se dedicara a escuchar peticiones de conexión, y el otro buscara conectarse y enviar un mensaje. El proceso que escucha puede responder al mensaje, pero siempre escucha o espera.