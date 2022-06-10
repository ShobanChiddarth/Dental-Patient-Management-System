import os
import sys

import subprocess
import pprint
import json
from typing import Any
from pwinput import pwinput
from pymsgbox import password as msgbox_password

os.chdir(os.path.dirname(__file__))

if not os.path.exists(os.path.join(os.path.dirname(__file__), '.cache')):
    os.mkdir(os.path.join(os.path.dirname(__file__), '.cache'))



print('''\
DENTAL PATIENT MANAGEMENT SYSTEM
Sri Sakthi Dental Clinic

your connection configuration should something look like''')

with open(os.path.join(os.path.dirname(__file__), "sqlcredentials_sample.json")) as _credentialsFile:
    pprint.pprint(json.loads(_credentialsFile.read()), sort_dicts=False, indent=4)

print('But it looks like')

config = {
    "program_name" : "dpms",
    "program_file" : os.path.join(os.path.dirname(__file__), "dpms.bat")
}

subprocess.Popen(f'{config["program_name"]} read-config --jsonoutput',
                text=True, encoding='utf-8', shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                # stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)



def mapTrueFalse(value : Any) -> bool:

    if isinstance(value, str):
        value=value.strip().lower()

    trueFalseDict = {
    "true" : True,
    "t"    : True,
    1      : True,
    "1"    : True,
    "on"   : True,
    "y"    : True,
    "yes"  : True,

    "false": False,
    "f"    : False,
    0      : False,
    "0"    : False,
    "off"  : False,
    "n"    : False,
    "no"   : False
    }

    if value in trueFalseDict:
        return trueFalseDict[value]
    else:
        raise ValueError('Unable to convert this value to True or False')



def configSQLConnection():
    while True:
        try:
            choice=mapTrueFalse(input("Do you want to change it? "))
            break
        except ValueError as v:
            print(v)
            continue

    while choice:
        while True:
            try:
                modifyOrDelete=mapTrueFalse(input("""\
Do you want to update a value or delete it
(True = Modify, False = Delete) ? """))
                break
            except ValueError as v:
                print(v)
        
        if modifyOrDelete: # if update
            while True:
                key = input('Enter the key you want to modify (add/update): ')
                allowedValues=json.loads(subprocess.run(f'{config["program_name"]} load-allowed --jsonoutput',
                                    text=True, encoding='utf-8', capture_output=True, shell=True).stdout)
                if key in allowedValues:
                    break
                else:
                    print('Your key is a not allowed value. Re-enter it.')
                    continue

            while True:
                try:
                    value = eval(input('Enter the value of the key (will be `eval`uated by Python): '))
                    break
                except:
                    print('Improper value')
            
            while True:
                try:
                    prog_eval=mapTrueFalse(input("""\
By default, the program accepts any type of arguments as strings
and store them in the connection dictionary as strings.
Do you wan't your value to also be evaluated? """))
                    break
                except ValueError as v:
                    print(v)

            run_command=f'{config["program_file"]} config --key "{key}" --value "{value}"'

            if prog_eval:
                run_command+=' --evaluate'

            subprocess.run(run_command,
                            text=True, encoding='utf-8', shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                            # stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
            print('Successfully updated')

        else: # if delete
            while True:
                key=input("Enter the key you wan't to delete: ")
                connectionDict=json.loads(subprocess.run(f'{config["program_name"]} read-config --jsonoutput',
                                    text=True, encoding='utf-8', shell=True, capture_output=True))
                if key in connectionDict:
                    subprocess.run(f'{config["program_name"]} del-config --key "{key}"',
                                    text=True, encoding='utf-8', shell=True)
                    print('Deleted successfully')
                    break
                else:
                    while True:
                        ifForget=input('''\
The key you are trying to delete does not exist.
Enter a valid key or forget the operation
(type "forget" to forget, "continue" to re-enter another key: ''')
                        if ifForget in ('forget', 'continue'):
                            break
                        else:
                            print('Invalid Input')
                            continue
                    if ifForget=='forget':
                        break
                    elif ifForget=='continue':
                        continue

        while True:
            try:
                choice=mapTrueFalse(input('Do you still want to edit it? '))
                break
            except ValueError as v:
                print(v)
        
        if not choice:
            break
        else:
            continue

configSQLConnection()

if 'idlelib.run' in sys.modules:
    password=msgbox_password(text='Enter MYSQL Password', title='Dental Patient Management System', mask='•')
else:
    password=pwinput(prompt='''\
(will be used for MYSQL related commands)
Enter MYSQL Password: ''', mask='•')


while True:
    command=input('dpms> ').strip()

    if command in ('exit', 'quit'):
        print('logout')
        break

    command=config['program_name']+' '+command+' '

    if command.split()[0] not in ("load-allowed", "read-config", "config", "del-config"):
        command+=f'-p "{password}"'

    p1=subprocess.run(command.split(), text=True, encoding='utf-8', shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                        # stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    



