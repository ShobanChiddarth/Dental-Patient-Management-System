
import json
import os
import pprint
import sys

import pandas as pd

import sqlconfig

def mapTrueFalse(s : str) -> bool:
    """Converts the string given to boolean value"""
    TrueFalseDict={
            'y':True,
            'n':False,
            't':True,
            'f':False,
            '0':False,
            '1':True,
            'yes':True,
            'no':False,
            'true':True,
            'false':False,
        }
    if s.lower().strip() in TrueFalseDict:
        return TrueFalseDict[s.lower().strip()]
    else:
        raise ValueError('This string cannot be converted to True or False')

if __name__ != "__main__":
    sys.exit()



print("""\
This program is to edit the connection configuration stored in the file
`sqlcredentials.json` (inside sqlconfig module).
""")


current_sql_configuration = sqlconfig.load.load_data(1)
filepath=os.path.join(os.path.dirname(__file__), 'sqlcredentials_sample.json')

print('''Please look at this dictionary to get an idea about sql connection config dict.
Your dictionary must look somewhat like this.''')

with open(file=filepath, mode='rt', encoding='utf-8', newline='') as fh:
    pprint.pprint(json.loads(fh.read()))

print()
print('But it looks like this', pprint.pformat(current_sql_configuration, indent=4), sep='\n')

while True:
    try:
        proceed=input('''\
Do you wish to use the following configuration?
(please make changes according to your need) [Y/n]: ''')
        proceed=mapTrueFalse(proceed)
        break
    except ValueError:
        print('Invalid input')
        continue

while not proceed:
    print('Do you want to update/add or delete?')
    print(pd.Series(['update/add', 'delete']).to_string())
    while True:
        _edit_choice=input('Enter your choice: ')
        try:
            _edit_choice=int(_edit_choice)
            break
        except ValueError as VE:
            print('Invalid Input.', VE)
            continue

    if _edit_choice==0:
        print('''\
Enter the item you wish to update/add
You have to add only items that are allowed.
Type `allowed` to get a list of all allowed items''')
        allowed = sqlconfig.load.load_allowed(1)
        item=input(': ').strip()
        if item=='allowed':
            pprint.pprint(allowed, indent=4)
            continue
        elif item in allowed:
            value=eval(input("Enter updated value (will be evaluated by python's `eval` function): "))

            sqlconfig.manage.safe_edit(current_sql_configuration, item, value)
            sqlconfig.manage.flushdict(current_sql_configuration)

            print('Dictionary now is')
            pprint.pprint(sqlconfig.load.load_data(1), indent=4)

        else:
            print('Your `item` is not allowed. ')
            continue

    elif _edit_choice==1:
        del_key=input('Enter the key to be deleted: ')
        if del_key in current_sql_configuration:
            del current_sql_configuration[del_key]
            sqlconfig.manage.flushdict(current_sql_configuration)
            print('Deleted')
        else:
            print('Key does not exist')

    else:
        print('Invalid Input')

    print()
    print('Do you wish to save the following configuration?')
    pprint.pprint(current_sql_configuration, indent=4)
    proceed=input('Yes/No: ')

    while True:
        try:
            proceed=mapTrueFalse(proceed)
            break
        except ValueError as VE:
            print('Invalid Input')
            continue


print()
print("Exiting program with configuration as")
pprint.pprint(current_sql_configuration)
