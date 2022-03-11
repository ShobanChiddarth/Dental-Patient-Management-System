import mysql.connector as connector
import prettytable
from prettytable import from_db_cursor

print('''\
SRI SAKTHI DENTAL CLINIC
DENTAL PATIENT MANAGEMENT SYSTEM
''')

connection=connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='1234',
    database='SrisakthiPatients'
)
if connection.is_connected():
    print('Connected to MySQL Database SriSakthiPatients')
    print('''\
Welcome admin
Tyoe `help` for help
''')
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

        elif command.strip()=='show patients':
            cursor=connection.cursor()
            cursor.execute('SELECT * FROM patients;')
            mytable = from_db_cursor(cursor)
            mytable.align='l'
            print(mytable)
    
    print('Exited')
    input()
    connection.close()
else:
    print('Connection to MySQL Database SriSakthiPatients FAILED')


