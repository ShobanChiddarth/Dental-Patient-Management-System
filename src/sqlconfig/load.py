"""\
This submodule is to be used to **read** the data (coniguration credentials)
"""
import os
import json

_directory=os.path.dirname(__file__)
_filepath=os.path.join(_directory, 'sqlcredentials.json')

if not os.path.exists(_filepath):
    # creating an empty file
    with open(_filepath, mode='at', encoding='utf-8', newline='') as _credentialsfile:
        pass

def load_data(n: 0 | 1 = 1):
    """\
Return the content in the file `sqlcredentials.json` as text if n == 0.
Return the content in the file `sqlcredentials.json` as a dictionary if n==1.
Else, raise ValueError
"""
    with open(_filepath, mode='rt', encoding='utf-8', newline='') as fh:
        _data= fh.read()
        sqlcredentialsdict = json.loads(_data)
        if n == 0:
            return _data
        elif n == 1:
            return sqlcredentialsdict
        else:
            raise ValueError('n must be 0 or 1')
