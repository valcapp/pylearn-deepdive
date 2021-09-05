
from decimal import Decimal
from datetime import date, datetime
import inspect

class AutoRepr:
    @classmethod
    def vars_signature(cls, dct):
        """return a map of attribute names to __init__ arguments names"""
        params = inspect.signature(cls.__init__).parameters.keys()
        inits = {}
        # print('inits: vars(cls)=', vars(dct))
        for attr in dct:
            par = next((
                par for par in params
                if attr in par
            ), None)
            # print(f'inits: attr={attr}, par={par}')
            if par is not None:
                inits[attr] = par
        # print('inits: inits=', inits)
        return inits

    @classmethod
    def signature_vars(cls, dct):
        """return a map of __init__ arguments names to attribute names"""
        return {
            val: key for key, val in
            cls.vars_signature(dct).items()
        }

    @property
    def init_kwargs(self):
        return {
            key: getattr(self, attr, None) for key, attr
            in self.signature_vars(vars(self)).items()
        }
    
    def __repr__(self):
        args = ', '.join(
            f"{key}='{str(val)}'"
            for key, val in self.init_kwargs.items()
        )
        return f"{self.__class__.__name__}({args})"

class Stock(AutoRepr):
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        
class Trade(AutoRepr):
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume

if __name__ == '__main__':      
    stock1 = Stock(
        'TSLA', date(2018, 11, 22), Decimal('338.19'),
        Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607
    )
    trade1 = Trade(
        'TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy',
        Decimal('338.25'), 100, Decimal('9.99')
    )
    print(stock1)
    print(trade1)