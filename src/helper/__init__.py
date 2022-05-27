"""\
Everything related to the `help` command of 'src/main.py'
"""
import os
import json
import pprint
import pandas as pd


def notempty(line:str):
    return not (line.isspace() or (not line))             

def mappingTitles(line:str):
            if line.startswith('**') and (line.count('**')==2):
                return line
            else:
                return '- '+line

def homogeneous_type(seq):
    """https://stackoverflow.com/questions/13252333/check-if-all-elements-of-a-list-are-of-the-same-type"""
    iseq = iter(seq)
    first_type = type(next(iseq))
    if all( (type(x) is first_type) for x in iseq ):
        return first_type
    else:
        return False

global_flattened_list=[]
def flattenDict(d : dict,):
    """Recursively iterate over the given dictionary

And store it in a dictionary `flattenedDict`, later look for the key in it and return the value"""
    for k,v in d.items():
        if isinstance(d, dict):
            if isinstance(v, str):
                global_flattened_list.append((k,v))
            elif isinstance(v, dict):
                flattenDict(v)

            

def helpParse(command : str, searchdict : dict):
    # try:
        command=command.lstrip('help').strip()
        flattenDict(_data)
        for key, value in global_flattened_list:
            if key==command:
                return value
            

        # return global_flattened_list[command]
        
    # except KeyError as k:
    #     return str(k)+' '+'does not exist'

def processHelp(helpCommand : str):

    with open(os.path.join(os.path.dirname(__file__), 'commands.json')) as fh:
        global _data
        _data=json.loads(fh.read())

    helpCommand=helpCommand.strip().lower()

    if helpCommand=='help':
        string="""\
DENTAL PATIENT MANAGEMENT SYSTEM DOCUMENTATION
==============================================

"""

        tempS=pprint.pformat(_data, width=200, indent=4, compact=True, sort_dicts=False, underscore_numbers=False)

        tempS=tempS.replace('{','\n').replace(':',' : ').replace('}','\n').replace(',','\n').replace("'", '')

        tempS='\n'.join(map(mappingTitles, filter(notempty, (map(str.strip, tempS.split('\n'))))))

        string+=tempS

        return string
    
    elif helpCommand.startswith('help'):
        return helpParse(helpCommand, _data)

                    





