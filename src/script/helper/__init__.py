"""\
Everything related to the `help` command of 'src/main.py'
"""
import os
import json
import pprint


def not_empty(line: str):
    """Tell if a given line (string) is empty (blank or whitespace) or not"""
    return not (line.isspace() or (not line))


def mapping_titles(line: str):
    """\
If a line is not a title (is not bolded(in markdown) from the begginning),
return the line as bulleted list."""
    if line.startswith('**') and (line.count('**') == 2):
        return line
    else:
        return '- '+line


global_flattened_list = []

def flatten_dict(d: dict,):
    """\
Recursively iterate over the given dictionary

And store it in a global list global_flattened_list as a list of tuples of key, value pairs"""
    for k, v in d.items():
        if isinstance(d, dict):
            if isinstance(v, str):
                global_flattened_list.append((k, v))
            elif isinstance(v, dict):
                flatten_dict(v)


def help_parse(command: str):
    """\
**Parse** the help command

Lstrip('help'), call the function `flattenDict` iterate over the global list `global_flattened_list`
(iterate with key,value pair strategy -> like how you would iterate on dict.items())
and by taking command as the key, return the corresponding value. If key does not exist,
return appropriate msg.
"""
    command = command.lstrip('help').strip()
    flatten_dict(_DATA)
    for key, value in global_flattened_list:
        if key == command:
            return value

    return "UNKNOWN COMMAND"


def process_help(help_command: str):
    """\
The actual function to be called to **procees** the help statement.

It does a lot of things."""

    with open(os.path.join(os.path.dirname(__file__), 'commands.json'), encoding='utf-8') as fh:
        global _DATA
        _DATA = json.loads(fh.read())

    help_command = help_command.strip().lower()

    if help_command == 'help':
        string = """\
DENTAL PATIENT MANAGEMENT SYSTEM DOCUMENTATION
==============================================

"""

        temp_s = pprint.pformat(_DATA, width=200, indent=4, compact=True)

        temp_s = temp_s.replace('{','\n').replace(':',' : ').replace('}','\n').replace(',','\n').replace("'", '')

        temp_s = '\n'.join(map(mapping_titles, filter(not_empty, (map(str.strip, temp_s.split('\n'))))))

        string += temp_s

        return string

    elif help_command.startswith('help'):
        return help_parse(help_command)
