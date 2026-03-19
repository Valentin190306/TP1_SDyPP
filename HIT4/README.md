### HIT 4

# Enunciado:
Refactoriza el código de los programas A y B en un único programa, que funcione simultáneamente como cliente y servidor. Esto significa que al iniciar el programa C, se le deben proporcionar por parámetros la dirección IP y el puerto para escuchar saludos, así como la dirección IP y el puerto de otro nodo C. De esta manera, al tener dos instancias de C en ejecución, cada una configurada con los parámetros del otro, ambas se saludan mutuamente a través de cada canal de comunicación.

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
HIT4/
├── logs/
├── tests/
│   └── HIT4_Test.py
├── HIT4_NodoC.py
├── Logger.py
└── README.md
```

Archivos principales:
* HIT4_NodoC.py — nodo C, actúa como cliente y servidor simultáneamente.
* tests/HIT4_Test.py — script de pruebas automáticas.

---

### 3. Ejecución de los nodos

Iniciar cada nodo en una terminal distinta:

Linux / macOS
```bash
# Terminal 1
python3 HIT4_NodoC.py 127.0.0.1 5001 127.0.0.1 5002

# Terminal 2
python3 HIT4_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
```
Windows
```bash
# Terminal 1
python HIT4_NodoC.py 127.0.0.1 5001 127.0.0.1 5002

# Terminal 2
python HIT4_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
```

Cada nodo recibe cuatro parámetros:
```
<mi_host> <mi_puerto> <host_remoto> <puerto_remoto>
```

---

### 4. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT4_Test.py
```
Windows
```bash
python tests/HIT4_Test.py
```

---

### 5. Resultado esperado del test

* C1 saluda a C2 y recibe respuesta.
* C2 saluda a C1 y recibe respuesta.
* Ambos canales funcionan simultáneamente.
* El servidor sigue respondiendo después de que el cliente se desconecta (reconexión).

