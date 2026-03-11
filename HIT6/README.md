### HIT 6

# Enunciado:
Cree un programa D, el cual actuará como un “Registro de contactos”. Para ello, en un array en RAM, inicialmente vacío, este nodo D llevará un registro de los programas C que estén en ejecución.
Además, el nodo D debe exponer un endpoint HTTP /health que devuelva el estado del servicio en formato JSON (cantidad de nodos C registrados, uptime, estado general). Este endpoint será utilizado como health check público del sistema.
Modifique el programa C de manera tal que reciba por parámetros únicamente la IP y el puerto del programa D. C debe iniciar la escucha en un puerto aleatorio y debe comunicarse con D para informarle su IP y su puerto aleatorio donde está escuchando. D le debe responder con las IPs y puertos de los otros nodos C que estén corriendo, haga que C se conecte a cada uno de ellos y envíe el saludo.
Es decir, el objetivo de este HIT es incorporar un nuevo tipo de nodo (D) que actúe como registro de contactos para que al iniciar cada nodo C no tenga que indicar las IPs de sus pares. Esto debe funcionar con múltiples instancias de C, no solo con 2.

## Instrucciones para ejecutar el proyecto:

## Diagrama de arquitectura

## Decisiones de diseño tomadas.