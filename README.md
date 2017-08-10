zmq_tutorial
==========

### Esto es solo para recordar los pasos que segui, proximamente un tutorial bien armado.
### This is just a remainder. Coming soon, the real tutorial.

Cree la estructura de archivos

~~~
zmq_tutorial
|_ logger.py
|_ README.md
|_ start_conversation.py
|_ server
|  |_ handlers.py
|  |_ __init__.py
|  |_ server.py
|_ subscriber
   |_ client.py
   |_ handlers.py
   |_ __init__.py
~~~

Cree el handler del _subscriber_
Cree el handler del _server_
dentro de start conversation arme el script que crea tanto server como subscriber como threads. despues de eso se le asigna un filtro al subscriber y se setea un sleep (si, horrible) para que despues de x tiempo se le cambie el filtro al subscriber, luego de eso, se setea un sleep (si, horrible de nuevo) para enviar el mensaje 'END' que finaliza con el subscriber y el programa finaliza.







