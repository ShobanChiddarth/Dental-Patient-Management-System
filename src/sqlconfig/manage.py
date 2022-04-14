import json
from .load import _filepath, current_sqlcredentials

def fileisemtpy():
    return not not current_sqlcredentials

def flushdict():
    global current_sqlcredentials
    with open(file=_filepath, mode='w', encoding='utf-8', newline='') as fh:
        fh.write(json.dumps(current_sqlcredentials, indent=4))



def edit_credentials(item:str, edited):
    global current_sqlcredentials
    current_sqlcredentials[item] = edited
    flushdict()