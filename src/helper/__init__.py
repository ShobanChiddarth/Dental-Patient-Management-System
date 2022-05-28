"""\
Everything related to the `help` command of 'src/main.py'
"""
import os
import json
import pprint


def notempty(line:str):
    """Tell if a given line (string) is empty (blank or whitespace) or not"""
    return not (line.isspace() or (not line))             

def mappingTitles(line:str):
    """\
If a line is not a title (is not bolded(in markdown) from the begginning), return the line as bulleted list."""
    if line.startswith('**') and (line.count('**')==2):
        return line
    else:
        return '- '+line



global_flattened_list=[]
def flattenDict(d : dict,):
    """\
Recursively iterate over the given dictionary

And store it in a global list global_flattened_list as a list of tuples of key, value pairs"""
    for k,v in d.items():
        if isinstance(d, dict):
            if isinstance(v, str):
                global_flattened_list.append((k,v))
            elif isinstance(v, dict):
                flattenDict(v)

            

def helpParse(command : str):
    """\
**Parse** the help command

Lstrip('help'), call the function `flattenDict`, iterate over the global list `global_flattened_list`
(iterate with key,value pair strategy -> like how you would iterate on dict.items())
and by taking command as the key, return the corresponding value. If key does not exist, return appropriate msg.
"""
    command=command.lstrip('help').strip()
    flattenDict(_data)
    for key, value in global_flattened_list:
        if key==command:
            return value
    else:
            return "UNKNOWN COMMAND"

def processHelp(helpCommand : str):
    """\
The actual function to be called to **procees** the help statement.

It does a lot of things."""

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
        return helpParse(helpCommand)
