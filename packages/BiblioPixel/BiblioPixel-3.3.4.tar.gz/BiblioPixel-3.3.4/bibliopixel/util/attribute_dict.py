class AttributeDict(object):
    """A dict that exposes its values as attributes."""

    def __init__(self, *args, **kwds):
        for k, v in dict(*args, **kwds).items():
            setattr(self, k, v)

    def __setattr__(self, k, v):
        if isinstance(v, dict):
            v = AttributeDict(**v)
        super().__setattr__(k, v)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __bool__(self):
        return bool(self.__dict__)
