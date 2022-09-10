import sys
import os
import string

from collections import deque
import json
import pprint
import random
import tkinter as tk
from typing import Any
from mysql import connector
from prettytable import PrettyTable, from_db_cursor
from pymsgbox import password
from pwinput import pwinput
import pandas as pd

import helper
import sqlconfig


class MutableStringContainer():
    """Just a mutable container of an immutable type str. The data is in `self.data`."""
    def __init__(self, data:str='') -> None:
        self.data=data

    def __str__(self) -> str:
        return str(self.data)



def multilineinput(input_text='Enter your input'):
    '''Get and return a multi line input (GUI)'''
    string=MutableStringContainer()

    window=tk.Tk()
    window.title('Dental Patient Management System')
    window.geometry('600x230')

    title=tk.Label(window, text=input_text)
    title.pack(side=tk.TOP)

    yscrollbar=tk.Scrollbar(window, orient='vertical')
    yscrollbar.pack(side=tk.RIGHT, fill='y')

    text=tk.Text(window, height=7, width=50, padx=30, pady=20, yscrollcommand=yscrollbar.set)


    yscrollbar.config(command=text.yview)
    text.pack()

    def submitf(msc=string):
        msc.data+=text.get(1.0 , "end-1c")
        window.destroy()
    
    submit=tk.Button(window, text='SUBMIT', command=submitf)

    submit.pack()
    window.attributes('-topmost',1)
    window.mainloop()
    return string.data.strip()

def randomstring(length, nums=True, upper=True, lower=False) -> str:
    '''\
Return a random string'''
    choice_of_strings=deque()
    if nums:
        choice_of_strings.extend(deque(string.digits))
    if upper:
        choice_of_strings.extend(deque(string.ascii_uppercase))
    if lower:
        choice_of_strings.extend(deque(string.ascii_lowercase))
    return ''.join(random.choices(choice_of_strings, k=length)).strip()

if __name__!='__main__':
    sys.exit()


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
        return TrueFalseDict[s]
    else:
        raise ValueError('This string cannot be converted to True or False')
    


while True:
    try:
        proceed=input('Do you wish to proceed with the following (please make changes according to your need) [Y/n]?')
        proceed=mapTrueFalse(proceed)
        break
    except ValueError:
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
        while True:
            try:
                proceed=input('Are you satisfied [Y/n]?')
                break
            except ValueError:
                print('Invalid input')
                continue
                

    else:
        print('Your `item` is not allowed. ')
        continue

# begin password getting process
if 'idlelib.run' in sys.modules:
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

    def exists(
            value : Any,
            column : str,
            table : str,
            connection = connection,
            add_quotation=True
            ):
        """\
Tell if the given value exists in the given column in given table.

Set `add_quotation` to False if you don't want `"` being added to the
 front and back of the `value` automatically (If your `value` is not str).
"""
        if add_quotation:
            value='"'+value+'"'
        inner_cursor=connection.cursor()
        inner_cursor.execute(f'SELECT * from {table} where {column}={value};')
        data=inner_cursor.fetchall()
        return bool(data)

    def table_from_db(table:str, v='*', align='l') -> PrettyTable:
        '''Return the given table name as prettytable from database'''
        inner_cursor=connection.cursor()
        inner_cursor.execute(f'SELECT {v} FROM {table};')
        table = from_db_cursor(inner_cursor)
        if align is not False:
            table.align=align
        return table

    def show_patients():
        '''Prints table `patients` in python output'''
        patients = table_from_db('patients')

        fieldname='Sno'
        patients.field_names.insert(0, fieldname)
        patients.align[fieldname]='c'
        patients.valign[fieldname]='t'
        for i, _ in enumerate(patients.rows):
            patients.rows[i].insert(0, i+1)

        print(patients)

    def add_patient():
        '''\
Gets user input and adds a new patient in the table `patients`'''
        print('Adding new patient in table `patients` in database `SrisakthiPatients`')


        name=input('Enter patient name: ')
        phone=input('Enter phone number with country code: ')
        while (len(phone)>17 and (not phone.replace('+', '').replace('-', '').isdigit())):
            phone=input('Re-enter proper phone number: ')
        while exists(value=phone, column='phone', table='patients'):
            print('A patient with that phone number already exists.')
            phone=input('Re-enter proper phone number: ')

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


        while True:
            gender=input('Enter gender (M/F) : ')
            if gender in ('M', "F"):
                break
            else:
                print('''\
Invalid gender
Re-enter gender''')

        address=multilineinput("Enter address below")

        inner_cursor=connection.cursor()
        inner_cursor.execute(f'''INSERT INTO patients (name, phone, dob, gender, address)
VALUES ("{name}",  "{phone}", '{dob}', "{gender}", "{address}");''')
        connection.commit()

        print('New patient created')

    def update_patient():
        '''\
Gets user input and updates a patient in table `patients`'''
        while True:
            phone=input('Enter phone number of existing patient to update (or even show patients): ')
            if phone=='show patients':
                show_patients()
                continue
            else:
                if exists(value=phone, column='phone', table='patients'):
                    while True:
                        value_to_be_updated=input('Enter value to be updated: ').strip()
                        allowed_patient_update_values=('name', 'dob', 'phone', 'address', 'gender')
                        if value_to_be_updated in allowed_patient_update_values:
                            if value_to_be_updated=='address':
                                    the_value=multilineinput("Enter address below")
                            else:
                                    while True:
                                        try:
                                            the_value=eval(input('Enter the value (will be `eval`utated by python): '))
                                            if isinstance(the_value, str):
                                                the_value='"'+the_value+'"'
                                            break
                                        except (NameError, SyntaxError):
                                            print('ERROR, INVALID VALUE')
                                            continue
                            break
                        else:
                            print('Wrong item. Your item must be any of', allowed_patient_update_values, sep='\n')
                            continue
                else:
                    print('Wrong phone number. Re-enter it.')
                    continue
                inner_cursor=connection.cursor()
                inner_command=f'''UPDATE patients
SET {value_to_be_updated}="{the_value}" WHERE phone="{phone}";'''
                inner_cursor.execute(inner_command)
                connection.commit()
                print('Updated successfully')
                break

    def show_appointments():
        '''\
Shows all the appointments in `appointments` table'''
        inner_cursor=connection.cursor()
        inner_cursor.execute('''\
SELECT patients.Name, patients.Phone, appointments.treatmentID, appointments.Date, appointments.Time
FROM patients, appointments
WHERE patients.Phone=appointments.Phone;''')
        appointments=from_db_cursor(inner_cursor)

        fieldname='Sno'
        appointments.field_names.insert(0, fieldname)
        appointments.align[fieldname]='c'
        appointments.valign[fieldname]='t'
        for i, _ in enumerate(appointments.rows):
            appointments.rows[i].insert(0, i+1)

        print(appointments)

    def add_appointment():
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
            phone=input('Enter phone number of patient you want to create appointment: ').strip()
            if phone=='show patients':
                show_patients()
            elif phone=='add patient':
                add_patient()
            else:
                if exists(value=phone, column='phone', table='patients'):
                    break

                else:
                    print('Wrong phone number. A patient with that number does not exist.')
                    continue

        treatment_id=randomstring(8)
        while exists(value=treatment_id, column='treatmentID', table='appointments'):
            treatment_id=randomstring(8)

        inner_cursor=connection.cursor()
        inner_cursor.execute(f'''INSERT INTO Appointments (phone, treatmentID, date, time)
VALUES ("{phone}", "{treatment_id}", '{date}', '{time}');''')
        connection.commit()

        print('New appointment created')

    def update_appointment():
        '''\
Gets user input and updates an appointment in the table `appointments`'''
        print('You can update an appointment only if there is no `treatment` related to it')
        while True:
            treatment_id=input('''Enter treatmentID of appointment to update it:
(`show appointments` to show all appointments) > ''')
            if treatment_id=='show appointments':
                show_appointments()
                continue
            else:
                if exists(value=treatment_id, column='treatmentID', table='appointments'):
                    if not exists(value=treatment_id, column='treatmentID', table='treatments'):
                        break
                    else:
                        print('Wrong treatmentID. A treatment for that ID exists.')
                else:
                    print('Wrong treatmentID. An appointment with that ID does not exists.')
                    continue
            
        
        inner_cursor=connection.cursor()
        print('''\
Updatable values
- date
- time''')
        while True:
            value_to_be_updated=input('Enter value to be updated: ')
            allowed_appointment_update_values=('date', 'time')
            if value_to_be_updated in allowed_appointment_update_values:
                break
            else:
                print('It must either be `date` or `time`. Re enter it.')
                continue

        while True:  
            try:
                the_value=eval(input('Enter the value (will be `eval`utated by python): '))
                break
            except (NameError, SyntaxError):
                print("ERROR, CAN'T BE `EVAL`UATED.")
                continue

        inner_command=f'''UPDATE appointments
SET {value_to_be_updated}="{the_value}" WHERE treatmentID="{treatment_id}";'''
        inner_cursor.execute(inner_command)
        connection.commit()
        print('Updated successfully')

    def show_treatments():
        '''\
Shows all records in table `treatments`'''
        inner_command="""\
SELECT
patients.Name, patients.Phone,
treatments.treatmentID, doctors.Name AS "Name of Doctor", treatments.DoctorsPhone AS "Doctor's Phone", 
treatments.Date, treatments.Time, treatments.Treatment, treatments.Status, treatments.Fee,

CASE treatments.Paid
WHEN 0 THEN "False"
WHEN 1 THEN "True"
END AS Paid

FROM
patients


JOIN appointments
ON patients.Phone=appointments.Phone
JOIN treatments
ON treatments.TreatmentID=appointments.TreatmentID
JOIN doctors
ON doctors.Phone=treatments.DoctorsPhone;"""
        inner_cursor=connection.cursor()
        inner_cursor.execute(inner_command)
        treatments=from_db_cursor(inner_cursor)

        fieldname='Sno'
        treatments.field_names.insert(0, fieldname)
        treatments.align[fieldname]='c'
        treatments.valign[fieldname]='t'
        for i, _ in enumerate(treatments.rows):
            treatments.rows[i].insert(0, i+1)

        print(treatments)

    def add_treatment():
        '''\
Gets user input and adds a treatment to table `treatments`'''
        while True:
            print('Enter treatmentID (from table `appointments`) below:')
            treatment_ID=input('(also `show appointments` or `add appointment`) : ')

            if treatment_ID=='show appointments':
                show_appointments()
                continue
            elif treatment_ID=='add appointment':
                add_appointment()
                continue
            else:
                if not exists(value=treatment_ID, column='treatmentID', table='appointments'):
                    print('Invalid treatmentID. It does not exist in table `appointments`.')
                    continue
                elif exists(value=treatment_ID, column='treatmentID', table='treatments'):
                    print('''Date format: YYYY-MM-DD
Example: 1999-03-12''')

                    DoctorsPhone=input('Enter the phone of doctor of this treatments (also `show doctors`): ')

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

                    status=multilineinput('''What is the status of the treatment?
You can also add the prescription here''')

                    while True:
                        fee=eval(input('Enter amount in rupees (without symbols) : '))
                        if not isinstance(fee, (int, float)):
                            print('Should be integer or decimal')
                            continue
                        break

                    while True:
                        try:
                            paid=input('Is the payment complete [True/False] ?')
                            paid=mapTrueFalse(paid)
                            break
                        except ValueError as v:
                            print('You entered',v)
                            print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                            continue

                    if exists(value=DoctorsPhone, column='Phone', table='doctors'):
                        inner_command=f'''INSERT INTO treatments (treatmentID, DoctorsPhone, date, time, treatment, status, fee, paid)
VALUES ("{treatment_ID}", "{DoctorsPhone}", "{date}", "{time}", "{treatment}", "{status}", {fee}, {paid});'''
                        inner_cursor=connection.cursor()
                        inner_cursor.execute(inner_command)
                        connection.commit()
                        print('Added successfully')
                        break
                    else:
                        print("Wrong phone number of doctor")
                else:
                    print('An appointment with the given treatmentID does not exist.')
                    continue

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
                if not exists(value=treatmentID, column='treatmentID', table='appointments'):
                    print('Wrong treatmentID. Appointment does not exist.')
                    continue
                else:
                    if exists(value=treatmentID, column='treatmentID', table='treatments'):
                        print('Wrong treatmentID. Treatment exists.')
                        continue
                    else:
                        inner_cursor=connection.cursor()
                        inner_cursor.execute(f'SELECT date, time from appointments WHERE treatmentID="{treatmentID}";')
                        (date, time)=inner_cursor.fetchall()[0]
                        date=date.strftime('%Y-%m-%d')
                        time=str(time)

                        treatment=input('What treatment it is ? ')

                        status=multilineinput('''What is the status of the treatment?
You can also add the prescription here''')

                        while True:
                            fee=eval(input('Enter amount in rupees (without symbols) : '))
                            if not isinstance(fee, (int, float)):
                                print('Should be integer or decimal')
                                continue
                            break

                        while True:
                            try:
                                paid=input('Is the payment complete [True/False] ?')
                                paid=mapTrueFalse(paid)
                                break
                            except ValueError as v:
                                print('You entered',v)
                                print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                                continue    

                        while True:    
                            DoctorsPhone=input('Enter the phone of doctor of this treatments (also `show doctors`): ')
                            if exists(value=DoctorsPhone, column="Phone", table="doctors"):
                                command=f'''\
INSERT INTO treatments (treatmentID, DoctorsPhone, date, time, treatment, status, fee, paid)
VALUES ("{treatmentID}", "{DoctorsPhone}", "{date}", "{time}", "{treatment}", "{status}", {fee}, {paid});'''
                                inner_cursor=connection.cursor()
                                inner_cursor.execute(command)
                                connection.commit()
                                print('Added Successfully')
                                break
                            elif DoctorsPhone=='show doctors':
                                show_doctors()
                                continue
                            else:
                                print("Wrong phone number of doctor")
                                continue
                        
                        break

    def update_treatment():
        '''\
Gets user input and updates a record in table `treatments`'''
        while True:
            print('Enter treatmentID below:')
            treatment_ID=input('(even `show treatments`) >')
            if treatment_ID=='show treatments':
                show_treatments()
                continue
            else:
                if not exists(value=treatment_ID, column='treatmentID', table='treatments'):
                    print('Wrong treatmentID. Enter again.')
                    continue
                else:
                    break

        print('''`update treatment` options
    0 : treatment name
    1 : status
    2 : paid (if payment is over)

NOTE: You can\'t update anything else''')
        while True:
            try:
                choice=int(input('Update what? '))
                break
            except (TypeError, ValueError):
                print('Invalid Input')
                continue

        while True:
            if choice==0:
                treatment=input('Enter (new) name of treatment: ')
                inner_cursor=connection.cursor()
                inner_cursor.execute(f'''UPDATE treatments
SET treatment="{treatment}"
WHERE treatmentID="{treatment_ID}"''')
                print('Updated successfully')
                break

            elif choice==1:
                status=multilineinput('''What is the status of the treatment?
You can also add the prescription here''')
                inner_command=f'''UPDATE treatments
SET status="{status}" WHERE treatmentID="{treatment_ID}";'''
                inner_cursor=connection.cursor()
                inner_cursor.execute(inner_command)
                connection.commit()
                print('Updated successfully')
                break

            elif choice==2:
                while True:
                    try:
                        paid=input('Is the payment complete now [True/False] ?')
                        paid=mapTrueFalse(paid)
                        break
                    except ValueError as v:
                        print('You entered',v)
                        print('Anything other than `True`, `False`, `0`, `1` cannot be accepted')
                        continue

                inner_command=f'''UPDATE treatments
SET paid={paid} WHERE treatmentID="{treatment_ID}";'''
                inner_cursor=connection.cursor()
                inner_cursor.execute(inner_command)
                connection.commit()
                print('Updated Successfully')
                break
        
            else:
                print('Invalid Input')
                continue

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
                if not exists(value=treatmentID, column='treatmentID', table='appointments'):
                    print('Wrong treatmentID. It does not exist.')
                    continue
                elif exists(value=treatmentID, column='treatmentID', table='treatments'):
                    print('Wrong treatmentID. There is a treatment associated with it.')
                    continue
                else:
                    inner_cursor=connection.cursor()
                    inner_cursor.execute(f'''DELETE FROM appointments
WHERE treatmentID="{treatmentID}";''')
                    print('Deleted successfully')                       

    def show_doctors():
        """Shows the table `doctors`"""
        doctors=table_from_db('doctors')
        fieldname='Sno'
        doctors.field_names.insert(0, fieldname)
        doctors.align[fieldname]='c'
        doctors.valign[fieldname]='t'
        for i, _ in enumerate(doctors.rows):
            doctors.rows[i].insert(0, i+1)
        print(doctors)

    def show_treatments_of_patient():
        """Shows the list of treatments of a particular patient in table form"""
        while True:
            phone=input('''\
Enter phone number of existing patient to show their treatments
(or even show patients): ''')
            if phone=='show patients':
                show_patients()
                continue
            else:
                if exists(value=phone, column='phone', table='patients'):
                    inner_cursor=connection.cursor()
                    inner_command=(f'''\
SELECT
patients.Name, patients.Phone,
treatments.treatmentID, doctors.Name AS "Name of Doctor", treatments.DoctorsPhone AS "Doctor's Phone", 
treatments.Date, treatments.Time, treatments.Treatment, treatments.Status, treatments.Fee,

CASE treatments.Paid
WHEN 0 THEN "False"
WHEN 1 THEN "True"
END AS Paid

FROM
patients


JOIN appointments
ON patients.Phone=appointments.Phone
JOIN treatments
ON treatments.TreatmentID=appointments.TreatmentID
JOIN doctors
ON doctors.Phone=treatments.DoctorsPhone;''')
                    inner_cursor.execute(inner_command)
                    table=from_db_cursor(inner_cursor)

                    df=pd.DataFrame(table.rows, columns=table.field_names)
                    # print(df.to_string(index=False, ))
                    temp=PrettyTable(field_names=table.field_names)

                    for index, value in enumerate(df["Phone"]):
                            if value==phone:
                                temp_row=list(df.loc[index])
                                temp_row[6]=str(temp_row[6])[-8:]
                                temp.add_row(temp_row)
                    print(temp)
                    break

                else:
                    print("Wrong phone number. Re-enter it.")
                    continue

    def show_treatments_of_doctor():
        while True:
            DoctorsPhone=input('''\
Enter phone number of a doctor to show their treatments
(or even `show doctors`): ''')
            if DoctorsPhone=='show doctors':
                show_doctors()
                continue
            else:
                if exists(value=DoctorsPhone, column='Phone', table='doctors'):
                    inner_cursor=connection.cursor()
                    inner_command=(f'''\
SELECT
patients.Name, patients.Phone,
treatments.treatmentID, doctors.Name AS "Name of Doctor", treatments.DoctorsPhone AS "Doctor's Phone", 
treatments.Date, treatments.Time, treatments.Treatment, treatments.Status, treatments.Fee,

CASE treatments.Paid
WHEN 0 THEN "False"
WHEN 1 THEN "True"
END AS Paid

FROM
patients


JOIN appointments
ON patients.Phone=appointments.Phone
JOIN treatments
ON treatments.TreatmentID=appointments.TreatmentID
JOIN doctors
ON doctors.Phone=treatments.DoctorsPhone;''')
                    inner_cursor.execute(inner_command)
                    table=from_db_cursor(inner_cursor)

                    df=pd.DataFrame(table.rows, columns=table.field_names)

                    temp=PrettyTable(field_names=table.field_names)

                    for index, value in enumerate(df["Doctor's Phone"]):
                            if value==DoctorsPhone:
                                temp_row=list(df.loc[index])
                                temp_row[6]=str(temp_row[6])[-8:]
                                temp.add_row(temp_row)
                    print(temp)
                    break

                else:
                    print("Wrong phone number of doctor. Re-enter it.")
                    continue

    def add_doctor():
        """Add a doctor record to the list of doctors in the table `doctors`"""
        Name=input("Enter name of the doctor: ")

        while True:
            Phone=input("Enter the phone number of doctor (with country code): ")
            if len(Phone)>17:
                print("Phone number with country code can't be more than 17 digits. Re-enter it.")
                continue
            else:
                break

        Qualification=input("Enter qualifications of the doctor: ")
        Role=input("Enter the role of the doctor in the clinic: ")

        Special_In=input("""\
(Type `None` or `null` if this doctor is not a specialist)
Specialist in what? """)
        if Special_In.lower() in ("none", "null"):
            Special_In='NULL'
        else:
            Special_In='"'+Special_In+'"'

        inner_cursor=connection.cursor()
        inner_cursor.execute(f"""\
INSERT INTO doctors (Phone, Name, Qualification, Role, Special_In) values
("{Phone}", "{Name}", "{Qualification}", "{Role}", {Special_In});""")
        connection.commit()
        print("Added successfully")

    def update_doctor():
        """Update a doctor record in the table `doctors`"""
        while True:
            Phone=input("""\
Enter the phone number of the doctor you wan't to update values
(also `show doctors`): """)
            if Phone=='show doctors':
                show_doctors()
                continue
            elif exists(value=Phone, column="Phone", table='doctors'):
                break
            else:
                print("Phone number does'nt exist. Re-enter it")
                continue



        print("Values that can be updated: ")

        v = tuple(pd.read_sql("desc doctors;", con=connection)['Field'])
        values_that_can_be_updated=pd.Series(v)
        print(values_that_can_be_updated.to_string())

        while True:
            value_to_be_updated = input("Which value do you wan't to update (enter the number before it)? ")
            try: 
                value_to_be_updated=int(value_to_be_updated)
            except ValueError as VE:
                print(VE)
                print("Re-enter it.")
                continue
            else:
                if 0<=value_to_be_updated<=len(v):
                    print(f"Would you like to confirm you have selected to update {v[value_to_be_updated]}?")

                    while True:
                        confirmation=input("Yes/no: ")
                        if confirmation.lower().strip() in ('yes', 'y', '1', 'true'):
                            confirmation=True
                            break
                        elif confirmation.lower.strip() in ('no', 'n', 0, 'false'):
                            confirmation=False
                            break
                        else:
                            print("Wrong input for confirming selected item. Re-enter it")
                            continue
                    
                    if confirmation:
                        print("Confirmed")
                        break
                    else:
                        print("Re-select it")
                        continue

                else:
                    print("Invalid Input. Re-enter it.")
                    continue
        
        new_value=input(f"Enter new value of {v[value_to_be_updated]} : ")

        if value_to_be_updated==4: # Special_In
            if new_value.lower().strip() in ('null', 'none', '0'):
                new_value='NULL'
            else:
                new_value='"'+new_value+'"'

        inner_cursor=connection.cursor()
        inner_command=f"""
UPDATE `doctors`
SET {v[value_to_be_updated]} = {new_value}
WHERE Phone={Phone};"""
        inner_cursor.execute(inner_command)
        connection.commit()
        print("Updated successfully")


    while True:
        command=input('Enter command> ')
        command=command.strip().lower()

        if command.startswith('help'):
            print(helper.process_help(command))

        elif command in ('exit', 'quit'):
            break

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
        
        elif command=='show doctors':
            show_doctors()

        elif command=='show treatments of patient':
            show_treatments_of_patient()

        elif command=='show treatments of doctor':
            show_treatments_of_doctor()

        elif command=='add doctor':
            add_doctor()
        
        elif command=='update doctor':
            update_doctor()

        else:
            print("WRONG COMMAND [See `help`]")

    print('logout')
    connection.close()
else:
    print('Connection to MySQL Database SriSakthiPatients FAILED')
