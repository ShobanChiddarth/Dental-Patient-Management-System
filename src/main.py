import mysql.connector as connector
import prettytable
from prettytable import from_db_cursor
import json
import requests
import sys

print('''\
SRI SAKTHI DENTAL CLINIC
DENTAL PATIENT MANAGEMENT SYSTEM
''')
try:
    connection=connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='1234',
        database='SrisakthiPatients',
        buffered=True
    )
except connector.errors.DatabaseError as connectionerror:
    print(connectionerror)




if connection.is_connected():
    print('Connected to MySQL Database SriSakthiPatients')
    print('''\
Welcome admin
Tyoe `help` for help
''')

    def randomstring(chars, nums='on', upper='on', lower='off') -> str:
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

        r=requests.get(f'https://www.random.org/strings/?num=1&len={chars}&digits={nums}&upperalpha={upper}&loweralpha={lower}&unique=on&format=plain&rnd=new')
        return r.content.decode('utf-8')
    
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
        address=multi_line_input()

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

    def multi_line_input(
    margin='| ',
    end='\n',
    error=KeyboardInterrupt
):
        line=input(margin)
        while True:
            try:
                line=line+end+input(margin)
            except error as e:
                sys.stdout.write('\r\n')
                return line

    while True:
        command=input('Enter command> ')
        command=command.strip()
        if command.lower().startswith('help'):
            if command=='help':
                
                with open('help.md','rt', encoding='utf-8', newline='\r\n') as helpfile:
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

            """elif command=='update patient': #-\t-\t
            print('''Enter patientID to update''')
            while True:
                    try:
                        patientID=input('patientID>')
                        cursor=connection.cursor()
                        cursor.execute(f'''select * from patients
WHERE patientid='{patientID}';''')
                        table = from_db_cursor(cursor)
                        print(table)
                        choice=input('Is the the patient you wan\'t to update (Y/N)? ')
                        if choice.lower()=='y':
                            break
                    except:
                        print('Invalid patientID')
            print('''PRO TIP
Just copy and paste the old details if you need to leave it unchanged''')
            name=input('new name of patient: ')
            dob=input('new Enter dob: ')
            while not (dob[0:4].isdigit() and 
                        dob[4]=='-' and 
                        dob[5:7].isdigit() and 
                        dob[7]=='-' and
                        dob[8:10].isdigit()
                        and len(dob)==10 ):
                    print('Invalid DOB')
                    dob=input('Re-enter DOB: ')
            while True:
                gender=input('Enter gender (M/F) : ')
                if gender in ('M', "F"):
                    break
                else:
                    print('Invalid gender')
                    print('Re-enter gender')
            phone=input('Enter new phone number with country code: ')
            print('''Please enter line by line
Enter new address:''')
            address=multi_line_input()

            cursor=connection.cursor()
            cursor.execute(f'''UPDATE patients
SET name="{name}", dob='{dob}', gender="{gender}", phone="{phone}", address="{address}"
WHERE patientID="{patientID}";''')
            connection.commit()
            print('Updated')"""

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

            """elif command=='update appointment':
            print('You can update an appointment only if the treatment didn\'t take place')
            while True:
                    # if input treatmentID exists in `treatments`
                    print('''TIP: Enter 'show appointments' to see all appointments''')
                    treatmentID=input('Enter treatmentID: ')
                    if treatmentID=='show appointments':
                        show_appointments()
                    else:
                        data=connection.cursor().execute(f'''SELECT treatmentID from Appointments
WHERE treatmentID="{treatmentID}";''')
                        if data:
                            print('Invalid treatmentID')
                        else:
                            break
                            

            date=input('Enter new date: ')
            while not (date[0:4].isdigit() and 
                        date[4]=='-' and 
                        date[5:7].isdigit() and 
                        date[7]=='-' and
                        date[8:10].isdigit()
                        and len(date)==10 ):
                    print('Invalid Date')
                    date=input('Re-enter new Date: ')


            time=input('Enter new time: ')
            while not (time[0:2].isdigit() and
                        time[2]==':' and
                        time[3:5] and
                        len(time)==5):
                        print('Invalid Time')
                        time=input('Re-enter new time: ')
            
            cursor=connection.cursor(buffered=True)
            cursor.execute(f'''UPDATE Appointments
SET date='{date}', time=\'{time}\'
WHERE treatmentID="{treatmentID}"''')
            print('Updated appointment')
            show_appointments()"""

        elif command=='show treatments':
            treatments=table_from_db('treatments')
            print(treatments)

    print('Exited')
    connection.close()
else:
    print('Connection to MySQL Database SriSakthiPatients FAILED')