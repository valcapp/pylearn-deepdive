from decimal import Decimal
from datetime import date, datetime
import json
import functools
from classes import Stock, Trade
from encode import CustomJSONEncoder
from example import activity

import re

decimal_re = re.compile('Decimal\(.+\)')

def my_hook(arg):
    # print('\n\nreading:', type(arg), arg)
    for key, val in arg.items():
        if isinstance(val,str) and decimal_re.match(val):
            arg.update({key: Decimal(val.strip(' Decimal(\')'))})
    for label, Class in (
            ('class_date', date),
            ('class_datetime', datetime)
        ):
        if label in arg:
            return Class.fromisoformat(arg[label])
    for label, Class in (
            ('class_stock', Stock),
            ('class_trade', Trade)
        ):
        if label in arg:
            kwargs = arg[label]
            init_map = Class.vars_signature(kwargs)
            return Class(**{init_map[k]:v for k,v in kwargs.items()})
    else:
        return arg

class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        return json.loads(arg, object_hook=my_hook)

if __name__ == '__main__':
    # val = "Decimal('1.344')"
    # if decimal_re.match(val):
    #     dec1 = Decimal(val.strip(' Decimal(\')'))
    #     print(dec1)
    encoded = json.dumps(activity, cls=CustomJSONEncoder)
    # decoded = json.loads(encoded, object_hook=my_hook)
    decoded = json.loads(encoded, cls=CustomDecoder)
    print(decoded)