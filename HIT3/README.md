### HIT 3

# Enunciado:
Modifique el código de B para que si el proceso A cierra la conexión (por ejemplo matando el proceso) siga funcionando.

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
HIT3/
├── logs/
├── tests/
│   └── HIT3_Test.py
├── HIT3_Cliente.py
├── HIT3_Servidor.py
├── Logger.py
└── README.md
```

Archivos principales:
* HIT3_Servidor.py — nodo B, sigue funcionando aunque A se caiga abruptamente.
* HIT3_Cliente.py — nodo A, con reconexión automática.
* tests/HIT3_Test.py — script de pruebas automáticas.

---

### 3. Ejecución del Servidor (Nodo B)

Iniciar el servidor primero:

Linux / macOS
```bash
python3 HIT3_Servidor.py
```
Windows
```bash
python HIT3_Servidor.py
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
python3 HIT3_Cliente.py
```
Windows
```bash
python HIT3_Cliente.py
```

Si A se cae o es terminado abruptamente, B detecta la desconexión, cierra el socket de ese cliente y sigue esperando nuevas conexiones.

---

### 5. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT3_Test.py
```
Windows
```bash
python tests/HIT3_Test.py
```

---

### 6. Resultado esperado del test

* A se conecta a B y envía un mensaje.
* A se desconecta (simulado).
* B sigue funcionando y acepta una nueva conexión de A.
* A envía un nuevo mensaje y recibe respuesta correctamente.

