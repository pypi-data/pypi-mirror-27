import re
import itertools
from typing import Union


def jsonshape(o: Union[list, object]) -> str:
    # todo: does this really need to return strings instead of an int?
    l = len(o)
    if hasattr(o, "keys"):
        return f"Object with {l} key/value pairs"
    else:
        return f"Array with {l} items"


def namify(s: str) -> str:
    """
    convert all whitespaces in a string to a regular space

    :param s:
    :return:
    """
    return re.sub(r"\s+", " ", s)


def tablecolumn(v):
    vs = v.split(".")
    return (".".join(vs[:-1]), vs[-1])


def dictproduct(dct: dict):
    return [dict(zip(dct.keys(), a)) for a in itertools.product(*dct.values())]
