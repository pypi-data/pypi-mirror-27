import jmespath
import logging

from ..helpers import jsonshape
from ..helpers import namify

from ..jpfunctions import CustomFunctions

logger = logging.getLogger(__name__)


class JMESPath(object):
    __slots__ = ('jmespath', 'compiled', 'job')

    def __init__(self, path, job=None):
        self.jmespath = path
        self.compiled = jmespath.compile(path)
        self.job = job

    def process_json(self, json, pcontext=None):
        shape = jsonshape(json)
        logger.debug(f"Processing {shape} json through {self} ")
        jpoptions = jmespath.Options(custom_functions=CustomFunctions(context=pcontext))
        result = self.compiled.search(json, options=jpoptions)
        # embed_ipython()
        if result is None:
            result = []
        return result

    def __repr__(self):
        return "<JMESPath '{}...'>".format(namify(self.jmespath[:20]))
