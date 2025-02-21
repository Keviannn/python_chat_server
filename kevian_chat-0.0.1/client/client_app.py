import socket
import getpass
import threading
import sys
import queue
import os

from common.message import *

VERSION = "0.0.1"

class client_app:
        
    def __init__(self):
        # creates the client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 10000))

        # other variables
        self.log_in_success = False

        # recieve transmission values
        self.text_format = self.client.recv(1024).decode('ascii')
        self.client.send(message(message.INFO_MSG, message.ACKNOWLEDGE).to_json().encode('ascii'))
        self.max_transmission_size = int(self.client.recv(1024).decode(self.text_format))
        

        print("===== Welcome to chat client! =====\nVersion: "+ VERSION + "\n")
        server_name = self.client.recv(self.max_transmission_size).decode(self.text_format)
        server_version = self.client.recv(self.max_transmission_size)

        print("Conected to" + server_name + ". Server version: " + server_version)

        # receives the welcome message
        print(self.client.recv(self.max_transmission_size).decode(self.text_format))  

        # log in or sign in menu                   
        self.log_sign_in_menu()
        
        # TODO client functionality

    def log_sign_in_menu(self):
        print("===== Log in (0) or Sign in (1) =====")
        while True:
            os.system('clear')
            option = input("Option: ")
            if option == '0':
                self.client.send(0)
                if self.log_in():
                    print("Log in success")
                    self.log_in_success = True
                    return
                else:
                    print("Log in failed")
                    self.log_in_success = False
                    return
            elif option == '1':
                self.client.send(1)
                self.sign_in()
            else:
                print('Non valid input')
                continue
        
    def log_in(self):
        count = 0
        success = False
        while count < 3:
            name = input("Write your name: ")
            self.client.send(name.encode(self.text_format))
            password = getpass.getpass("Write your password: ")
            self.client.send(password.encode(self.text_format))
            validation_msg = message.from_json(self.client.recv(self.max_transmission_size).decode(self.text_format))
            if validation_msg.msg_type == message.WARNING_MSG and validation_msg.msg_content == message.VALID_PASSWD:
                success = True
                break
            count += 1
        return success

    def sign_in(self):
        name = input("Write your name: ")
        self.client.send(name.encode(self.text_format))
        match = False
        while not match:
            password_0 = getpass.getpass("Write your password: ")
            password_1 = getpass.getpass("Write your password again: ")
            if password_0 != password_1:
                print("Passwords do not match")
                continue
            else:
                match = True
        self.client.send(password_0.encode(self.text_format))
        response = self.client.recv(self.max_transmission_size).decode(self.text_format)
        print('Server response: ' + response)

if __name__ == "__main__":
    client = client_app()

        

