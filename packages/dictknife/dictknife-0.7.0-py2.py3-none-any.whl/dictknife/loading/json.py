from collections import OrderedDict
from ._lazyimport import m


def load(fp, *, loader=None):
    return m.json.load(fp, object_pairs_hook=OrderedDict)


def dump(d, fp):
    return m.json.dump(d, fp, ensure_ascii=False, indent=2, default=str)
