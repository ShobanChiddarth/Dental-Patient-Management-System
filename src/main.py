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



online=True # variable to tell the program if internet connectivity is available/not available
# It is used in `randomstring` function

def multilineinput(
    margin = '| ',
    stream = sys.stdout,
    error = KeyboardInterrupt
    ):
    '''[Gist on multi line input in Python](https://gist.github.com/ShobanChiddarth/bf5002290c2116fe30350e37bebde5a0)'''
    string=str()
    try:
        while True:
            stream.write(margin)
            string=string+input()+'\n'
    except error:
        stream.write('\r')
        stream.write('\n')
        return string.strip()


def randomstring(length, nums=True, upper=True, lower=False) -> str:
            '''\
Return a random string'''
            choice_of_strings=deque()
            if nums:
                choice_of_strings.append(string.digits)
            if upper:
                choice_of_strings.append(string.ascii_uppercase)
            if lower:
                choice_of_strings.append(string.ascii_lowercase)
            return ''.join(random.choices(choice_of_strings, k=length)).strip()


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
        # proceedict and TrueFalseDict are just to turn user input into python boolean variables
        proceeddict={'y':True, 'n': False}
        TrueFalseDict={
            'y':True,
            'n':False,
            't':True,
            'f':False,
            '0':False,
            '1':True
        }
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

    def get_xpair():
        return '='.join(map(str.strip, input('> ').split('=')))
    
    def table_from_db(table:str, v='*', align='l'):
        '''Return the given table name as prettytable from database'''
        cursor=connection.cursor()
        cursor.execute(f'SELECT {v} FROM {table};')
        table = from_db_cursor(cursor)
        table.align=align
        return table
    
    def show_patients():
        '''Prints table `patients` in python output'''
        patients = table_from_db('patients')
        patients.align='l'
        print(patients)

    def add_patient():
        print('Adding new patient in table `patients` in database `SrisakthiPatients`')

        patientID=randomstring(7, online=online)
        patientcursor=connection.cursor()
        patientcursor.execute('SELECT patientID from patients;')
        iddata=patientcursor.fetchall()
        patientIDlist=[id for id in iddata]
        while patientID in patientIDlist:
            patientID=randomstring(7, online=online)

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

    def update_patient():
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
                    xpair=get_xpair()
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

    def show_appointments():
            cursor=connection.cursor()
            cursor.execute(f'''SELECT * FROM Appointments
ORDER BY date, time;''')
            appointments = from_db_cursor(cursor)
            appointments.align='l'
            print(appointments)

    def add_appointment(): # intended 2 tabs unnecasarily
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
            
            treatmentID=randomstring(8, online=online)

            cursor=connection.cursor()
            cursor.execute(f'''INSERT INTO Appointments (date, time, patientID, treatmentID)
VALUES ('{date}', '{time}', "{patientID}", "{treatmentID}");''')
            connection.commit()

            print('New appointment created')

    def update_appointment():
        print('You can update an appointment only if there is no `treatment` related to it')
        while True:
            try:
                treatmentID=input('''Enter treatmentID of appointment to update it:
(`show appointments` to show all appointments) > ''')
                if treatmentID=='show appointments':
                    show_appointments()
                    continue
                else:
                    try:
                        cursor=connection.cursor()
                        cursor.execute(f'SELECT * FROM treatments WHERE treatmentID=\"{treatmentID}\"')
                        data=cursor.fetchall()
                        if not data: # checks if treatmentID not in treatments
                            try:
                                cursor=connection.cursor()
                                print('''Enter value to be updated, detail.
For example
`date="2022-07-23"` (or) `time="14:30"`
Updatable values
- date
- time''')
                                xpair=get_xpair()
                                command=f'''UPDATE appointments
SET {xpair} WHERE treatmentID="{treatmentID}";'''
                                cursor.execute(command)
                                connection.commit()
                                print('Updated successfully')
                                show_appointments()
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

                        else:
                            print('Wrong treatmentID. Do it again.')
                    except KeyboardInterrupt:
                        break
                    except:
                        print('You made a mistake somewhere. Start from first')
                        continue
            except KeyboardInterrupt:
                break

    def show_treatments():
        treatments=table_from_db('treatments')
        print(treatments)

    def add_treatment():
        while True:
            print('Enter treatmentID below:')
            treatmentID=input('(also `show appointments` or `add appointment`) : ')

            if treatmentID=='show appointments':
                show_appointments()
                continue
            elif treatmentID=='add appointment':
                add_appointment()
            else:
                cursor=connection.cursor()
                cursor.execute(f"SELECT * FROM appointments WHERE treatmentID='{treatmentID}'")
                data=cursor.fetchall()
                if data:
                    print('Invalid treatmentID. Start from first.')
                else:

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

                    treatment=input('What treatment it is ? ')

                    print('''What is the status of the treatment?
Enter status below (ENTER for newline, CTRL+C on newline to stop)''')
                    status=multilineinput()
                        
                    while True:
                        fee=eval(input('Enter amount in rupees (without symbols) : '))
                        if not isinstance(fee, (int, float)):
                            print('Should be integer or decimal')
                            continue
                        break
                        
                    while True:
                        try:
                            paid=bool(TrueFalseDict[input('Is the payment complete [True/False] ?').strip().lower()[0]])
                            break
                        except KeyError as k:
                            print('You entered',k)
                            print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                            continue
                        
                    command=f'''INSERT INTO treatments (treatmentID, date, time, treatment, status, fee, paid)
VALUES ("{treatmentID}", "{date}", "{time}", "{treatment}", "{status}", {fee}, {paid})'''
                    cursor=connection.cursor()
                    cursor.execute(command)
                    connection.commit()
                    print('Added successfully')
                    show_treatments()

    def add_treatment_exact():
        while True:
            print('Enter treatmentID to add treatment in exact date, time of appointment')
            treatmentID=input('(or even `show appointments`) : ')
            if treatmentID=='show appointments':
                show_appointments()
                continue
            else:
                cursor=connection.cursor()
                cursor.execute(f'SELECT * FROM appointments WHERE treatmentID="{treatmentID}"')
                data=cursor.fetchall()
                if not data:
                    print('Wrong treatmentID. Appointment does not exist.')
                else:
                    cursor=connection.cursor()
                    cursor.execute(f'SELECT * FROM treatments WHERE treatmentID="{treatmentID}"')
                    data=cursor.fetchall()
                    if data:
                        print('Wrong treatmentID. Treatment exists.')
                        continue
                    else:
                        cursor=connection.cursor()
                        cursor.execute(f'SELECT date, time from appointments WHERE treatmentID="{treatmentID}"')
                        (date, time)=cursor.fetchall()[0]
                        date=date.strftime('%Y-%m-%d')
                        time=str(time)

                        treatment=input('What treatment it is ? ')

                        print('''What is the status of the treatment?
Enter status below (ENTER for newline, CTRL+C on newline to stop)''')
                        status=multilineinput()
                        
                        while True:
                            fee=eval(input('Enter amount in rupees (without symbols) : '))
                            if not isinstance(fee, (int, float)):
                                print('Should be integer or decimal')
                                continue
                            break
                        
                        while True:
                            try:
                                paid=bool(TrueFalseDict[input('Is the payment complete [True/False] ?').strip().lower()[0]])
                                break
                            except KeyError as k:
                                print('You entered',k)
                                print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                                continue
                        
                        command=f'''INSERT INTO treatments (treatmentID, date, time, treatment, status, fee, paid)
VALUES ("{treatmentID}", "{date}", "{time}", "{treatment}", "{status}", {fee}, {paid})'''
                        cursor=connection.cursor()
                        cursor.execute(command)
                        connection.commit()
                        print('Updated Successfully')


    def update_treatment():
        while True:
            print('Enter treatmentID below:')
            treatmentID=input('(even `show treatments`) >')
            if treatmentID=='show treatments':
                show_treatments()
                continue
            else:
                cursor=connection.cursor()
                cursor.execute(f'''SELECT * FROM treatments WHERE treatmentID="{treatmentID}"''')
                data=cursor.fetchall()
                if not data:
                    print('Wrong treatmentID. Enter again.')
                    continue
                else:
                    break

        print('''`update treatment` options
    0 : status
    1 : paid (if payment is over)

NOTE: You can\'t update anything else''')
        choice=int(input('Update what? '))
        if choice==0:
            print('''What is the new status of the treatment?
Enter status below (ENTER for newline, CTRL+C on newline to stop)''')
            status=multilineinput()
            command=f'''UPDATE treatments
SET status="{status}" WHERE treatmentID={treatmentID}"'''
            cursor=connection.cursor()
            cursor.execute(command)
            connection.commit()
            print('Updated successfully')
            show_treatments()

        elif choice==1:
            while True:
                try:
                    paid=bool(TrueFalseDict[input('Is the payment complete now [True/False] ?').strip().lower()[0]])
                    break
                except KeyError as k:
                    print('You entered',k)
                    print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                    continue
            
            command=f'''UPDATE treatments
SET paid={paid} WHERE treatmentID="{treatmentID}"'''
            cursor=connection.cursor()
            cursor.execute(command)
            connection.commit()
            print('Updated Successfully')
            show_treatments()

    def remove_appointment():

        print('You can remove an appointment only if it doesn\'t have a treatment associated with it')
        print('Enter treatmentID below : ')
        while True:
            treatmentID=input('(or even `show appointments`) : ')

            if treatmentID=='show appointments':
                show_appointments()
                continue
            else:
                cursor=connection.cursor()
                cursor.execute(f'SELECT * FROM appointments WHERE treatmentID="{treatmentID}";')
                data=cursor.fetchall()
                if not data:
                    print('Wrong treatmentID. It does not exist.')
                    continue
                else:
                    cursor=connection.cursor()
                    cursor.execute(f'SELECT * FROM treatments WHERE treatmentID="{treatmentID}"')
                    data=cursor.fetchall()
                    if data:
                        print('Wrong treatmentID. There is a treatment associated with it.')
                        continue
                    else:
                        cursor=connection.cursor()
                        cursor.execute(f'''DELETE FROM treatments
WHERE treatmentID="{treatmentID}"''')
                        print('Deleted successfully')
                        show_treatments()                        



    while True:
        command=input('Enter command> ')
        command=command.strip().lower()
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

        elif command in ('exit', 'quit'):
            break

        elif command=='enter-python-eval':
            while True:
                subcommand=input('enter-python-eval> ').strip().lower()
                try:
                    if subcommand in ('exit', 'quit'):
                        print('exited `enter-python-eval`')
                        break
                    else:
                        print(eval(subcommand))
                        continue
                except SyntaxError as s:
                    print('SyntaxError:',s, file=sys.stderr)
                    continue
                except:
                    print('ERROR', file=sys.stderr)
                    continue

        elif command=='enter-python-exec':
            while True:
                subcommand=input('enter-python-exec> ').strip().lower()
                try:
                    if subcommand in ('exit', 'quit'):
                        print('exited `enter-python-exec`')
                        break
                    else:
                        exec(subcommand)
                        continue
                except:
                    print('ERROR', file=sys.stderr)
                    continue

        elif command=='enter-sql-mode':
            while True:
                subcommand=input('enter-sql-mode> ').strip().lower()
                if command in ('exit', 'quit'):
                    break
                try:
                    cursor=connection.cursor()
                    cursor.execute(subcommand)
                    connection.commit()
                except:
                    print('ERROR', file=sys.stderr)
                else:
                    print('SUCCESS')
                finally:
                    continue

        elif command=='show patients':
            show_patients()
        
        elif command=='add patient':
            add_patient()
        
        elif command=='update patient':
            update_patient()

        elif command=='remove patient':
            print('You can\'t remove patients')

        elif command=='show appointments':
            show_appointments()
        
        elif command=='add appointment':
            add_appointment()

        elif command=='update appointment':
            update_appointment()

        elif command=='remove appointment':
            remove_appointment()

        elif command=='show treatments':
            show_treatments()
        
        elif command=='add treatment':
            add_treatment()

        elif command=='add treatment-exact':
            add_treatment_exact()

        elif command=='update treatment':
            update_treatment()

        elif command=='remove treatment':
            print('You can\'t remove treatments')

    print('logout')
    connection.close()
else:
    print('Connection to MySQL Database SriSakthiPatients FAILED')