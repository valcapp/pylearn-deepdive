import pytest

import widget_exc as wex
import inspect
widget_exceptions = inspect.getmembers(wex,
    lambda kls: (
        inspect.isclass(kls)
        and issubclass(kls, wex.WidgetException)
    )
)

import json
from http import HTTPStatus
import traceback

def pick_status(exc_class:type)->dict:
    default = HTTPStatus.INTERNAL_SERVER_ERROR
    alternative = HTTPStatus.BAD_REQUEST
    alternative_excs = (
        wex.InvalidCouponCodeException,
        wex.CannotStackCouponException,
    )
    return (
        alternative
        if exc_class in alternative_excs
        else default
    )
    
def make_tcase(exc_class:type, **kwargs)->dict:
    return {
        'exc': exc_class,
        'args': ('hello',),
        'user_msg': 'sorry user, I am exceptional',
        'status': pick_status(exc_class),
        **kwargs
    }
    
tcases = tuple(
    make_tcase(exc_class)
    for exc_name, exc_class
    in widget_exceptions
)

@pytest.mark.parametrize('tcase', tcases)
class TestWidgetException:
    """Tests WidgetException"""
    def get_we(self, tcase:dict)->wex.WidgetException:
        kwargs = {
            k:tcase[k]
            for k in ('user_msg',)
            if k in tcase
        }
        return tcase['exc'](
            *tcase['args'],
            **kwargs
        )
    
    def test_init(self, tcase):
        we = self.get_we(tcase)
        assert we.status == tcase['status']
        assert we.internal_msg == tcase['args'][0]
        assert we.user_msg == tcase['user_msg']
    
    def test_log(self, tcase, monkeypatch):
        we = self.get_we(tcase)
        testlog = {}
        def record_error(err_report):
            testlog['error'] = err_report
            
        with monkeypatch.context() as patch:
            patch.setattr(we.logger, "error", record_error)
            we.log()
            assert testlog['error'] == we.report
    
    def test_report(self, tcase):
        report = self.get_we(tcase).report
        assert report['type'] == tcase['exc'].__name__
        assert report['status'] == tcase['status'].value
        assert report['message'] == tcase['args'][0]
        assert report['traceback'] == traceback.format_exc()
    
    def test_json(self, tcase):
        assert (
            self.get_we(tcase).json
            == json.dumps({
                'status': tcase['status'].value,
                'message': tcase['user_msg']
            })
        )

if __name__ == '__main__':
    # [print(w) for w in widget_exceptions]
    pytest.main()