import os
import logging

from .jpfunctions import CustomFunctions

if not "AWS_DEFAULT_REGION" in os.environ:
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"

logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

from .processor.processor import FeedProcessor
from .processor.job import FeedProcessorJob


def test_current():
    source = 'http://emm.newsbrief.eu/rss?type=rtn&language=de&duplicates=false'
    fp = FeedProcessor()
    return fp.json(source)


def test_rss():
    source = 'http://emm.newsbrief.eu/rss?type=story&id=peiner-nachrichten-03f6043d1e68ad47b011086fb5079b18.20171104.de&duplicates=false'
    fp = FeedProcessor(source=source)
    return fp.get(source)


def test_html():
    source = "http://emm.newsbrief.eu/NewsBrief/clusteredition/en/latest_de.html"
    fp = FeedProcessor(source=source)
    return fp.get(source)


if __name__ == "__main__":
    source = "http://emm.newsbrief.eu/NewsBrief/clusteredition/en/latest_{lang}.html"
    values = [dict(lang=a) for a in ('de', 'en', 'es', 'fr', 'it')]
    fp = FeedProcessor(source, values)
