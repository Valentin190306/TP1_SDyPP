### HIT 6

# Enunciado:
Cree un programa D, el cual actuará como un “Registro de contactos”. Para ello, en un array en RAM, inicialmente vacío, este nodo D llevará un registro de los programas C que estén en ejecución.
Además, el nodo D debe exponer un endpoint HTTP /health que devuelva el estado del servicio en formato JSON (cantidad de nodos C registrados, uptime, estado general). Este endpoint será utilizado como health check público del sistema.
Modifique el programa C de manera tal que reciba por parámetros únicamente la IP y el puerto del programa D. C debe iniciar la escucha en un puerto aleatorio y debe comunicarse con D para informarle su IP y su puerto aleatorio donde está escuchando. D le debe responder con las IPs y puertos de los otros nodos C que estén corriendo, haga que C se conecte a cada uno de ellos y envíe el saludo.
Es decir, el objetivo de este HIT es incorporar un nuevo tipo de nodo (D) que actúe como registro de contactos para que al iniciar cada nodo C no tenga que indicar las IPs de sus pares. Esto debe funcionar con múltiples instancias de C, no solo con 2.

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
HIT6/
├── logs/
├── tests/
|   └── HIT6_Test.py
├── venv/
├── HIT6_NodoC.py
├── HIT6_NodoD.py
├── Logger.py
├── README.md
└── requirements.txt
```

Archivos principales:
* HIT6_NodoD.py — nodo registry (D).
* HIT6_NodoC.py — nodo subscriptor (C).
* tests/HIT6_Test.py — script de pruebas automáticas.

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
python3 HIT6_NodoD.py
```

Windows
```bash
python HIT6_NodoD.py
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
python3 HIT6_NodoC.py 127.0.0.1 8000
```
Windows
```bash
python HIT6_NodoC.py 127.0.0.1 8000
```
Cada nodo C:
1. Inicia escucha en un puerto aleatorio
2. Se registra en el nodo D
3. Recibe la lista de nodos existentes
4. Envía saludo a los demás nodos

Para probar múltiples nodos, ejecutar el comando en distintas terminales.

---

### 6. Ejecución de tests

Linux / macOS
```bash
python3 tests/HIT6_Test.py
```
Windows
```bash
python tests/HIT6_Test.py
```

---

### 7. Resultado esperado del test

* Los nodos C se registran en el nodo D.
* El registry devuelve la lista de nodos existentes.
* Cada nodo C se conecta con los demás nodos.
* El endpoint /health devuelve el estado del servicio.

Ejemplo de respuesta del endpoint /health:
```bash
{
  "status": "ok",
  "nodos_registrados": 3,
  "uptime": 5.04
}
```
---

## Conclusión

El nuevo nodo D tiene el proposito particular de almacenar la información de conexión de todos los nodos C que deciden ser visibles ante el resto de nodos C. Para que un nodo C no tenga que almacenar la información de todos los nodos C para permitir la comunicación, recurre al servicio del nodo D por medio de una URL para dar a conocer sus datos propios y acceder a la lista de nodos C disponibles. Los nodos C entonces consumen la llamada API del nodo D. Entonces los nodos C solo deben conocer la dirección IP y el puerto del servidor web para realizar la consulta HTTP y tener acceso a todos los demas nodos C.
