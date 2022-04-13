import json
from . import _filepath
from load import sqlcredentialsdict

def fileisemtpy():
    return not not sqlcredentialsdict

def flushdict():
    global sqlcredentialsdict
    with open(file=_filepath, mode='w', encoding='utf-8', newline='') as fh:
        fh.write(json.dumps(sqlcredentialsdict, indent=4))



def edit_credentials(item:str, edited):
    '''\
'''
    global sqlcredentialsdict
    sqlcredentialsdict[item] = edited
    flushdict()