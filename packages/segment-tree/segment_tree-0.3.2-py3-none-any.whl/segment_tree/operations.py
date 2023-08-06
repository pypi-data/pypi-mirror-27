class Operation:
    def __init__(self, name, function, function_on_equal):
        self.name = name
        self.f = function
        self.f_on_equal = function_on_equal


def add_multiple(x, count):
    return x * count


def min_multiple(x, count):
    return x


def max_multiple(x, count):
    return x


sum_operation = Operation("sum", sum, add_multiple)
min_operation = Operation("min", min, min_multiple)
max_operation = Operation("max", max, max_multiple)
