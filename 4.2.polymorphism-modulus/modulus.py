from __future__ import annotations
from collections.abc import Callable

def check_validity(value, validate:Callable, err_type:Exception, message:str)->bool:
    try:
        if not validate(value):
            raise err_type(message)
    except ValueError as exc:
        raise err_type(message) from exc

def check_integer(value:int)->None:
    return check_validity(
        value, lambda value: isinstance(int(value), int),
        ValueError,
        f'{value} is not an integer, it must be integer'
    )

def check_positive(value:int)->None:
    return check_validity(
        value, lambda value: value > 0,
        ValueError,
        f'{value} is not positive, it must be > 0'
    )

def value_of(other)->int:
    return other if isinstance(other, int) else other.value
class Mod:
    """Implements some concepts of modular arithmetic"""
    def __init__(self, value:int, modulus:int)->None:
        check_integer(modulus)
        check_positive(modulus)
        check_integer(value)
        self._value = value % modulus
        self._modulus = modulus
    
    @property
    def value(self)->int:
        return self._value

    @property
    def modulus(self)->int:
        return self._modulus
    
    def __repr__(self)->str:
        return (
            f"{self.__class__.__name__}("
            +', '.join(
                f"{key}={getattr(self, key)}"
                for key in ('value','modulus')
            )
            +")"
        )
    
    def check_implemented(self, other, message='')->None:
        not_implemented = TypeError(
            f'Unsupported operation between {type(other)} and {self.__class__.__name__}.'
            +f'{self.__class__.__name__} supports operations with either int'
            +f'or another {self.__class__.__name__} instance with same modulus'
            +message
        )
        if isinstance(other, int):
            return
        if isinstance(other, self.__class__):
            if self.modulus != other.modulus:
                raise not_implemented
            return
        else:
            raise not_implemented
    
    def __eq__(self, other)->bool:
        self.check_implemented(other)
        return (self.value ==
            (value_of(other) % self.modulus)
        )
    
    def __hash__(self)->int:
        return hash((self.__class__, self.value, self.modulus,))
    
    def __int__(self)->int:
        return self.value
    
    def __add__(self, other)->Mod:
        self.check_implemented(other)
        return self.__class__(
            self.value + value_of(other),
            self.modulus
        )

    def __iadd__(self, other)->Mod:
        self._value = self.__add__(other).value % self.modulus
        return self
    
    def __radd__(self, other)->Mod:
        return self.__add__(other)
    
    def __neg__(self)->Mod:
        return self.__class__(-self.value, self.modulus)

    def __sub__(self, other)->Mod:
        return self.__add__(-other)

    def __isub__(self, other)->Mod:
        self._value = self.__sub__(other).value % self.modulus
        return self
    
    def __rsub__(self, other)->Mod:
        return self.__neg__().__add__(other)
    
    def __mul__(self, other)->Mod:
        self.check_implemented(other)
        return self.__class__(
            self.value * value_of(other),
            self.modulus
        )

    def __imul__(self, other)->Mod:
        self._value = self.__mul__(other).value % self.modulus
        return self
    
    def __rmul__(self, other)->Mod:
        return self.__mul__(other)

    def __pow__(self, other)->Mod:
        self.check_implemented(other)
        return self.__class__(
            self.value ** value_of(other),
            self.modulus
        )
    
    def __ipow__(self, other)->Mod:
        self._value = self.__pow__(other).value % self.modulus
        return self
        
    def __gt__(self, other)->bool:
        self.check_implemented(other)
        return (self.value > value_of(other))
    
    def __ge__(self, other)->bool:
        self.check_implemented(other)
        return (self.value >= value_of(other))
    
    def __lt__(self, other)->bool:
        self.check_implemented(other)
        return (self.value < value_of(other))
    
    def __le__(self, other)->bool:
        self.check_implemented(other)
        return (self.value <= value_of(other))

    
    