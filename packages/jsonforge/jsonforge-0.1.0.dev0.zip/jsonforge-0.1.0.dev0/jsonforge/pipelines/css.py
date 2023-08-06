import lxml
import copy
import logging

from pyquery import PyQuery

logger = logging.getLogger(__name__)


class CSS(object):
    __slots__ = ('cssdescriptor', 'job')

    def __init__(self, cssdescriptor, job=None):
        self.cssdescriptor = cssdescriptor
        self.job = job

    def process_etree(self, etree, pcontext=None):
        logger.debug(f"Processing etree through {self}")
        result = PyQuery(etree)(self.cssdescriptor)
        root = lxml.etree.Element(etree.tag)
        for element in result:
            root.append(copy.deepcopy(element))
        return root

    def __repr__(self):
        return f"<CSS '{self.cssdescriptor}'>"
