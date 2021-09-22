from helpers import (
    check_sufficient,
    check_natural,
    expect_natural,
    quote_if_str,
)

class Resource:
    def __init__(self, name:str, manufacturer:str, total:int, allocated:int)->None:
        check_natural(total)
        check_natural(allocated)
        check_sufficient(total, allocated)
        self._name = name
        self._manufacturer = manufacturer
        self._total = total
        self._allocated = allocated
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def manufacturer(self)->str:
        return self._manufacturer
    
    @property
    def total(self)->int:
        return self._total
    
    @property
    def allocated(self)->int:
        return self._allocated

    @property
    def available(self)->int:
        return self.total - self.allocated
    
    def __str__(self)->str:
        return self.name
    
    def __repr__(self)->str:
        init_vals = ", ".join(
            f"{attr}={quote_if_str(getattr(self,attr))}" for attr in
            ('name','manufacturer','total','allocated')
        )
        return f"{self.__class__.__name__}({init_vals})"
    
    @property
    def category(self)->str:
        return self.__class__.__name__.casefold()
    
    @expect_natural
    def claim(self, n_items:int)->None:
        check_sufficient( self.available, n_items)
        self._allocated += n_items
    
    @expect_natural
    def freeup(self, n_items:int)->None:
        check_sufficient(self.allocated, n_items)
        self._allocated -= n_items
    
    @expect_natural
    def died(self, n_items:int)->None:
        check_sufficient(self.available, n_items)
        self._total -= n_items
    
    @expect_natural
    def purchased(self, n_items:int)->None:
        self._total += n_items
        