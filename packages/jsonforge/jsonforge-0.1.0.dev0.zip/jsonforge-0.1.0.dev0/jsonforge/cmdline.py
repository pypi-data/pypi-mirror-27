#!/usr/bin/env python

import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s')

from jsonforge import FeedProcessorJob
from jsonforge.processor.storage import Store

import ruamel.yaml
import fire
import re

logger = logging.getLogger(__name__)


def cmdline(config=None, datasets=".*", output=None, limit=None, parameters={}, loglevel='DEBUG', batch=False):
    try:
        loglevelno = getattr(logging, loglevel)
    except AttributeError:
        print(f"Loglevel {loglevel} not defined")
        loglevelno = logging.DEBUG
    logging.getLogger('').setLevel(loglevelno)
    if config is None :
        import sys
        logger.debug(f"please use {sys.argv[0]} -- --help")
        sys.exit()
    logger.info(f"Loading {config}")
    config = Store.read(config)  # ruamel.yaml.safe_load(open(config))
    to_do = [a for a in config["datasets"] if re.search(datasets, a["name"])]
    datastore = {}
    logger.info("Jobs to do: {}".format(",".join((a["name"] for a in to_do))))
    for jd in to_do:
        try:
            name = jd["name"]
            datastore[name] = FeedProcessorJob(jd, datastore=datastore)
            logger.debug(f"starting {datastore[name]}")
            datastore[name].run(limit=limit, parameters=parameters, datastore=datastore)
            datastore[name].write(output)
        except Exception as e:
            logger.exception(e)
            logger.error(f"{datastore[name]} failed: {e}")
            if not batch:
                sys.exit()
        else:
            d = datastore[name].diagnose()
            if d:
                logger.error(f"{datastore[name]}: {d}")
            else:
                logger.info(f"{datastore[name]} finished")

def run() :
    fire.Fire(cmdline)


