# Chat Server in Python

The goal is to develop a cloud service that enables multiple users to chat concurrently and securely through a robust and simple interface.

## Implementation

Currently, all the classes are under development, and their number is continually evolving. Additional documentation will be provided as the project progresses.

## Client

### client_app.py
This file handles all communication with the server from the client-side application.

## Server

### server_app.py
This file runs the server and retrieves its initial configuration from `server_info.json`. It utilizes functions from `server_client_handler.py` to manage client connections.

- #### server_info.json
  This file stores critical server information such as its name, IP address, and port.

- #### server_client_handler.py
  This file is responsible for managing client connections, including client storage, creation, and validation.

## Common

### definitions.py
This file contains common definitions shared between the client and server. It is planned to be primarily used on the server side, with the client adapting to these definitions.

### message.py
A common class used for managing and creating messages.


    