from feedprocessor import helpers

import unittest


class TestHelpers(unittest.TestCase):
    def test_jsonshape(self):
        test_array = [1, 1]
        self.assertEqual(helpers.jsonshape(test_array), 'Array with 2 items')

        test_obj = {1: 1,
                    2: 2}
        self.assertEqual(helpers.jsonshape(test_obj), 'Object with 2 key/value pairs')

    def test_namify(self):
        test_strings = {
            "some random string": "some random string",
            "string with    tabs": "string with tabs",  # makes tabs to whitespace
            """test
            123""": "test 123",
            "two  whitespaces": "two whitespaces"
        }
        for k, v in test_strings.items():
            self.assertEqual(helpers.namify(k), v)

    def test_tablecolumn(self):
        # todo
        self.assertTrue(True)

    def test_dictproduct(self):
        # todo
        self.assertTrue(True)

