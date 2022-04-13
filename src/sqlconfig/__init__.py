from . import load
import os

_directory=os.path.dirname(__file__)
_filepath=os.path.join(_directory, 'sqlcredentials.json')

if not os.path.exists(_filepath):
    with open(_filepath, mode='at', encoding='utf-8', newline='') as _credentialsfile:
        pass