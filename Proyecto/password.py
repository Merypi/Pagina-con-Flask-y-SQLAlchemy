import hashlib

class PasswordVer():
    
    __password = None

    def __init__(self, password):
        self.__password = password
    
    def validarPassword(self,password):
        if(hashlib.md5(bytes(self.__password, encoding='utf-8')).hexdigest() == password):
            return True
        else:
            return False