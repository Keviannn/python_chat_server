import json
import socket

class message:
    # msg types
    TEXT_MSG = "txt"
    WARNING_MSG = "wrn"
    ERROR_MSG = "err"
    INFO_MSG = "inf"

    # code types
    VALID_PASSWD = "v_psw"
    INVALID_PASSWD = "i_psw"
    TIMEOUT_EX = "t_ex"
    ACKNOWLEDGE = "ack"
    SUCCESS = 0
    FAILURE = 1

    def __init__(self, msg_type, msg_content):
        self.msg_type = msg_type
        self.msg_content = msg_content
    
    def to_json(self):
        return json.dumps({"msg_type": self.msg_type, "msg_content": self.msg_content})
    
    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        return cls(d["msg_type"], d["msg_content"])
    
    @classmethod
    def get_ack(cls, socket):
        ack = cls.from_json(socket.recv(1024).decode('ascii'))
        if ack.msg_content == message.ACKNOWLEDGE:
            socket.send(ack.to_json().encode('ascii'))
            return True
        else:   
            return False
    
    @classmethod
    def send_ack(cls, socket):
        ack = message(message.INFO_MSG, message.ACKNOWLEDGE)
        socket.send(ack.to_json().encode('ascii'))
        response = cls.from_json(socket.recv(1024).decode('ascii'))
        if(response.msg_content == message.ACKNOWLEDGE):
            return True
        else:
            return False

    
    
        
        