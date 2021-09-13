from __future__ import annotations
from collections.abc import Callables

class InvalidValue(ValueError):
    """When the value does not meet validy requirements"""

class NegativeValueError(InvalidValue):
    """When the value is expected to be greater than or equal to zero."""
    
class NonIntegerValueError(InvalidValue):
    """When the value is expected to integer."""

def check_validity(value, validate:Callable, err_type:Exception, message:str)->bool:
    try:
        if not validate(value):
            raise err_type(message)
    except ValueError as exc:
        raise err_type(message) from exc

def check_integer(value:int)->None:
    return check_validity(
        value, lambda value: isinstance(int(value), int),
        NonIntegerValueError,
        f'{value} is not an integer, it must be '
    )

def check_positive(value:int)->None:
    return check_validity(
        value, lambda value: value > 0,
        NegativeValueError,
        f'{value} is not positive, it must be > 0'
    )

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
                f"{key} = {getattr(self, key)}"
                for key in ('value','modulus')
            )
            +")"
        )
    
    def __eq__(self, other)->bool:
        custom_exc = NotImplemented(
            f'{other} cannot be compared with instance of {self}.'
            + f'{self.__class__.__name__} instance must be compared '
            + 'with either an int or same class instance with same modulus'
        )
        if isinstance(other, int):
            return self.value == (other % self.modulus)
        elif isinstance(other, self.__class__):
            if self.modulus != other.modulus:
                raise custom_exc
            return self.value == other.value
        else:
            raise custom_exc
    
    def __hash__(self)->int:
        return hash((self.__class__, self.value, self.modulus,))
    
    def __int__(self)->int:
        return self.value
    
    def __add__(self, other)->Mod:
        if isinstance(other, int):
            new_value = self.value + other
        elif isinstance(other, self.__class__):
            new_value = self.value + other.value
        else:
            raise NotImplemented(
                f'{other} cannot be added to instance of {self.__class__.__name__}'
                +'it must be either same type or int.'
            )
        return Mod(new_value, self.modulus)

    def __iadd__(self, other)->None:
        self._value = self.__add__(other).value % self.modulus
    
    def __radd__(self, other)->None:
        return self.__add__(other)
    
    def __neg__(self)->Mod:
        return self.__class__(-self.value, self.modulus)

    def __sub__(self, other)->Mod:
        return self.__add__(-other)

    def __isub__(self, other)->None:
        self._value = self.__sub__(other).value % self.modulus
    
    def __rsub__(self, other)->Mod:
        return self.__neg__().__add__(other)
    
    def __mul__(self, other)->Mod:
        if isinstance(other, int):
            new_value = self.value * other
        elif isinstance(other, self.__class__):
            new_value = self.value * other.value
        else:
            raise NotImplemented(
                f'{other} cannot be added to instance of {self.__class__.__name__}'
                +'it must be either same type or int.'
            )
        return Mod(new_value, self.modulus)

    def __imul__(self, other)->None:
        self._value = = self.__mul__(other).value % self.modulus
    
    def __rmul__(self, other)->Mod:
        return self.__mul__(other)
    