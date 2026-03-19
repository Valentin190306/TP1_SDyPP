### HIT 8

# Enunciado:
Refactorice la comunicación del Hit #5 (mensajes JSON sobre TCP) reemplazándola por gRPC con Protocol Buffers. Para ello:
    1. Defina un archivo .proto que describa los mensajes y servicios de comunicación entre los nodos C y D.
    2. Genere los stubs de cliente y servidor con el compilador protoc para su lenguaje elegido.
    3. Reemplace la serialización/deserialización JSON manual por las llamadas gRPC generadas.
Compare en su informe: el tamaño de los mensajes en bytes (JSON vs protobuf), la latencia de las llamadas, y la experiencia de desarrollo (código manual vs código generado).

## Instrucciones de ejecución

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
HIT8/
├── logs/
├── tests/
│   └── HIT8_Test.py
├── venv/
├── HIT8_NodoC.py
├── saludo.proto
├── saludo_pb2.py
├── saludo_pb2_grpc.py
├── Logger.py
├── README.md
└── requirements.txt
```

Archivos principales:
* HIT8_NodoC.py — nodo C, cliente y servidor simultáneo con gRPC.
* saludo.proto — definición de mensajes y servicios.
* saludo_pb2.py — generado por protoc, clases de mensajes.
* saludo_pb2_grpc.py — generado por protoc, stubs de cliente y servidor.
* tests/HIT8_Test.py — script de pruebas automáticas.

---

### 3. Preparación del entorno y dependencias

#### Creación del entorno virtual:

Linux / macOS
```bash
python3 -m venv venv
```
Windows
```bash
python -m venv venv
```

#### Activación del entorno virtual:

Linux / macOS
```bash
source venv/bin/activate
```
Windows
```bash
venv\Scripts\activate
```

#### Instalación de dependencias:

Linux / macOS
```bash
pip3 install -r requirements.txt
```
Windows
```bash
pip install -r requirements.txt
```

---

### 4. Generación de stubs

Con el entorno virtual activado, generar los stubs desde el archivo `.proto`:

Linux / macOS
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. saludo.proto
```

Windows
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. saludo.proto
```

Esto genera `saludo_pb2.py` y `saludo_pb2_grpc.py`.

---

### 5. Ejecución de los nodos

Iniciar cada nodo en una terminal distinta:

Linux / macOS
```bash
# Terminal 1
python3 HIT8_NodoC.py 127.0.0.1 5001 127.0.0.1 5002

# Terminal 2
python3 HIT8_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
```
Windows
```bash
# Terminal 1
python HIT8_NodoC.py 127.0.0.1 5001 127.0.0.1 5002

# Terminal 2
python HIT8_NodoC.py 127.0.0.1 5002 127.0.0.1 5001
```

Cada nodo recibe cuatro parámetros:
```
<mi_host> <mi_puerto> <host_remoto> <puerto_remoto>
```

---

### 6. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT8_Test.py
```
Windows
```bash
python tests/HIT8_Test.py
```

---

### 7. Resultado esperado del test

* C1 saluda a C2 y recibe respuesta vía gRPC.
* C2 saluda a C1 y recibe respuesta vía gRPC.
* Ambos canales funcionan simultáneamente.
* El servidor sigue respondiendo tras la desconexión del cliente.
* Se imprime la comparación de tamaño de mensajes JSON vs Protobuf.
* Se imprime la latencia promedio de las llamadas gRPC.

Ejemplo de salida de los tests de comparación:
```
Tamaño JSON    : 80 bytes
Tamaño Protobuf: 55 bytes
Reducción      : 31.2%

Latencia gRPC — promedio: X.XXXms | min: X.XXXms | max: X.XXXms
```

---

### 8. Datos relevados

Equipo de prueba:
* SO: Debian 13 (Trixie)
* Procesador: AMD Ryzen 7 5700G
* RAM: 8 GB

Resultados:
```bash
==================================================
Test 5: Comparación tamaño mensajes (JSON vs Protobuf)
Tamaño JSON    : 95 bytes
Tamaño Protobuf: 62 bytes
Reducción      : 34.7%
Comparación de tamaño OK
==================================================
```

Medidas de latencia:
```bash
Latencia gRPC — promedio: 1.072ms | min: 0.959ms | max: 1.32ms
```