### HIT 5

# Enunciado:
Modifique el programa C de manera tal que los mensajes se envíen en formato JSON, serializar y deserializar los mismos al enviar/recibir.


### 1. Requisitos

Software necesario para ejecutar el proyecto.

* Sistema operativo: Linux / macOS / Windows
* Lenguaje: Python 3.13.5
* Dependencias: especificadas en `requirements.txt`

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
HIT6/
├── logs/
├── tests/
|   └── HIT5_Test.py
├── HIT5_NodoC.py
├── Logger.py
└── README.md
```

Archivos principales:
* HIT5_NodoC.py
* tests/HIT5_Test.py — script de pruebas automáticas.

---

### 4. Ejecución de nodos C
Iniciar un nodo C indicando su propia dirección IP y puerto, y la dirección IP y el puerto de su nodo C par.

Linux / macOS
```bash
python3 HIT5_NodoC.py <mi_host> <mi_puerto> <host_remoto> <puerto_remoto>

```
Windows
```bash
python HIT5_NodoC.py <mi_host> <mi_puerto> <host_remoto> <puerto_remoto>
```
Ejemplo:
```bash
Terminal 1:$ python3 HIT5_NodoC.py 127.0.0.1 5001 127.0.0.1 5002
Terminal 2:$ python3 HIT5_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
```

Para probar múltiples nodos, ejecutar el comando en distintas terminales.

---

### 5. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT5_Test.py
```
Windows
```bash
python tests/HIT5_Test.py
```

---

### 7. Resultado esperado del test

* El nodo C1 saluda al nodo C2.
* El nodo C2 saluda al nodo C1.
* Se pueden reconectar.
* Los saludos se realizan con mensajes con formato JSON.

---
