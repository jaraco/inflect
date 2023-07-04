class ValidateCallWrapperWrapper:
    def __new__(cls, wrapped):
        # bypass wrapper if wrapped method has the fix
        if wrapped.__class__.__name__ != 'ValidateCallWrapper':
            return wrapped
        if hasattr(wrapped, '_name'):
            return wrapped
        return super().__new__(cls)

    def __init__(self, wrapped):
        self.orig = wrapped

    def __eq__(self, other):
        return self.raw_function == other.raw_function

    @property
    def raw_function(self):
        return getattr(self.orig, 'raw_function')


def same_method(m1, m2) -> bool:
    """
    Return whether m1 and m2 are the same method.

    Workaround for pydantic/pydantic#6390.
    """
    return ValidateCallWrapperWrapper(m1) == ValidateCallWrapperWrapper(m2)
