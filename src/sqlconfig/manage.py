"""\
This submodule is to be used to **edit** the data (configuration credentials)

In this module docstrings, allowed means it is present in the list of values in
the file `allowed_args.json`.
"""
import json
from typing import Any
from . import load

def dict_has_only_allowed_values(d : dict) -> bool:
    """\
If d has only values that are allowed,
return True.
else,
return False"""
    return all((x in load.load_allowed(1)) for x in d)


def fileisemtpy():
    """Tell if `sqlcredentails` is empty or not"""
    return not not load.load_data(0).replace(json.dumps({}), '')


def flushdict(d : dict):
    """\
Flush the dictionary to the file holding credentials if dict has only allowed values.
else, ValueError

To be called after modifying the dictionary in memory.
"""
    if dict_has_only_allowed_values(d):
        with open(file=load._filepath, mode='w', encoding='utf-8', newline='') as fh:
            fh.write(json.dumps(d, indent=4))
    else:
        raise ValueError('dict has unallowed values')

def safe_edit(d : dict, key : str, value : Any):
    """\
If key is allowed, set the value in `d`. Else, raise ValueError.
"""
    if key in load.load_allowed(1):
        d[key]=value
    else:
        raise ValueError('`key` is a not-llowed value')
