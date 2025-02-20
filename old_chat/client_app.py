import socket
import threading
import sys
import readline

class chat_client:
    def __init__(self):
        print("===== Wellcome to kevian-cloud chat! =====\nDevelopment stage 0.0.0\n")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 10000))
        name = input("Write your name: ")
        self.client.send(name.encode('ascii'))
        self.running = True

    def recieve_log_updates(self):
        while self.running:
            try:
                msg = self.client.recv(1024).decode('ascii')
                if msg == '/log_updated':
                    self.client.send('/log'.encode('ascii'))
                    log = self.client.recv(4096).decode('ascii')
                    current_input = readline.get_line_buffer()
                    sys.stdout.write("\033c") 
                    print(log)
                    sys.stdout.write(f"Write message: {current_input}") 
                    sys.stdout.flush()
                    readline.redisplay()
                else:
                    print(msg)
            except:
                if self.running:
                    print("Server closed.")
                    self.client.close()
                    sys.exit()
                break

    def write_msg(self):
        while True:
            try:
                msg = input("")
                if msg == '/exit':
                    self.client.send(msg.encode('ascii'))
                    self.running = False
                    self.client.close()
                    sys.exit()
                else:
                    self.client.send(msg.encode('ascii'))
            except:
                if self.running:
                    print("Server closed.")
                    self.client.close()
                    sys.exit()
                break

if __name__ == "__main__":
    client = chat_client()

    recieve_log_thread = threading.Thread(target=client.recieve_log_updates)
    recieve_log_thread.start()

    write_msg_thread = threading.Thread(target=client.write_msg)
    write_msg_thread.start()

    recieve_log_thread.join()
    write_msg_thread.join()

    print("Client closed.")

    