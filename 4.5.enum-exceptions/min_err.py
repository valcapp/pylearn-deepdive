# %%
from enum import Enum

class FriendlyEnum(Enum):
    def hello(self):
        print(self.name + ' says hello!')

MyEnum = type('MyEnum',
    (FriendlyEnum,),
    {'foo':1,'bar':2}
)

class MyEnum(FriendlyEnum):
    foo = 1
    bar = 2
MyEnum.foo.hello()

MyEnum.foo.hello()





# %%
