class RangeValidator:
    def __init__(self, min_val:int = None, max_val:int = None)->None:
        self.check_init_types(min_val, max_val)
        self.min = min_val
        self.max = max_val
    
    def check_init_types(self, min_val, max_val):
        pass
    
    def eval(self, value):
        return value
    
    def is_below_min(self, val)->bool:
        return (
            self.min is not None
            and val < self.min
        )
    
    def is_above_max(self, val)->bool:
        return (
            self.max is not None
            and val > self.max
        )
    
    def check_type(self, value)->None:
        pass
    
    def check_range(self, value)->None:
        evaluated = self.eval(value)
        base_msg = f'Value was evaluated out of range: {evaluated}s; '
        if self.is_below_min(evaluated):
            raise ValueError(base_msg + f"must be >= {self.min}")
        if self.is_above_max(evaluated):
            raise ValueError(base_msg + f"must be <= {self.max}")

    def __set_name__(self, owner, name)->None:
        self.name = name
    
    def __set__(self, instance, value)->None:
        self.check_type(value)
        self.check_range(value)
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner)->object:
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

class TypedRangeField(RangeValidator):
    def check_init_types(self, min_val, max_val)->None:
        super().check_init_types(min_val, max_val)
        for val in min_val, max_val:
            if not (isinstance(val,int) or val is None):
                raise TypeError(
                    f"Min and Max values should be either None or int types. Not: '{type(val)}'"
                )

class IntegerField(TypedRangeField):
    def check_type(self, value) -> None:
        super().check_type(value)
        if not isinstance(value, int):
            raise TypeError(
                f"Value must be of type int. not '{type(value)}'"
            )

class CharField(TypedRangeField):
    def check_type(self, value)->None:
        super().check_type(value)
        if not isinstance(value, str):
            raise TypeError(
                f"Value must be of type str, not '{type(value)}'"
            )

    def eval(self, value)->int:
        return len(value)



