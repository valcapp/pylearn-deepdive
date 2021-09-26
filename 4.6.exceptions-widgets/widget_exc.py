from http import HTTPStatus

import json
import logging
import traceback

logging.basicConfig(
    format='%(name)s:%(levelname)s: %(asctime)s: %(message)s',
    level=logging.DEBUG
)

class WidgetException(Exception):
    """ Main Exception type for backend API application"""
    logger = logging.getLogger('widget-exception')
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_msg = "Exception of application widget"
    user_msg = "Something went wrong with application widget"
    
    def __init__(self, *args, user_msg = None)->None:
        if args:
            self.internal_msg = args[0]
            super().__init__(*args)
        else:
            super().__init__(self.internal_msg)
        
        if user_msg is not None:
            self.user_msg = user_msg
    
    @property
    def json(self)->str:
        return json.dumps({
            'status': self.status,
            'message': self.user_msg
        })
    
    @property
    def report(self)->dict:
        return {
            'type': type(self).__name__,
            'status': self.status.value,
            'message': self.internal_msg,
            'args': self.args,
            'traceback': traceback.format_exc()
        }
    
    def log(self)->None:
        self.logger.error(self.report)

"""
1. Supplier exceptions
    a. Not manufactured anymore
    b. Production delayed
    c. Shipping delayed
    
2. Checkout exceptions
    a. Inventory type exceptions
        - out of stock
    b. Pricing exceptions
        - invalid coupon code
        - cannot stack coupons
"""
        
if __name__ == '__main__':
    try:
        raise WidgetException('hello')
    except WidgetException as we:
        print(we.json)
        we.log()