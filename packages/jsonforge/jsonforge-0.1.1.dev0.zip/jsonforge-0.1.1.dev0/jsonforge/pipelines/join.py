import collections
import logging
import re

from attrdict import AttrDict

logger = logging.getLogger(__name__)


class Join(object):
    __slots__ = ('param', 'job')

    _parse = re.compile(r"(?P<table>[^ ]+) +on +(?P<column>[^ ]+) +as +(?P<property>[^ ]+)")

    def __init__(self, param, job=None):
        param = Join._parse.search(param)
        if param is None:
            raise ValueError(f"Join argument '{other}' does not match <table> on <column> as <property>")
        else:
            self.param = AttrDict(param.groupdict())
        self.job = job

    def process_json(self, json, pcontext=None):
        table = self.job.datastore[self.param.table].result
        index = collections.defaultdict(lambda: [])
        if self.param.column not in table.columns:
            l = ",".join(table.columns)
            raise ValueError(f"{self.param.column} not in columns: {l}")
        for (i, k) in table[self.param.column].iteritems():
            index[k].append(i)
        count = 0
        obs = 0
        for item in json:
            lookup = item.get(self.param.column, None)
            if lookup in index:
                count += len(index[lookup])
                obs += 1
                ob = table.iloc[index[lookup]]
                if len(ob) == 1:
                    item[self.param.property] = ob.iloc[0].to_dict()
                else:
                    item[self.param.property] = [a[1] for a in ob.to_records()]
            else:
                logger.debug(
                    f"Join: Lookup for {lookup} (value of column {self.param.column}) failed in {self.param.table}")
        logger.debug(f"Join: added {count} objects to the {self.param.property} property of {obs} items")
        return json

    def __repr__(self):
        return "<Join {table} on {column} as {property}>".format(**self.param)
