import socket
import threading
from client_object import client as user
import sys
from datetime import datetime

class server_chat:
    # prints the msg to all clients
    def broadcast(self, msg):
        open('chat-log.txt', 'a').write(datetime.now().strftime("%d-%m-%Y %H:%M ") + msg.decode('ascii') + '\n')
        for client in self.clients:
            client.client_socket.send('/log_updated'.encode('ascii'))

    # console management
    def console(self):
        while True:
            command = input("csh> ")
            if command == 'stop':
                break
            if command == 'log':
                log = open('chat-log.txt', 'r').read()
                print(log)
                
    # accepts new clients
    def accept_clients(self):
        self.server.settimeout(0.001)
        while self.running:
            try:
                # accepts new clients, gets their name and adds them to a list
                client_socket, client_dir = self.server.accept()

                # creates new thread for managing the client and add the thread to a list
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket, client_dir))
                client_thread.start()
                self.client_threads.append(client_thread)
            except socket.timeout:
                pass
            except: 
                break
        
    # handles clients conections
    def client_handler(self, client_socket, client_dir):
        # gets client name and creates the user
        name = client_socket.recv(1024).decode('ascii')
        new_client = user(client_socket, client_dir, name)
        self.clients.append(new_client)

        # announces the user has joined 
        self.broadcast(f"{new_client.client_name} joined!".encode('ascii'))

        new_client.client_socket.settimeout(0.001)
        while self.running:
            try:
                msg = new_client.client_socket.recv(1024).decode('ascii')

                if msg:
                    if msg == '/exit':
                        self.broadcast(f"{new_client.client_name} left.".encode('ascii'))
                        break
                    elif msg == '/log':
                        log = open('chat-log.txt', 'r').read()
                        new_client.client_socket.send(log.encode('ascii'))
                    else:
                        self.broadcast(f"{new_client.client_name}: {msg}".encode('ascii'))
            except socket.timeout:
                continue
            except:
                break
            
        new_client.client_socket.close()
        self.clients.remove(new_client)

    # initializes the server on instance creation 192.168.1.71
    def __init__(self, ip = '127.0.0.1', port = 10000):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(5)
        self.running = True
        self.clients = []
        self.client_threads = []

        print("===== Wellcome to kevian-cloud chat! =====\nDevelopment stage 0.0.0\n")
        print("Server online, waiting for clients...")

        # creates both console and client accpeter threads
        self.accept_thread = threading.Thread(target=self.accept_clients, args=())
        self.accept_thread.start()

        self.console_thread = threading.Thread(target=self.console, args=())
        self.console_thread.start()

if __name__ == "__main__":
    server = server_chat()
    server.console_thread.join()
    server.running = False
    server.server.close()
    # waits for client threads when getting out of the while loop
    for thread in server.client_threads:
        thread.join()
    server.accept_thread.join()
    print("Server closed.")
    sys.exit()

