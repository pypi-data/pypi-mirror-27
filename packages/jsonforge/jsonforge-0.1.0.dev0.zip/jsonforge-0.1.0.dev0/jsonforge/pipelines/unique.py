import jmespath
import logging
import json

from ..jpfunctions import CustomFunctions
from ..helpers import namify

logger = logging.getLogger(__name__)


class Unique(object):
    __slots__ = ('jmespath', 'compiled', 'job', 'seen')

    def __init__(self, path=None, job=None):
        self.jmespath = path
        if path is not None:
            try:
                self.compiled = jmespath.compile(path)
            except jmespath.exceptions.EmptyExpressionError:
                self.compiled = None
        else:
            self.compiled = None
        self.job = job
        self.seen = set()

    def process_json(self, jsonobj, pcontext=None):
        logger.debug(f"Processing json through {self}")
        jpoptions = jmespath.Options(custom_functions=CustomFunctions(context=pcontext))
        result = []
        for item in jsonobj:
            if self.compiled is not None:
                key = json.dumps(self.compiled.search(json, options=jpoptions))
            else:
                key = json.dumps(item)
            if not key in self.seen:
                result.append(item)
                self.seen.add(key)
        return result

    def __repr__(self):
        return "<Unique '{}...'>".format(namify(self.jmespath[:20]))
