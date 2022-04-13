from . import _filepath
import json

with open(_filepath, mode='rt', encoding='utf-8', newline='') as fh:
    _data= fh.read()
    sqlcredentialsdict = json.loads(_data)