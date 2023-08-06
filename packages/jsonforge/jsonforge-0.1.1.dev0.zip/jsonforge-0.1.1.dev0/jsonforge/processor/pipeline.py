import collections

from .textdata import TextData

class FeedProcessorPipeline(collections.UserList):
    def process(self, thing :TextData) -> TextData:
        result = thing
        for transformer in self.data:
            result = result.transform(transformer)
        # result can be of "any" shape: list of lists/tuples/dicts, dict, list, tuple, scalar
        # can this be made more explicit?
        return result

    __call__ = process
