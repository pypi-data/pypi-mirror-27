class NOP(object):
    __slots__ = ()

    def process_object(self, other):
        return other
