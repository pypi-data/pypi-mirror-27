import os
import sys
import json
import collections
import logging
import jmespath
import typing

from typing import Union
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


def default_json_dump(o: Union[dict, list], output_file: Union[typing.TextIO, typing.BinaryIO], kwargs={}):
    _kwargs = {**dict(allow_nan=False, ensure_ascii=False), **kwargs}
    try:
        json.dump(o, output_file, **_kwargs)
    except ValueError as e:
        logger.error(f'could not write file {output_file.name}: {e}')
        raise
        ##  logger.error(f'trying to dump file without flags: {json.dumps(o)}')


class LocalStore():
    @staticmethod
    def write(name, mode, index, processor):
        if mode == 'upsert' and not os.path.exists(name):
            mode = 'replace'
        if mode == 'replace':
            if name == "-":
                ofile = sys.stdout
            else:
                (d, p) = os.path.split(name)
                if len(d) > 0:
                    os.makedirs(d, exist_ok=True)
                if os.path.exists(name):
                    logger.debug(f"{processor}: file {name} will be overwritten")
                ofile = open(name, "w")
            # embed_ipython()
            if len(processor.result.columns) == 1 and len(processor.result) > 1:
                logger.debug(f"{processor} one column only - writing list")
                default_json_dump(list(processor.result.iloc[index, 0]), ofile)

            else:
                # embed_ipython()
                if len(index) == 1:
                    default_json_dump(processor.result.iloc[index, :].iloc[0].to_dict(), ofile)
                    logger.info("{}: single record written to {}".format(processor, ofile.name))
                else:
                    processor.result.iloc[index, :].to_json(ofile, 'records')
                    logger.info("{}: {} records written to {}".format(processor, len(index), ofile.name))
        if mode == 'upsert':
            if name == "-":
                raise ValueError(f"{mode} does not work with stdout")
            else:
                key = processor.config['output']['key']
                keyf = jmespath.compile(key)
                indexed = collections.OrderedDict(((json.dumps(keyf.search(a)), a) for a in json.load(open(name))))
                old_len = len(indexed.keys())
                logger.debug(f"read {old_len} existing records from {name}")
                for row in processor.result.iloc[index, :].iterrows():
                    rrow = row[1]
                    if len(rrow) == 1:
                        rrow = rrow[0]
                    else:
                        rrow = rrow.to_dict()
                    key = json.dumps(keyf.search(rrow))
                    indexed[key] = rrow
                # embed_ipython("check indexed ;-)")
                new_len = len(indexed.keys())
                fdir, fname = os.path.split(name)
                with NamedTemporaryFile(dir=fdir,
                                           prefix="{}.".format(fname),
                                           mode="w",
                                           delete=False) as sfile:
                    default_json_dump(list(indexed.values()), sfile)

                bakfile = "{}.bak".format(name)
                try:
                    os.remove(bakfile)
                except FileNotFoundError:
                    pass
                try:
                    os.rename(name, bakfile)
                except FileNotFoundError:
                    pass
                os.rename(sfile.name, name)
                logger.info("{new_len} records written to {name}. Old length was {old_len}, upserted {} records "
                            .format(len(index), **locals()))

    @staticmethod
    def read(path):
        import ruamel.yaml
        with open(os.path.abspath(path)) as f:
            obj = ruamel.yaml.safe_load(f)
        return obj
