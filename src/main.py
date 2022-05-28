from collections import deque
import json
import pprint
import random
import mysql.connector as connector
from prettytable import from_db_cursor
import helper
import sqlconfig
import sys
import os
import string
from pyautogui import password
from pwinput import pwinput




def multilineinput(
    margin = '| ',
    stream = sys.stdout,
    error = KeyboardInterrupt
    ):
    '''[Gist on multi line input in Python](https://gist.github.com/ShobanChiddarth/bf5002290c2116fe30350e37bebde5a0)'''
    s=str()
    try:
        while True:
            stream.write(margin)
            s=s+input()+'\n'
    except error:
        stream.write('\r')
        stream.write('\n')
        return s.strip()


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

current_sql_configuration = sqlconfig.load.load_data(1)

print('Using current sql connection configuration',
    pprint.pformat(current_sql_configuration, indent=4), sep='\n')

print('''Please look at this dictionary to get an idea about sql connection config dict.
Your dictionary must look somewhat like this.''')
with open(file=filepath, mode='rt', encoding='utf-8', newline='') as fh:
    pprint.pprint(json.loads(fh.read()))

print('But it looks like', pprint.pformat(current_sql_configuration, indent=4), sep='\n')

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
        # not using the variable `current_sql_configuration`
        # just in case if there is some error when flushing the dict, it would be detected
        proceed=proceeddict[input('Are you satisfied [Y/n]?')[0].lower()]
 
    else:
        print('Your `item` is not allowed. ')
        continue

# begin password getting process
if ('idlelib.run' in sys.modules):
    password=password(text='Enter MYSQL Password', title='Dental Patient Management System', mask='•')
else:
    password=pwinput(prompt='Enter MYSQL Password: ', mask='•')

current_sql_configuration['password']=password
try:
    connection=connector.connect(**current_sql_configuration)
except connector.errors.DatabaseError as connectionerror:
    print(connectionerror)
    sys.exit()






if connection.is_connected():
    print('Connected to MySQL Database SriSakthiPatients')
    print('''\
Welcome admin
Type `help` for help
''')

    def get_xpair():
        """\
Remove the whitespaces before, between, and after """
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
        '''\
Gets user input and adds a new patient in the table `patients`'''
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

    def update_patient():
        '''\
Gets user input and updates a patient in table `patients`'''
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
            '''\
Shows all the appointments in `appointments` table'''
            appointments=table_from_db('appointments')
            print(appointments)

    def add_appointment(): # intended 2 tabs unnecasarily
            '''\
Gets user input and adds an appointment in the table `appointments`'''
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

    def update_appointment():
        '''\
Gets user input and updates an appointment in the table `appointments`'''
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
        '''\
Shows all records in table `treatments`'''
        treatments=table_from_db('treatments')
        print(treatments)

    def add_treatment():
        '''\
Gets user input and adds a treatment to table `treatments`'''
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
        '''\
Gets user input but date and time are of the exact time as per table `appointments`
and inserts into table `treatments`'''
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
        '''\
Gets user input and updates a record in table `treatments`'''
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
        '''\
Gets user input and removed a record in table `appointments` if it is not linked to
a record in the table `treatments`'''

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

        if command.startswith('help'):
            print(helper.process(command))

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
