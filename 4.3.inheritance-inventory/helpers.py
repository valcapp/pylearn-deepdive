from typing import Callable
from functools import wraps

def check_natural(val:int)->None:
    """Check is value is a natural number,
    returns None if check is passed,
    raises a TypeError if not
    
    Args:
        val (int): value to check
        
    Returns:
        None

    Raises:
        TypeError: if val is not instance of integer or less than 0.
    """
    if not isinstance(val, int) or val<0:
        raise TypeError('Value must be non-negative integer')

class InsufficientResource(ValueError):
    """When there are not enough available items in stock"""

def quote_if_str(val)->str:
    if isinstance(val,str):
        return f"'{val}'"
    else:
        return val

def check_sufficient(available:int, requested:int)->None:
    if available < requested:
        raise InsufficientResource(
            "Current items are insufficient to satisfy the request."
            +f"Resource: {available}; Requested: {requested}s"
        )

def expect_natural(func:Callable)->Callable:
    @wraps(func)
    def checked(self, *args, **kwargs):
        val, _ = args + (None,)
        check_natural(val)
        return func(self, *args, **kwargs)
    return checked