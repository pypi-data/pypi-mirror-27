import requests
import copy
import logging

from .textdata import TextData

logger = logging.getLogger(__name__)


class FeedProcessor(object):
    __slots__ = ('client', 'template', 'values', 'datastore', 'hints')

    def __init__(self, template, values=[{}], headers={}, datastore={}):
        self.client = requests.Session()
        if hasattr(template, 'keys') and 'url' in template:
            self.template = template['url']
            self.hints = template
        else:
            self.template = template
            self.hints = {}
        self.values = values
        self.client.headers.update(headers)
        self.datastore = datastore

    def get(self, source):
        return self.client.get(source)

    def __iter__(self):
        for v in self.values:
            try:
                current = self.template.format(**v)
            except KeyError as e:
                raise KeyError(f"{self.template} not filled, missing Key: {e}. Available keys: {v}")

            vhere = copy.deepcopy(v)
            vhere.update(self.hints)

            if current in self.datastore:
                logger.debug(f"New TextData object from internal dataset {current}")
                df = self.datastore[current].result
                v.update(self.hints)
                a = TextData(client=self, source=current, context=vhere,
                             json=[a[1].to_dict() for a in df.iterrows()])
                yield (a)

            else:
                logger.debug(f"New lazy TextData object from source {current}, context {v}")
                yield TextData(client=self, source=current, context=vhere)
