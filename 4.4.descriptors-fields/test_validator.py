import pytest

from validator import RangeValidator, IntegerField, CharField

from functools import total_ordering
from dataclasses import dataclass
from math import sqrt
from numbers import Number

@total_ordering
@dataclass
class Pt2D:
    x: Number
    y: Number
    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)
    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and abs(self) == abs(other)
        )
    def __lt__(self, other):
        return (
            isinstance(other, type(self))
            and abs(self) < abs(other)
        )

inits = (
    (0,10),
    (5, 20),
    # ('abc','defg'),
    # (Pt2D(0,3),Pt2D(1,6.)),
)

@pytest.mark.parametrize('init',inits)
class TestRangeValidator:
    def test_init(self, init):
        vmin, vmax = init
        vtor = RangeValidator(vmin, vmax)
        assert vtor.min == vmin
        assert vtor.max == vmax

    def test_get(self,init):
        vtor = RangeValidator(*init)
        class Obj:
            field = vtor
        obj = Obj()
        assert Obj.field is vtor
        # assert obj.field is None
    
    def test_set(self, init):
        vtor = RangeValidator(*init)
        class Obj:
            field = vtor
        obj = Obj
        obj.field = init[0]+1
        assert obj.field == init[0]+1
        # assert Obj.field is vtor



if __name__ == '__main__':
    TestRangeValidator().test_get([1,10])

