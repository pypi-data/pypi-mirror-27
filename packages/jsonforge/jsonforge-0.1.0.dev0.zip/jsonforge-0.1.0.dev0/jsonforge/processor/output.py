import datetime
import collections
import logging

from .storage import Store

logger = logging.getLogger(__name__)


class FeedProcessorOutput(object):
    __slots__ = ('processor')

    def __init__(self, processor):
        self.processor = processor

    def writables(self, output=None):
        now = datetime.datetime.now()
        if output is None:
            to = self.processor.config["output"]["name"]
        else:
            to = output
        if to.find("{") == -1:
            # only one name t write to
            return {to: range(0, len(self.processor.result))}
        else:
            filenames = collections.defaultdict(lambda: [])
            for (i, item) in enumerate(self.processor.result.iterrows()):
                lu = item[1].to_dict()
                if len(lu.keys()) == 1 and type(list(lu.values())[0]) == dict :
                    lu = list(lu.values())[0]
                try :
                    fn = to.format(now=now, **collections.ChainMap(lu, self.processor.config))
                except Exception as e:
                    from IPython import embed
                    embed()
                filenames[fn].append(i)
                # logger.debug(f"{i} for {fn}")
            # embed_ipython("writimg to filenames!")
            return filenames

    def write(self, name, index):
        processor = self.processor
        mode = self.processor.config['output'].get('mode', 'replace')
        index = index

        Store.write(name, mode, index, processor)
