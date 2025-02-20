import socket
import getpass
import threading
import sys
import queue

from common.definitions import *
from common.message import *

VERSION = "0.0.1"

class client_app:
    def log_in(self):
        count = 0
        success = False
        while count < 3:
            name = input("Write your name: ")
            self.client.send(name.encode(TEXT_FORMAT))
            password = getpass.getpass("Write your password: ")
            self.client.send(password.encode(TEXT_FORMAT))
            validation_msg = message.from_json(self.client.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT))
            if validation_msg['msg_type'] == message.WARNING_MSG and validation_msg['msg_content'] == message.VALID_PASSWD:
                success = True
                break
            count += 1
        return success

    def sign_in(self):
        name = input("Write your name: ")
        self.client.send(name.encode(TEXT_FORMAT))
        match = False
        while not match:
            password_0 = getpass.getpass("Write your password: ")
            password_1 = getpass.getpass("Write your password again: ")
            if password_0 != password_1:
                print("Passwords do not match")
                continue
            else:
                match = True
        self.client.send(password_0.encode(TEXT_FORMAT))
        response = self.client.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
        print('Server response: ' + response)

    def log_sign_in_menu(self):
        print("===== Log in (0) or Sign in (1) =====")
        while True:
            option = input("Option: ")
            if option == '0':
                self.client.send(LOG_IN)
                if self.log_in():
                    print("Log in success")
                    self.log_in_success = True
                    return
                else:
                    print("Log in failed")
                    self.log_in_success = False
                    return
            elif option == '1':
                self.client.send(SIGN_IN)
                self.sign_in()
            else:
                print('Non valid input')
                continue

    def __init__(self):
        # creates the client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 10000))

        # other variables
        self.log_in_success

        print("===== Welcome to chat client! =====\nVersion: "+ VERSION + "\n")
        server_name = self.client.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT)
        server_version = self.client.recv(MAX_TRANSMISSION_SIZE)

        print("Conected to" + server_name + ". Server version: " + server_version)

        # receives the welcome message
        print(self.client.recv(MAX_TRANSMISSION_SIZE).decode(TEXT_FORMAT))  

        # log in or sign in menu                   
        self.log_sign_in_menu()
        
        # TODO client functionality
        

if __name__ == "__main__":
    client = client_app()

        

