from ruamel.yaml import YAML

from collections import OrderedDict
from unittest.mock import MagicMock
from unittest.mock import patch, mock_open

from feedprocessor.processor.storage.local import LocalStore
from feedprocessor.processor.processor import FeedProcessor

import unittest

class TestLocalStore(unittest.TestCase):
    def test_write(self):
        test_path = 'some/path.ext'
        test_mode = 'upsert'
        index = 1
        #processor = FeedProcessor()
        #LocalStore.write('')
        pass

    # todo
