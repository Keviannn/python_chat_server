# Servicio de chat escrito en python

La meta es el desarrollo de un servicio en la nube que permita a multiples usuarios chatear de forma concurrente y concurrente y segura mediante una interfaz robusta y simple.

## Roadmap del proyecto

- Desarrollo de las clases principales de forma modular que permita su inclusión posterior en una interfaz. 

    1. Clase server_app.py: control de usuarios, log de chat, funciones de arranque y parada seguras. De forma completamente concurrente una consola y un aceptador de clientes y sus handlers.
    2. Clase client_api.py: gestión de los usuarios por parte del servidor.
    3. Clase client.py: contenedor del objeto cliente y todas sus funciones.
    4. Clase message.py: contiene la estructura de los mensajes y como van a ser mostrados, los metadatos que contienen etc.
    5. Clase client_app.py: contiene toda la interfaz grafica del usuario, tomando su funcionalidad de la clase client_api.py.

## Implmentación precisa de las clases

1. **client_api.py:** 
    - Objeto cliente: toma sus valores de un .json previamente creado. Contiene información como el nombre, contraseña y otros datos para la validación y gestión por parte del servidor.
    - validate_session(): se encarga de validar la sesión de un usuario, buscando los datos con session_finder() y, en caso de no existir, llama a client_creator() para la creación y guardado de ese nuevo usuario.
    - session_finder(): se encarga de la búsqueda de los clientes, inicialmente una colección de archivos .json almacenados en carpetas basadas en la primera letra del usuario, para acelerar la búsqueda un poco.
    - client_creator(): crea el nuevo cliente y lo almacena en la carpeta adecuada ya seleccionada por session_finder().

2. **message.py:**
    - Objeto mensaje: estructura de los metadatos de un mensaje como usuario, contenido, hora... Es la información que recibe el servidor y posteriormente refleja. 
    - 

3. **server_app.py:**
    - Objeto server: estructura con todos los sockets e información necesaria para cargar el servidor, recibe un json para facilitar la configuración. Contiene información básica como IP, puerto, información a mostrar al usuario, motd etc
    - \_\_init\_\_(): llama a get_json_info() para cargar los datos necesarios para iniciar el servidor.
    - get_init_info(): recive un json especifico del servidor y aplica los datos al servidor creado.
    - console(): servicio de consola principal del servidor, para opciones como ver el log, parar el servidor, reiniciarlo, ver uptime...
    - client_accepter(): acepta a los clientes nuevos y llama a un nuevo hilo de client_handler().
    - client_handler(): se encarga de la comuniación directa con el cliente, manejando todas sus peticiones y gestionando las comunicaciones.

4. **client_app.py:**
    - Se encargara de la comunicación con el servidor y el usuario mostrando una interfaz simple pero robusta. 
    