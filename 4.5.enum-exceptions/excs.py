from enum import Enum

class EnumAppExceptions(Enum):    
    def __new__(cls, code:int, exc_type:Exception, message:str=None)->Enum:
        appexc = object.__new__(cls)
        appexc._value_ = code
        appexc.exc_type = exc_type
        appexc.message = message
        return appexc

    def throw(self, custom_msg:str=None)->None:
        raise self.exc_type(str(custom_msg or self.message))

# example
# class AppExceptions(EnumAppExceptions):
#     NotAnInteger = (1,TypeError,'Value is not an integer.')
#     OutOfRange = (2,ValueError,'Value is out of range.')
#     KeyNotFound = (3,KeyError,'Key was not found in hashable.')