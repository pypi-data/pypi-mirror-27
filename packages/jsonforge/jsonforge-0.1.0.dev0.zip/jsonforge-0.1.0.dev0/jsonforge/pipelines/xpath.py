import lxml
import logging
import copy

logger = logging.getLogger(__name__)


class XPath(object):
    __slots__ = ('xpathdescriptor', 'job')

    def __init__(self, xpathdescriptor, job=None):
        self.xpathdescriptor = xpathdescriptor
        self.job = job

    def process_etree(self, etree, pcontext=None):
        logger.debug(f"Processing etree through {self}")
        result = etree.xpath(self.xpathdescriptor)
        root = lxml.etree.Element(etree.tag)
        for element in result:
            root.append(copy.deepcopy(element))
        return root

    def __repr__(self):
        return f"<XPath '{self.xpathdescriptor}'>"
