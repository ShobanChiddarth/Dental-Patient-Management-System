from collections import deque
import random
import mysql.connector as connector
import prettytable
from prettytable import from_db_cursor
import sqlconfig
import requests
import sys
import json
import os
import string

def multilineinput(
    margin = '| ',
    stream = sys.stdout,
    error = KeyboardInterrupt
    ):
    '''[Gist on multi line input in Python](https://gist.github.com/ShobanChiddarth/bf5002290c2116fe30350e37bebde5a0)'''
    lines=str()
    try:
        while True:
            stream.write(margin)
            lines=lines+input()+'\n'
    except error:
        stream.write('\r')
        stream.write('\n')
        return lines


filepath=os.path.join(os.path.dirname(__file__), 'sqlcredentials_sample.json')

print('''\
SRI SAKTHI DENTAL CLINIC
DENTAL PATIENT MANAGEMENT SYSTEM
''')
print('''Using current sql connection configuration
''', sqlconfig.load.load_data(0), sep='')

print('''Please look at this dictionary to get an idea about sql connection config dict.
Your dictionary must look somewhat like this.''')
with open(file=filepath, mode='rt', encoding='utf-8', newline='') as fh:
    print(fh.read())

print('But it looks like')
with open(file=sqlconfig.load._filepath, mode='rt', encoding='utf-8', newline='') as fh:
    print(fh.read())

while True:
    try:
        proceeddict={'y':True, 'n': False}
        proceed=proceeddict[input('Do you wish to proceed with the following (please make changes according to your need) [Y/n]?')[0].lower()]
        break
    except KeyError:
        print('Invalid input')
        continue

while not proceed:
    item=input('Enter item to edit: ')
    value=eval(input('Enter updated value: '))
    sqlconfig.manage.edit_credentials(item, value)
    print('Dictionary now is')
    print(sqlconfig.load.load_data(0))
    proceed=proceeddict[input('Are you satisfied [Y/n]?')[0].lower()]
 
try:
    connection=connector.connect(**sqlconfig.load.load_data(1))
except connector.errors.DatabaseError as connectionerror:
    print(connectionerror)
    exit()




if connection.is_connected():
    print('Connected to MySQL Database SriSakthiPatients')
    print('''\
Welcome admin
Type `help` for help
''')

    def randomstring(chars, online=True, nums=True, upper=True, lower=False) -> str:
        '''\
Random String Generator

Function to use the form at https://www.random.org/strings/
(modified as per the requirements of the program)

RANDOM.ORG Documentation
------------------------
This form allows you to generate random text strings. 
The randomness comes from atmospheric noise, which for 
many purposes is better than the pseudo-random number 
algorithms typically used in computer programs.

PARAMETERS
----------
chars : length of the string
nums : Numeric digits (0-9)
upper : Uppercase letters (A-Z)
lower : Lowercase letters (a-z)

OUTPUT
------
Return a random string'''
        if online:
            tempdict={
                True:'on',
                False:'off'
            }
            nums=tempdict[nums]
            upper=tempdict[upper]
            lower=tempdict[lower]
            r=requests.get(f'https://www.random.org/strings/?num=1&len={chars}&digits={nums}&upperalpha={upper}&loweralpha={lower}&unique=on&format=plain&rnd=new')
            return r.content.decode('utf-8')
        else:
            choice_of_strings=deque()
            if nums:
                choice_of_strings.append(string.digits)
            if upper:
                choice_of_strings.append(string.ascii_uppercase)
            if lower:
                choice_of_strings.append(string.ascii_lowercase)
            return ''.join(random.choices(choice_of_strings, k=chars))
    
    def table_from_db(table:str, v='*', align='l'):
        '''Return the given table name as prettytable from database'''
        cursor=connection.cursor()
        cursor.execute(f'SELECT {v} FROM {table};')
        table = from_db_cursor(cursor)
        table.align=align
        return table
    
    def show_patients():
        patients = table_from_db('patients')
        patients.align='l'
        print(patients)

    def add_patient():
        print('Adding new patient in table `patients` in database `SrisakthiPatients`')

        patientID=randomstring(7)
        patientcursor=connection.cursor()
        patientcursor.execute('SELECT patientID from patients;')
        iddata=patientcursor.fetchall()
        patientIDlist=[id for id in iddata]
        while patientID in patientIDlist:
            patientID=randomstring(7)

        del patientcursor, iddata, patientIDlist

        name=input('Enter patient name: ')

        print('''Date Of Birth Format: YYYY-MM-DD
Example: 1999-03-12''')
        dob=input('Enter dob: ')
        while not (dob[0:4].isdigit() and 
                            dob[4]=='-' and 
                            dob[5:7].isdigit() and 
                            dob[7]=='-' and
                            dob[8:10].isdigit()
                            and len(dob)==10 ):
                print('Invalid DOB')
                dob=input('Re-enter DOB: ')

        phone=input('Enter phone number with country code: ')

        while True:
            gender=input('Enter gender (M/F) : ')
            if gender in ('M', "F"):
                break
            else:
                print('Invalid gender')
                print('Re-enter gender')

        print('Enter address:')
        address=multilineinput()

        cursor=connection.cursor()
        cursor.execute(f'''INSERT INTO patients (patientID, name, dob, gender, phone, address)
VALUES ("{patientID}", "{name}", '{dob}', "{gender}", "{phone}", "{address}");''')
        connection.commit()

        print('New patient created')

    def show_appointments():
            cursor=connection.cursor()
            cursor.execute(f'''SELECT * FROM Appointments
ORDER BY date, time;''')
            appointments = from_db_cursor(cursor)
            appointments.align='l'
            print(appointments)



    while True:
        command=input('Enter command> ')
        command=command.strip()
        if command.lower().startswith('help'):
            if command=='help':
                
                with open(os.path.join(os.path.dirname(__file__),'help.md'),
                            mode='rt', 
                            encoding='utf-8',
                            newline='\r\n') as helpfile:
                    print(helpfile.read())
            else:
                command=command.split()
                del command[0]

                helpdict={
                    'help':'show help message',
                    'exit':'exit the script',
                    'quit':'alias of exit',
                    'show':{
                        'patients':'print the table `patients` in database `SrisakthiPatients`',
                        'appointments':'print the table `Appointments` in database `SrisakthiPatients`',
                        'treatments':'print the table `treatments` in database `SrisakthiPatients`',
                    },
                    'add':{
                        'patient':'''\
create a new patient
in database `SrisakthiPatients`, table `patients`''',
                        'appointment':'add a new appointment in table `Appointments` in database `',
                        'treatment':'''\
add new treatment in table `treatments` in database `SrisakthiPatients`
You must provide `treatmentID`''',
                        'treatment-exact':'''\
add new treatment in table `treatments` in database `SrisakthiPatients`
with the exact date and time in table `Appointments`
You must provide `treatmentID`'''
                    },
                    'update':{
                        'patient':'''\
update a patient in table `patients` in database `SrisakthiPatients`
You must provide `patientID`''',
                        'appointment':'''\
update an existing appointment in table `Appointments` in database `SrisakthiPatients`
You must provide `treatmentID`''',
                        'treatment':'''\
update treatment in in table `treatments` in database `SrisakthiPatients`
You must provide `treatmentID`'''
                    },
                    'remove':{
                        'patient':'You can\'t delete patients',
                        'appointment':'''\
remove an appointment in table `Appointments` in database `SrisakthiPatients`
You must provide `treatmentID`
NOTE: You can remove appointments only if the treatment didn\'t take place''',
                        'treatment':'You can\'t remove treatments'
                        }
                    }

                
                def helpparse(words, searchdict):
                    try:
                        if isinstance(words, list):

                            if isinstance(searchdict[words[0]], str):
                                return searchdict[words[0]]
                            elif isinstance(searchdict[words[0]], dict):
                                searchdict=searchdict[words[0]]
                                del words[0]
                                return helpparse(words, searchdict)
                    except KeyError as k:
                        return str(k)+'\n'+'Invalid Input'
                    except IndexError as I:
                        return 'Invalid Input'

                
                print(helpparse(command, helpdict))
        elif command.lower() in ('exit', 'quit'):
            break

        elif command=='show patients':
            show_patients()
        
        elif command=='add patient':
            add_patient()
        
        elif command=='update patient':
            while True:
                try:
                    patientID=input('Enter patientID to update (or show patients): ')
                    if patientID=='show patients':
                        show_patients()
                        continue
                    else:
                        print('''Enter value to be updated, detail.
For example
`name="Steven"`

Updatable values
- name
- dob
- gender
- phone
- address''')
                        xpair='='.join(map(str.strip, input('> ').split('=')))
                        cursor=connection.cursor()
                        command=f'''UPDATE patients
SET {xpair} WHERE patientID="{patientID}";'''
                        cursor.execute(command)
                        connection.commit()
                        print('Updated successfully')
                        show_patients()
                        while True:
                            try:
                                proceed=proceeddict[input('Are you satisfied [Y/n] ?')[0].lower()]
                                break
                            except KeyError:
                                print('Invalid Input')
                                continue
                        if proceed:
                            break
                        else:
                            continue
                except KeyboardInterrupt:
                    break
                except:
                    print('You made a mistake somewhere. Start from first')
                    continue


        elif command=='remove patient':
            print('You can\'t remove patients')

        elif command=='show appointments':
            show_appointments()
        
        elif command=='add appointment':
            print('''Date format: YYYY-MM-DD
Example: 1999-03-12''')
            date=input('Enter date: ')
            while not (date[0:4].isdigit() and 
                        date[4]=='-' and 
                        date[5:7].isdigit() and 
                        date[7]=='-' and
                        date[8:10].isdigit()
                        and len(date)==10 ):
                    print('Invalid Date')
                    date=input('Re-enter Date: ')
            
            print('''Time format: HH:MM (24 hr format)
Example: 13:50''')
            time=input('Enter time: ')
            while not (time[0:2].isdigit() and
                        time[2]==':' and
                        time[3:5] and
                        len(time)==5):
                        print('Invalid Time')
                        time=input('Re-enter time: ')
            while True:
                print('''TIP: Enter `show patients` to show all patients
   Enter `add patient` to add a patient''')
                patientID=input('Enter patientID: ').strip()
                if patientID.strip()=='show patients':
                    show_patients()
                elif patientID.strip()=='add patient':
                    add_patient()
                else:
                    break
            
            treatmentID=randomstring(8)

            cursor=connection.cursor()
            cursor.execute(f'''INSERT INTO Appointments (date, time, patientID, treatmentID)
VALUES ('{date}', '{time}', "{patientID}", "{treatmentID}");''')
            connection.commit()

            print('New appointment created')

        elif command=='show treatments':
            treatments=table_from_db('treatments')
            print(treatments)

    print('Exited')
    connection.close()
else:
    print('Connection to MySQL Database SriSakthiPatients FAILED')