"""\
This submodule is to be used to **edit** the data (configuration credentials)
"""
import json
import load

def fileisemtpy():
    """Tell if `sqlcredentails` is empty or not"""
    return not not current_sqlcredentials

def flushdict():
    """\
Flush the dictionary to the file holding credentials

To be called after modifying the dictionary in memory"""
    global current_sqlcredentials
    with open(file=_filepath, mode='w', encoding='utf-8', newline='') as fh:
        fh.write(json.dumps(current_sqlcredentials, indent=4))


