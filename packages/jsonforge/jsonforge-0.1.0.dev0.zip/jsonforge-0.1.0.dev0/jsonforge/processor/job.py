import pandas as pd
import logging

from attrdict import AttrDict

from .processor import FeedProcessor
from .output import FeedProcessorOutput

from .pipeline import FeedProcessorPipeline
from ..pipelines.css import CSS
from ..pipelines.jmespath import JMESPath
from ..pipelines.join import Join
from ..pipelines.unique import Unique
from ..pipelines.xpath import XPath
from ..pipelines.sqlite import SQLite
from ..pipelines.debug import Debug
from ..pipelines.nop import NOP

from ..helpers import tablecolumn
from ..helpers import dictproduct

logger = logging.getLogger(__name__)

classmap = {'css': CSS, 'jmespath': JMESPath, 'xpath': XPath, 'unique': Unique, 'sqlite': SQLite, 'join': Join,
            'debug': Debug}


class FeedProcessorJob(object):
    __slot__ = ('config', '_pipeline', 'result', 'datastore', 'stats')

    def __init__(self, cd, datastore=None):
        self.config = cd
        self._pipeline = None
        # "result" is the place where the result of this job is going to be collected. It's a Pandas DataFrame.
        # It gets filled in self.run()
        self.result = pd.DataFrame()
        self.datastore = datastore
        self.stats = AttrDict()

    @property
    def pipeline(self):
        if self._pipeline is None:
            p = FeedProcessorPipeline()
            if self.config.get("transform", None) is not None:
                for item in self.config["transform"]:
                    if item is None:
                        continue
                    k = list(item.keys())[0].lower()
                    v = list(item.values())[0]
                    if k in classmap:
                        p.append(classmap[k](v, job=self))
                    else:
                        logger.error(f"Unknown transform operator {k} in {self.config['name']}")
            else:
                p.append(NOP())
            self._pipeline = p
        return self._pipeline

    def run(self, limit=None, parameters=None, datastore=None):
        if parameters in (None, {}):
            pm = self.config.get("parameters", {})
        else:
            pm = parameters
        pme = dict()
        for (k, v) in pm.items():
            if type(v) not in (tuple, list):
                if v in datastore:
                    pme[k] = [a[1].to_dict() for a in datastore[v].result.iterrows()]
                else:
                    (table, column) = tablecolumn(v)
                    if table in datastore:
                        pme[k] = datastore[table].result[column]
                    else:
                        stores = ",".join(datastore.keys())
                        raise KeyError(
                            f"table {v} and {table} column {column} not in datastore. Avaliable datasets: {stores}.")
            else:
                pme[k] = v
        count = 1
        # import IPython
        # IPython.embed()
        iterations = dictproduct(pme)
        logger.debug("{}: starting {} iterations of {}-step processing pipeline".format(self, len(iterations),
                                                                                        len(self.pipeline)))
        # embed_ipython('check iterations')
        for data in FeedProcessor(self.config["source"], iterations, datastore=datastore):
            #
            # iterates over data source and accumulates results in self.result
            # result can be of "any" shape: list of lists/tuples/dicts, dict, list, tuple, scalar
            # can this be made more explicit?  See pipeline.py
            #
            #
            iresult = self.pipeline(data).json
            if len(iresult) > 0 and type(iresult) == list and type(iresult[0]) in (list, tuple, dict):
                # iresult is list of dicts
                ndf = pd.DataFrame(iresult)
            else:
                # iresult is one dict
                if type(iresult) == dict:
                    ndf = pd.DataFrame([iresult])
                # iresult is a list or a number
                else:
                    ndf = pd.DataFrame({self.config["name"]: iresult})
            # append to self.result
            self.result = self.result.append(ndf)
            # results are collected in a pandas DataFrame. Why is this a good idea? ... Hammer - Nail
            count = count + 1
            if limit is not None and count > limit:
                logger.info(f"Stopped after {count} jobs")
                break
        self.result.reset_index(inplace=True, drop=True)
        logger.debug("{} processed. Shape: {}. Columns: {}".format(
            self,
            self.result.shape,
            [c for c in self.result.columns]))
        (self.stats.rows, self.stats.columns) = self.result.shape
        return self.result

    def write(self, output=None):
        op = FeedProcessorOutput(self)
        count = 0
        for name, index in op.writables(output).items():
            op.write(name, index)
            count += 1
        self.stats.written = count

    def diagnose(self):
        if "check" in self.config:
            d = []
            for (k, v) in self.config["check"].items():
                if self.stats[k] < v:
                    d.append(f"{k} is {self.stats[k]} - should be {v}")
            if d:
                return (",".join(d))
            else:
                return False
        return None

    def __repr__(self):
        return f"<FeedProcessorJob {self.config['name']}>"
