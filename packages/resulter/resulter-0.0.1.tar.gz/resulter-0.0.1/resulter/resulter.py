class Result:
    __slots__ = ('value', 'status')

    def __init__(self, status, value=None):
        self.value = value
        self.status = status

    def __repr__(self):
        return 'Result: status: {0}; value: {1}'.format(self.status, self.value)

    def is_ok(self):
        return self.status

    __str__ = __repr__


def ok(value=None):
    return Result(status=True, value=value)


def error(value=None):
    return Result(status=False, value=value)


def resultify(f):
    def wrap_call(*args, **kwargs):
        try:
            return ok(f(*args, **kwargs))
        except Exception as e:
            return error(e)

    return wrap_call
