### HIT 7

# Enunciado:
Modifique el programa C y D, de manera tal de implementar un “sistema de inscripciones”, esto es, se define una ventana de tiempo fija de 1 MIN, coordinada por D, y los nodos C deben registrarse para participar de esa ventana. Cuando un nodo C se registra a las 11:28:34 en D, el registro se hace efectivo para la próxima ventana de tiempo que corresponde a las 11:29. Cuando se alcanza las 11:29:00, el nodo D cierra las inscripciones y todo nodo C que se registre será anotado para la ventana de las 11:30. Los nodos C que consulten las inscripciones activas solo pueden ver las inscripciones de la ventana actual, es decir, los nodos C no saben a priori cuáles son sus pares para la próxima ventana de tiempo, solo saben los que están activos actualmente. Recuerde almacenar las inscripciones en un archivo de texto con formato JSON. Esto facilitará el seguimiento ordenado de las ejecuciones y asegurará la verificación de los resultados esperados.
Para simplificar el problema, imagine que D lleva dos registros: un listado de los nodos C activos en la ventana actual, y un registro de nodos C registrados para la siguiente ventana. Cada 60 segundos el nodo D mueve los registros de las inscripciones futuras a la presente y comienza a inscribir para la siguiente ronda.

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
HIT7/
├── logs/
├── tests/
|   └── HIT7_Test.py
├── venv/
├── HIT7_NodoC.py
├── HIT7_NodoD.py
├── Logger.py
├── README.md
└── requirements.txt
```

Archivos principales:
* HIT7_NodoD.py — nodo registry (D).
* HIT7_NodoC.py — nodo subcriptor (C).
* tests/HIT7_Test.py — script de pruebas automáticas.

---

### 3. Preparación el entorno y dependencias

#### Creación del entorno virtual:

Linux / macOS

```bash
$ python3 -m venv venv
```
Windows
```bash
$ python -m venv venv
```

#### Activación del entorno virtual:

Linux / macOS

```bash
source venv/bin/activate
```

Windows
```bash
venv/bin/activate
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

### 4. Ejecución del Nodo D

Iniciar el nodo registry:

Linux / macOS
```bash
python3 HIT7_NodoD.py
```

Windows
```bash
python HIT7_NodoD.py
```

El registry se ejecuta en:
```bash
http://127.0.0.1:8000
```

Endpoint disponible:
```bash
GET /health
```
---

### 5. Ejecución de nodos C
Iniciar un nodo C indicando la dirección del registry.

Linux / macOS
```bash
python3 HIT7_NodoC.py 127.0.0.1 8000
```
Windows
```bash
python HIT7_NodoC.py 127.0.0.1 8000
```
Cada nodo C:
1. Inicia escucha en un puerto aleatorio
2. Se registra en el nodo D
3. Recibe la lista de nodos subcriptos en ventanas pasadas, cada 60 segundos consulta por actualizaciones
4. Envía saludo a los demás nodos

Para probar múltiples nodos, ejecutar el comando en distintas terminales.

---

### 6. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT7_Test.py
```
Windows
```bash
python tests/HIT7_Test.py
```

---

### 7. Resultado esperado del test

* El registry registra los nodos C en ventanas de tiempo diferentes dependiendo de la fecha de registro

---