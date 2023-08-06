import jmespath
from jmespath import functions
import re
from collections import OrderedDict
import dateparser
import datetime
import hashlib
import operator
import random
import slugify


# taken from https://pypi.python.org/pypi/jmespath
# 1. Create a subclass of functions.Functions.
#    The function.Functions base class has logic
#    that introspects all of its methods and automatically
#    registers your custom functions in its function table.
class CustomFunctions(functions.Functions):
    # 2 and 3.  Create a function that starts with _func_
    # and decorate it with @signature which indicates its
    # expected types.
    # In this example, we're creating a jmespath function
    # called "unique_letters" that accepts a single argument
    # with an expected type "string".

    def __init__(self, context=None):
        super().__init__()
        self.context = context
        self.data = {}

    @functions.signature({'types': ['string']})
    def _func_param(self, s):
        return jmespath.search(s, self.context)

    @functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_store(self, s, var):
        self.data[var] = s
        return s

    @functions.signature({'types': ['string']})
    def _func_fetch(self, var):
        return self.data.get(var, None)

    @functions.signature({'types': ['string', 'number', 'null']}, {'types': ['string', 'null']})
    def _func_extract(self, s, pat):
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        ss = str(s)
        res = re.search(pat, ss)
        if res:
            if res.groupdict():
                return res.groupdict()
            elif res.groups():
                return res.groups()
            else:
                return res.group()
        else:
            return None

    @functions.signature({'types': ['string', 'number']}, {'types': ['string']})
    def _func_split(self, s, pat):
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        ss = str(s)
        return re.split(pat, ss)

    @functions.signature({'types': ['string', 'number']})
    def _func_slugify(self, s):
        ss = str(s)
        return slugify.slugify(ss, only_ascii=True)

    @functions.signature({'types': ['string']}, {'types': ['string']}, {'types': ['string']})
    def _func_replace(self, old, new, s):
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        ss = str(s)
        res = re.sub(old, new, s)
        return res

    @functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_split(self, s, pat):
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        res = re.split(pat, s)
        return res

    @functions.signature({'types': ['array']})
    def _func_unfold(self, s):
        # Given a list of Objects with { key: ..., value: ... }  return an
        # object { 'key' : 'value', ...}
        return OrderedDict([(a["key"], a["value"]) for a in s])

    @functions.signature({'types': ['array']}, {'types': ['expref']})
    def _func_group_by(self, o, expref):
        result = OrderedDict()
        for item in o:
            # embed_ipython("expref")
            k = expref.visit(expref.expression, item)
            if k in result:
                result[k].append(item)
            else:
                result[k] = [item]
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        return [{"key": a[0], "value": a[1]} for a in result.items()]

    @functions.signature({'types': ['object']})
    def _func_fold(self, s):
        return [{"key": a[0], "value": a[1]} for a in s.items()]

    @functions.signature({'types': ['string']})
    def _func_md5(self, s1):
        if s1 is None:
            return s1
        return hashlib.md5(s1.encode("utf-8")).hexdigest()

    @functions.signature({'types': ['string', 'null']})
    def _func_parseDate(self, s1):
        if s1 is None:
            return s1
        return dateparser.parse(s1).strftime("%Y-%m-%dT%H:%M:%S%z")

    @functions.signature()
    def _func_now(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

    @functions.signature({'types': ['number']}, {'types': ['number']})
    def _func_div(self, s1, s2):
        return operator.truediv(s1, s2)

    @functions.signature({'types': ['string', 'array']})
    def _func_random(self, s1):
        return random.choice(s1)

    @functions.signature({'types': ['string', 'array']}, {'types': ['number']})
    def _func_sample(self, s1, s2):
        return random.sample(s1, s2)

    @functions.signature({'types': ['object']}, {'types': ['array']})
    def _func_filterdict_by_keys(self, o1, a1):
        d = OrderedDict()
        for k in a1:
            d[k] = o1.get(k, None)
        return d

    @functions.signature({'types': ['string']}, {'types': ['array']})
    def _func_sort_array_to_dict(self, s1, a1):
        """
        sort an array of dicts to dict based on key in array-dict

        e.g.
        > sort_array_to_dict('some_key', [
                {"some_key": "a"},
                {"some_key": "b"}
                {"some_key": "b", "other_key": 1}
            ])

        # will result in
        {
            "a": [
                    {"some_key": "a"}
                ],
            "b": [
                    {"some_key": "b"},
                    {"some_key": "b", "other_key": 1}
                ]
        }

        :param s1: key
        :param a1: array
        :return: dict
        """
        d = OrderedDict()
        for element in a1:
            key = element[s1]
            # print('sorting element %s to key %s' % (element, key))
            if not d.get(key, False):
                d[key] = []
            d[key].append(element)
        return d

    # Given a string s, return a sorted
    # string of unique letters: 'ccbbadd' ->  'abcd'
    # Here's another example.  This is creating
    # a jmespath function called "my_add" that expects
    # two arguments, both of which should be of type number.
    #@functions.signature({'types': ['number']}, {'types': ['number']})
    #def _func_my_add(self, x, y):
    #    return x + y
