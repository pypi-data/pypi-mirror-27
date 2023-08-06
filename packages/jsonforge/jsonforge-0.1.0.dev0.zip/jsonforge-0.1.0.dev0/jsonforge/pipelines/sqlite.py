import dataset
import logging

from ..helpers import namify

logger = logging.getLogger(__name__)


class SQLite(object):
    __slots__ = ('query', 'job')

    def __init__(self, query, job=None):
        self.query = query
        self.job = job

    def process_json(self, json, pcontext=None):
        logger.debug(f"Processing json through {self}")
        engine = dataset.connect("sqlite://")
        table = engine[self.id]
        try:
            table.insert_many(json)
        except Exception as e:
            raise ValueError(f"{self}: failed to insert json into sqlite table: {e}")
        if self.job is None:
            qk = {}
        else:
            qk = self.job.datastore
        query = self.query.format(self="`%s`" % self.id, **qk)

        try:
            result = list(engine.query(query))
        except Exception as e:
            raise SyntaxError(f"{self}: {query} failed: {e}")
        if result is None:
            result = []
        return result

    def __repr__(self):
        return "<SQLite '{}...'>".format(namify(self.query[:20]))

    @property
    def id(self):
        return "id%s" % str(id(self))
