from decimal import Decimal
from datetime import date, datetime
import json
import functools
from classes import Stock, Trade
from example import activity

@functools.singledispatch
def custom_dumps(arg)->str:
    return str(arg)

@custom_dumps.register(Decimal)
def _(arg:Decimal)->str:
    return f"Decimal({str(arg)})"

@custom_dumps.register(date)
def _(arg:date)->str:
    return {'class_date': arg.isoformat()}

@custom_dumps.register(datetime)
def _(arg:datetime)->str:
    return {'class_datetime': arg.isoformat()}

@custom_dumps.register(Stock)
def _(arg:Stock)->str:
    return {'class_stock': vars(arg)}

@custom_dumps.register(Trade)
def _(arg:Trade)->str:
    return {'class_trade': vars(arg)}

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, 'indent': 2})
    
    def default(self, arg):
        return custom_dumps(arg)


if __name__ == '__main__':  
    result1 = json.dumps(activity, default=custom_dumps, indent=2)
    result2 = json.dumps(activity, cls=CustomJSONEncoder)

    print(result1)
    print(result1 == result2)
    with open('activity_1.json', 'w', newline='') as file:
        file.write(result1)
    with open('activity_2.json', 'w', newline='') as file:
        file.write(result2)