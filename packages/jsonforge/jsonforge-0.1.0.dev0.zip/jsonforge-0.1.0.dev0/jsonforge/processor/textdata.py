import requests
import lxml
import logging
import collections
import simplejson
import json
import ruamel.yaml
import os
import pandas as pd
from typing import Union

from urllib.parse import urlparse
from xmljson import gdata

logger = logging.getLogger(__name__)


def csvloader(content: bytes, context={}) -> list:
    import io

    # make pd-table
    df = pd.read_csv(io.BytesIO(content), header=context.get('headers', 0))
    df = df.fillna('')

    # set index names
    # todo:
    #  @martin: i dont really get the if-statement.
    #           needs documentation about the context-object.
    if context.get("objects", "").find('colum') == 0:  # colum_n_ ?
        iname = context.get('index', df.columns[0])
        df = df.set_index(iname).transpose().reset_index().rename(columns={'index': iname})

    # todo:
    #  @martin: according to
    #           https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    #           read_csv´s "skip_blank_lines" defaults to true.
    #           (also, k > 0 breaks if we have non-strings in the data)
    # return [{k: v for (k, v) in a[1].to_dict().items() if k > "" and v > ""} for a in df.iterrows()]
    return [a[1].to_dict() for a in df.iterrows()]


class TextData(object):
    """
    TextData objects come from the Internet and can be transformed using XPath and CSS into arbitrary
    record-oriented data structures that can in turn be transformed using JMESPath (and SQL,untested)
    and then written as JSON files or potentially any other format supported by Pandas.

    """
    __slots__ = ('_content', '_json', '_etree', 'headers', 'client', 'source', 'context')
    dataloadermap = {'text/csv': csvloader}

    def __init__(self,
                 source: str = None,
                 client: requests.Session = None,
                 content=None,
                 etree=None,
                 json: Union[dict, list] = None,
                 context: dict = None):

        if hasattr(content, "headers"):
            self.headers = content.headers
        else:
            self.headers = {}

        if hasattr(content, "content"):
            self._content = content.content
        else:
            self._content = content

        self._json = json
        self._etree = etree

        if client is None:
            self.client = requests.Session()
        else:
            self.client = client

        self.source = source
        self.context = context

    @property
    def etree(self):
        if self._etree is None:
            try:
                self._etree = lxml.etree.XML(self.content)
            except lxml.etree.XMLSyntaxError as e2:
                logger.debug(f"Falling back to HTML (XML decoding Error: {e2})")
                self._etree = lxml.etree.HTML(self.content)
        return self._etree

    @property
    def json(self):
        # embed_ipython("Let's do JSON",banner2='')
        if self._json is None:
            if self._etree is None:
                param = collections.ChainMap(self.headers, self.context)
                ct = param.get("content-type", None)
                # embed_ipython("content?")
                if ct in self.dataloadermap:
                    self._json = self.dataloadermap[ct](self.content, context=self.context)
                else:
                    try:
                        self._json = simplejson.loads(self.content)
                    except (simplejson.decoder.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(f"Falling back to XML or HTML. (JSON decoding failed: {e})")
                        self._json = gdata.data(self.etree)
            else:
                self._json = gdata.data(self.etree)
        return self._json

    @property
    def content(self):
        # todo:
        #  if no scheme and ext == (yaml|json|aml..) self._content is never set!
        if self._content is None:
            logger.debug(f"{self}: retrieving {self.source}")
            scheme = urlparse(self.source).scheme
            if scheme in ('http', 'https'):
                response = self.client.get(self.source)
                self._content = response.content
                self.headers = response.headers
                logger.debug(f"{self}: Returned Status Code {response.status_code}")

            elif scheme == '':
                ext = os.path.splitext(self.source)[1]
                if ext in ('.json', '.yml', '.yaml'):
                    with open(self.source) as f:
                        self._json = ruamel.yaml.safe_load(f)
                elif ext in ('.aml', '.archieml'):
                    import archieml
                    self._json = archieml.load(open(self.source))
                else:
                    with open(self.source, "rb") as f:
                        self._content = f.read()
        return self._content

    def transform(self, other):
        #
        # idea: generic "TextDataTransformer" abstract class that chooses how to transform
        #
        if hasattr(other, "process_etree"):
            return TextData(etree=other.process_etree(self.etree, pcontext=self.context), context=self.context)
        if hasattr(other, "process_json"):
            return TextData(json=other.process_json(self.json, pcontext=self.context), context=self.context)
        if hasattr(other, "process_object"):
            return other.process_object(self)
        raise ValueError(f"{other} does not provide a way to process {self} via process_etree, process_json or "
                         f"process_object")

    def __repr__(self):
        try:
            cl = "%s bytes" % len(self._content)
        except Exception as e:
            cl = None
        try:
            if self._etree is not None:
                xl = "%s bytes" % len(lxml.etree.tostring(self._etree))
            else:
                xl = None
        except Exception as e:
            xl = None
        try:
            if self._json is not None:
                jl = "%s bytes" % len(simplejson.dumps(self._json))
            else:
                jl = None
        except Exception as e:
            jl = None
        return f"<TextData {self.source} {cl} content, {xl} xml, {jl} json>"
