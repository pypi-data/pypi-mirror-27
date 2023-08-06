class Debug(object):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def process_object(self, other, **kwargs):
        current = other
        import IPython
        IPython.embed()
        return other
