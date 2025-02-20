import json

class message:
    # msg types
    TEXT_MSG = "txt"
    WARNING_MSG = "wrn"
    ERROR_MSG = "err"
    INFO_MSG = "inf"

    # code types
    VALID_PASSWD = "v_psw"
    INVALID_PASSWD = "i_psw"
    SUCCESS = 0
    FAILURE = 1

    def __init__(self, msg_type, msg_content):
        self.msg_type = msg_type
        self.msg_content = msg_content
    
    def to_dic(self):
        return self.__dict__
    
    def from_json(self):
        return json.loads(self)
        
        