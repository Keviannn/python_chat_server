import json
from common.definitions import *

class client:
    # client constructor
    def __init__(self, client_socket, client_dir):
        self.client_socket = client_socket
        self.client_dir = client_dir

    # validates the client session
    def validate_session(self, client_name, client_password):
        try:
            with open('../clients/' + client_name + '.json', 'r') as client_file:       # opens the client file
                client_data = json.load(client_file)                                    # loads the client data
                if(client_password == client_data['password']):                         # checks if the password is correct
                    return True
                else:
                    return False
        
        # exception handling
        except FileNotFoundError:
            print("Client not found")

        except OSError:
            print("Could not open file")
    
    # creates a new client
    def create_client(self):
        name = self.client_socket.recv(1024).decode(TEXT_FORMAT)                                # gets the client name
        password = self.client_socket.recv(1024).decode(TEXT_FORMAT)                            # gets the client password
        try:
            with open('../clients/' + self.client_name + '.json', 'w') as client_file:                      # opens the client file
                client_data = {'email': name, 'password': password}                                         # creates the client data
                json.dump(client_data, client_file)                                                         # writes the client data to the file
                self.client_socket.send("Client created".encode(TEXT_FORMAT))                   # sends a message to the client
        
        # exception handling
        except OSError:
            print("Could not open file")