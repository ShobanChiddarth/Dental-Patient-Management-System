"""\
This submodule is to be used to **read** the data (coniguration credentials)
"""
import os
import json

_directory = os.path.dirname(__file__)
_filepath = os.path.join(_directory, 'sqlcredentials.json')
_allowed_filepath = os.path.join(_directory, 'allowed_args.json')

if not os.path.exists(_filepath):
    # creating an empty file
    # and dumping an empty dictionary (else, json would raise error when reading from '')
    with open(_filepath, mode='at', encoding='utf-8', newline='') as _credentialsfile:
        _credentialsfile.write(json.dumps({}))


def load_data(n: 0 | 1 = 1):
    """\
Return the content in the file `sqlcredentials.json` as text if n == 0.
Return the content in the file `sqlcredentials.json` as a dictionary if n == 1.
Else, raise ValueError.
"""
    with open(_filepath, mode='rt', encoding='utf-8', newline='') as fh:
        _data = fh.read()
        sqlcredentialsdict = json.loads(_data)
        if n == 0:
            return _data
        elif n == 1:
            return sqlcredentialsdict
        else:
            raise ValueError('n must be 0 or 1')


def load_allowed(n: 0 | 1 = 1):
    """\
Return the content in the file `allowed_args.json` as text if n == 0.
Return the content in the file `allowed_args.json` as list if n == 1.
Else, raise ValueError.
"""
    with open(_allowed_filepath, mode='rt', encoding='utf-8') as fh:
        _data = fh.read()
        allowed_args_list = json.loads(_data)
    if n == 0:
        return _data
    elif n == 1:
        return allowed_args_list
    else:
        raise ValueError('n must be 0 or 1')
