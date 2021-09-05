from decimal import Decimal
from datetime import date, datetime
import json
import functools
from classes import Stock, Trade
from encode import CustomJSONEncoder
from example import activity

from marshmallow import Schema, fields, post_load


class StockSchema(Schema):
    symbol= fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Int()
    
    @post_load
    def make_stock(self, data, **kwargs):
        # init_keys = Stock.vars_signature(data)
        # init_kwargs = { init_keys[k]: v for k, v in data.items()}
        # return Stock(**init_kwargs)
        for dict_key, kwarg_key in Stock.vars_signature(data).items():
            data[kwarg_key] = data.pop(dict_key)
        return Stock(**data)

class TradeSchema(Schema):
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal(as_string=True)
    commission = fields.Decimal(as_string=True)
    volume = fields.Int()
    
    @post_load
    def make_trade(self, data, **kwargs):
        return Trade(**data)

class ActivitySchema(Schema):
    quotes = fields.Nested(StockSchema, many=True)
    trades = fields.Nested(TradeSchema, many=True)

if __name__ == '__main__':
    from pprint import pprint
    # pprint(activity) 
    activity_schema = ActivitySchema()
    encoded = activity_schema.dumps(activity)
    print(encoded)
    decoded = activity_schema.loads(encoded)
    print(decoded)