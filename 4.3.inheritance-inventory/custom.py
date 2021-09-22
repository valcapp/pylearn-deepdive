from resource import Resource
from helpers import check_natural

class CPU(Resource):
    def __init__(self,
            name:str, manufacturer:str,
            cores:int, socket:str, power_watts:int,
            total:int, allocated:int
        )->None:
        super().__init__(name, manufacturer, total, allocated)
        check_natural(cores)
        check_natural(power_watts)
        self._cores = cores
        self._socket = socket
        self._power_watts = power_watts
    
    @property
    def cores(self)->int:
        return self._cores
    
    @property
    def socket(self)->str:
        return self._socket
    
    @property
    def power_watts(self)->int:
        return self._power_watts


class Storage(Resource):
    def __init__(self,
            name:str, manufacturer:str,
            capacity_GB: int,
            total:int, allocated:int
        )->None:
        super().__init__(name, manufacturer, total, allocated)
        check_natural(capacity_GB)
        self._capacity_GB = capacity_GB
    
    @property
    def capacity_GB(self):
        return self._capacity_GB


class HDD(Storage):
    def __init__(self,
            name:str, manufacturer:str,
            capacity_GB: int,
            size: str, rpm:int,
            total:int, allocated:int
        )->None:
        super().__init__(name, manufacturer, capacity_GB, total, allocated)
        check_natural(rpm)
        self._size = size
        self._rpm = rpm
    
    @property
    def size(self)->str:
        return self._size
    
    @property
    def rpm(self)->int:
        return self._rpm


class SSD(Storage):
    def __init__(self,
            name:str, manufacturer:str,
            capacity_GB: int,
            interface:str,
            total:int, allocated:int
        )->None:
        super().__init__(name, manufacturer, capacity_GB, total, allocated)
        self._interface = interface
    
    @property
    def interface(self)->str:
        return self._interface
        