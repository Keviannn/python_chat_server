import json
import socket
import threading
import sys
import queue

from .server_client_handler import client
from common.definitions import *
from common.message import *

VERSION = "0.0.1"

class server_chat:

    # takes messages from the qeue an writes them to the log file
    def log_writer(self):
        msg = self.msg_queue.get()
        json_msg = message.from_json(msg)
        self.log_file.write(json_msg.__dict__['msg_type'] + ": " + json_msg.__dict__['msg_content'] + '\n')
    
    # writes a message to the queue in json format
    def write_queue(self, msg):
        msg = message.to_json(msg)
        self.msg_queue.put(msg)
        
    # accepts clients and creates a new thread for each one
    def accept_clients(self):
        self.server.settimeout(0.001)
        while self.running:
            try:
                client_socket, client_dir = self.server.accept()
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket, client_dir))
                client_thread.start()
                self.client_threads.append(client_thread)
            except socket.timeout:
                pass
            except: 
                print("Error accepting clients")
                break
    
    # TODO: all
    def client_handler(self, client_socket, client_dir):
        new_client = client(client_socket, client_dir)
        with self.list_lock:
            self.clients_online.append(new_client)

        # send transmission data to client
        new_client.client_socket.send(str(MAX_TRANSMISSION_SIZE).encode("ascii"))
        if not message.get_ack(new_client.client_socket):
            pass

        new_client.client_socket.send(TEXT_FORMAT.encode("ascii"))

        # sends brief information to client
        new_client.client_socket.send(self.name.encode(TEXT_FORMAT))
        new_client.client_socket.send(VERSION.encode(TEXT_FORMAT))
        
        # sends a welcome message
        new_client.client_socket.send("Wellcome to the server, please log in or sign in".encode(TEXT_FORMAT))

        # log in or sign in based on the client option
        option = new_client.client_socket.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)

        # sets the timeout
        new_client.client_socket.settimeout(60)

        if option == 0: # log in
            count = 0
            while count < 3:
                try:
                    name = client_socket.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
                    password = client_socket.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
                except socket.timeout:
                    new_client.client_socket.send(message(message.ERROR_MSG, message.TIMEOUT_EX).to_json().encode(TEXT_FORMAT))
                    new_client.client_socket.close()
                    self.clients_online.remove(new_client)
                    return
                finally:
                    if new_client.validate_session(name, password):
                        new_client.client_socket.send(message(message.WARNING_MSG, message.VALID_PASSWD).to_json().encode(TEXT_FORMAT))
                        # TODO: rest of client management
                    elif count < 2:
                        new_client.client_socket.send(message(message.WARNING_MSG, message.INVALID_PASSWD).to_json().encode(TEXT_FORMAT))
                        continue
                    else:
                        new_client.client_socket.send(message(message.WARNING_MSG, message.INVALID_PASSWD).to_json().encode(TEXT_FORMAT))
                        new_client.client_socket.close()
                        self.clients_online.remove(new_client)
                        return

        '''else:
            try:
                name = client_socket.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
                password = client_socket.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
            except socket.timeout:
                new_client.client_socket.close()
                self.clients_online.remove(new_client)
                return
            finally:
                pass

        new_client.client_socket.settimeout(None)
        if(new_client.validate_session(name, password)):
            new_client.client_socket.send("Session validated, wellcome".encode(TEXT_FORMAT))
            # No se como hacer para notificar al usuario que algo ha sido succesful para que continue de alguna forma
        else:
            new_client.client_socket.send(message(message.WARNING_MSG, message.VALID_PASSWD).to_json().encode(TEXT_FORMAT))
            new_client.client_socket.close()
            return
            
        while True:
            try:
                msg = new_client.client_socket.recv(MAX_TRANSMISSION_SIZE).decode('ascii')
            except:
                break
            
        new_client.client_socket.close()
        self.clients.remove(new_client)'''
    
    # TODO: console management of the server
    def console(self):
        input("shell> ")
        pass

    # checks if the server information is complete
    def check_server_data(self, server_data, server_file):
        if 'name' not in server_data or 'ip' not in server_data or 'port' not in server_data:
            print("Server information not complete, please set the server information: \n")
            server_file.close()
            return False
        server_file.close()
        return True

    # sets up the server information in the server_info.json file
    def set_init_info(self, server_file):
        try:
            name = input("Write the server name: ")                 # gets the server information
            ip = input("Write the server ip: ")
            port = int(input("Write the server port: "))
            server_data = {'name': name, 'ip': ip, 'port': port}    # creates the server information dictionary
            json.dump(server_data, server_file, indent=4)           # writes the server information to the file
            print("\nServer information set.\n")
            return server_data
        except:
            print("Could not write server information")

    # server constructor
    def __init__(self):
        while True:
            try:
                server_data = {}
                # server information
                with open('server_info.json', 'r') as server_file:
                    server_data = json.load(server_file)
                    if(not self.check_server_data(server_data, server_file)):               # if the server information is not complete
                        server_data = self.set_init_info(server_file)                       # set the server information

                # server values
                self.name = str(server_data['name'])                        
                self.ip = server_data['ip']
                self.port = server_data['port']

                # socket setup
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # creates the server socket
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       # sets the socket options
                self.server.bind((self.ip, self.port))                                  # binds the server to the ip and port
                self.server.listen(5)                                                   # starts listening for clients

                # extra variables
                self.running = True
                self.msg_queue = queue.Queue()
                self.log_file = open('log.txt', 'a')
                self.list_lock = threading.Lock()
                self.clients_online = []
                self.client_threads = []

                # welcome message
                print("===== Wellcome to " + self.name + " chat! =====\n- Version: " + VERSION + "\n\nServer online, waiting for clients...")

                # threads
                threading.Thread(target=self.accept_clients, args=()).start()

                # console
                while True:
                    self.console()

            # exceptions  
            except FileNotFoundError:
                print("File server_info.json not found, please set the server information: \n")
                with open('server_info.json', 'w') as server_file:
                    self.set_init_info(server_file)
            except OSError:
                print("Could not open server infromation file")
                break


if __name__ == "__main__":
    server = server_chat()
    