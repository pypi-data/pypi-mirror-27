import requests
import unittest
import json
from ruamel.yaml import YAML

from collections import OrderedDict
from unittest.mock import MagicMock
from unittest.mock import patch, mock_open

from feedprocessor.processor import textdata


class TestCsvLoader(unittest.TestCase):
    def test_csvloader(self):
        # with headers on line 0
        test_csv = b'a,b,c\n' \
                   b'aa,bb,cc\n'
        expected_result = [{'a': 'aa', 'b': 'bb', 'c': 'cc'}]
        loaded_data = textdata.csvloader(test_csv, dict(headers=0))
        self.assertEqual(loaded_data, expected_result)

        # empty line in csv
        test_csv = b'a,b,c\n' \
                   b'\n' \
                   b'aa,bb,cc\n'
        expected_result = [{'a': 'aa', 'b': 'bb', 'c': 'cc'}]
        loaded_data = textdata.csvloader(test_csv, dict(headers=0))
        self.assertEqual(loaded_data, expected_result)

        # no headline
        test_csv = b'aa,bb,cc\n'
        expected_result = [{0: 'aa', 1: 'bb', 2: 'cc'}]
        loaded_data = textdata.csvloader(test_csv, dict(headers=None))
        self.assertEqual(loaded_data, expected_result)


class TestTextdata(unittest.TestCase):
    source = 'source'
    client = requests.Session()
    content = 'content'
    etree = 'etree'
    json = dict()
    context = dict()

    def test_textdata_init(self):
        text_data = textdata.TextData(self.source, self.client, self.content, self.etree, self.json, self.context)
        self.assertTrue(text_data)

        self.assertEqual(text_data.source, self.source)
        self.assertEqual(text_data.client, self.client)
        self.assertEqual(text_data.content, self.content)
        self.assertEqual(text_data._etree, self.etree)
        self.assertEqual(text_data._json, self.json)
        self.assertEqual(text_data.context, self.context)

    def test_textdata_etree(self):
        teststr = 'test'
        content = f'<html>{teststr}</html>'

        text_data = textdata.TextData(
            source=self.source,
            client=self.client,
            content=content,
            etree=None,
            json=None,
            context=self.context)

        self.assertEqual(text_data.etree.text, teststr)

        # no text
        teststr = None
        content = '<html></html>'

        text_data = textdata.TextData(
            source=self.source,
            client=self.client,
            content=content,
            etree=None,
            json=None,
            context=self.context)

        self.assertEqual(text_data.etree.text, teststr)

    def test_textdata_json(self):
        teststr = 'test'
        content = f'<html>{teststr}</html>'

        # actually this is copied from a printed result. still ugly.
        expected_json = OrderedDict([
            ('html', OrderedDict(
                [
                    ('$t', 'test')
                ]))
        ])

        text_data = textdata.TextData(
            source=self.source,
            client=self.client,
            content=content,
            etree=None,
            json=None,
            context=self.context)

        self.assertEqual(text_data.json, expected_json)

    def test_textdata_content_http(self):
        mocked_client = requests.Session()
        mocked_client.get = MagicMock()

        fake_response = requests.Response()
        fake_response._content = 'fake_content'
        fake_response.headers = {'fake': True}
        fake_response.status_code = 23

        mocked_client.get = MagicMock(side_effect=[fake_response])

        test_url = 'http://some_url'
        text_data = textdata.TextData(
            source=test_url,
            client=mocked_client,
            content=None,
            etree=None,
            json=None,
            context=None)

        content = text_data.content

        mocked_client.get.assert_called_with(test_url)

        self.assertEqual(content, fake_response._content)
        self.assertEqual(text_data.headers, fake_response.headers)

    def test_textdata_content_local_json(self):
        test_source_file = 'some_file.json'
        test_text = '"some text"'
        test_json = '{"text": %s}' % test_text
        text_data = textdata.TextData(
            source=test_source_file,
            client=None,
            content=None,
            etree=None,
            json=None,
            context=None)

        # https://stackoverflow.com/questions/33650568/mock-open-function-used-in-a-class-method
        with patch('builtins.open', mock_open(read_data=test_json)) as m:
            content = text_data.content
            m.assert_called_with(test_source_file)
            self.assertEqual(text_data._json, json.loads(test_json))

    def test_textdata_content_local_yaml(self):
        test_source_file = 'some_file.json'
        test_text = '"some text"'
        test_yaml = """
        text:
            %s 
        """ % test_text
        text_data = textdata.TextData(
            source=test_source_file,
            client=None,
            content=None,
            etree=None,
            json=None,
            context=None)

        with patch('builtins.open', mock_open(read_data=test_yaml)) as m:
            content = text_data.content
            m.assert_called_with(test_source_file)
            self.assertEqual(text_data._json, YAML().load(test_yaml))
