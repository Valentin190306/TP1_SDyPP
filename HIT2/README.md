### HIT 2

# Enunciado:
Revise el código de A para implementar una funcionalidad que permita la reconexión y el envío del saludo nuevamente en caso de que el proceso B cierre la conexión, como por ejemplo, al ser terminado abruptamente.

## Instrucciones de ejecución

### 1. Requisitos

Software necesario para ejecutar el proyecto.

* Sistema operativo: Linux / macOS / Windows
* Lenguaje: Python 3.x

Comandos según sistema operativo:

| Sistema | Comando Python  |
| ------- | --------------- |
| Linux   | `python3`       |
| macOS   | `python3`       |
| Windows | `python` o `py` |

---

### 2. Estructura de fichero del ejercicio

```
HIT2/
├── logs/
├── tests/
│   └── HIT2_Test.py
├── HIT2_Cliente.py
├── HIT2_Servidor.py
├── Logger.py
└── README.md
```

Archivos principales:
* HIT2_Servidor.py — nodo B, acepta múltiples clientes con threading.
* HIT2_Cliente.py — nodo A, se reconecta automáticamente si B cae.
* tests/HIT2_Test.py — script de pruebas automáticas.

---

### 3. Ejecución del Servidor (Nodo B)

Iniciar el servidor primero:

Linux / macOS
```bash
python3 HIT2_Servidor.py
```
Windows
```bash
python HIT2_Servidor.py
```

El servidor escucha en:
```
127.0.0.1:5001
```

---

### 4. Ejecución del Cliente (Nodo A)

En otra terminal, iniciar el cliente:

Linux / macOS
```bash
python3 HIT2_Cliente.py
```
Windows
```bash
python HIT2_Cliente.py
```

El cliente pide un mensaje por consola, lo envía al servidor y espera respuesta. Si el servidor cae, reintenta la conexión automáticamente cada 2 segundos.

---

### 5. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT2_Test.py
```
Windows
```bash
python tests/HIT2_Test.py
```

---

### 6. Resultado esperado del test

* El cliente A se conecta al servidor B y envía un mensaje.
* B cae (simulado) y A se reconecta automáticamente.
* A envía un nuevo mensaje y recibe respuesta correctamente.

