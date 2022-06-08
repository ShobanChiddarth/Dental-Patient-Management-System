"""\
DENTAL PATIENT MANAGEMENT SYSTEM CLI
====================================

This is the script of the CLI app. The script is made as a CLI with the help
of [click](https://palletsprojects.com/p/click). This offers all
functionalities of the [old script](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/blob/31b994185e733120252cad1afd520ee2d5ea1055/src/main.py)
but as a CLI app. This is meant to provide a Command Line Interface as an API,
with which the main script can be re-written using this API.

NOTE: dpms is not a module and should not be tried to import from anywhere.
"""
import string

from collections import deque
import json
import pprint
import random
from typing import Any
from mysql import connector
from mysql.connector.connection_cext import CMySQLConnection
from prettytable import PrettyTable, from_db_cursor
import click

import sqlconfig


def randomString(length, nums=True, upper=True, lower=False) -> str:
    '''\
Return a (pseudo)-random string

PARAMETERS
----------
- length : length of your random string
- nums   : wether or not to include digits (0-9) in your random string
- upper  : wether or not to include upper cased characters in your random string
- lower  : wether or not to include lower cased characters in your random string
'''
    choiceOfStrings=deque()
    if nums:
        choiceOfStrings.extend(deque(string.digits))
    if upper:
        choiceOfStrings.extend(deque(string.ascii_uppercase))
    if lower:
        choiceOfStrings.extend(deque(string.ascii_lowercase))
    return ''.join(random.choices(choiceOfStrings, k=length)).strip()

def exists(
            value : Any,
            column : str,
            table : str,
            connection : CMySQLConnection,
            quote=True
            ):
        """\
Tell if the given value exists in the given column in given table.

Set `add_quotation` to False if you don't want `"` being added to the
 front and back of the `value` automatically (If your `value` is not str).
"""
        if quote:
            value='"'+value+'"'
        inner_cursor=connection.cursor()
        inner_cursor.execute(f'SELECT * from {table} where {column}={value};')
        data=inner_cursor.fetchall()
        return bool(data)

def tableFromDB(connection:CMySQLConnection, table:str, v='*', align='l') -> PrettyTable:
    '''\
Return the given table name as prettytable from database

PARAMETERS
----------
- connection : the mysql connection with the database you want to look up
- table      : the name of the table you want as PrettyTable
- v          : the values you want to be selected from the table
- align      : what do you want the table to be aligned as?
'''
    innerCursor=connection.cursor()
    innerCursor.execute(f'SELECT {v} FROM {table};')
    ptable = from_db_cursor(innerCursor)
    if align is not False:
        ptable.align=align
    return ptable

def isValidDate(date : str) -> bool:
    """\
Tell if the given date is a valid date or not.

Valid means it is in the format `YYYY-MM-DD`
Example: 2000-03-04
Which is March 4, 2000
"""
    return bool(date[0:4].isdigit() and 
            date[4]=='-' and 
            date[5:7].isdigit() and 
            date[7]=='-' and
            date[8:10].isdigit()
            and len(date)==10)

def isValidTime(time : str, includeSeconds : bool = False):
    """\
Tell if the given time is a proper time or not

PARAMETERS
----------
includeSeconds : wether or not to include seconds in the calculation

if seconds are included, tell if the time format is like `HH:MM:SS`

else, tell if the time format is like `HH:MM`
"""
    if includeSeconds:
        return bool(time[0:2].isdigit() and
                    time[2]==':' and
                    time[3:5].isdigit() and
                    time[5]==':' and
                    time[5:8].isdigit() and
                    len(time)==8) 
    else:
        return bool(time[0:2].isdigit() and
                    time[2]==':' and
                    time[3:5].isdigit() and
                    len(time)==5)

def isValidPhone(phone : str):
    """\
Tell if the given phone is a proper phone number

(if it is lesser than 17 characters and consists of only digits
(excluding '+' and '-' characters))
"""
    return bool(len(phone)>17 and (not phone.replace('+', '').replace('-', '').isdigit()))

def addSerialNo(table : PrettyTable, fieldname: str ='Sno', startFrom0 : bool = False) -> PrettyTable:
    """\
Adds a column {fieldname} (serial numbers) to a given PrettyTable in the front

NOTE: It also returns the table

PARAMETERS
----------
1. `table`     : an instance of prettytable.Prettytable
2. `fieldname` : what should the serial number column have as a heading
3. `startFrom0`: should the serial number counting start from 0?
"""
    table.field_names.insert(0, fieldname)
    table.align[fieldname]='c'
    table.valign[fieldname]='t'
    if startFrom0:
        for i, _ in enumerate(table.rows):
            table.rows[i].insert(0, i)
    else:
        for i, _ in enumerate(table.rows):
            table.rows[i].insert(0, i+1)
    
    return table


class SpecialHelpOrder(click.Group):
    """\
This code was taken from [StackOverflow](https://stackoverflow.com/a/47984810/14195452)

Stack Overflow Answer
=====================
The order of the commands listed by help is set by the list_commands() method of the click.Group
class. So, one way to approach the desire to change the help listing order is to inherit for
click.Group and override list_commands to give the desired order.

Custom Class
------------
This class overrides the click.Group.command() method which is used to decorate command functions.
It adds the ability to specify a help_priority, which allows the sort order to be modified as desired.
"""
    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(SpecialHelpOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(SpecialHelpOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(SpecialHelpOrder, self).list_commands(ctx)
        return (c[1] for c in sorted(
            (self.help_priorities.get(command, 1), command)
            for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop('help_priority', 1)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(SpecialHelpOrder, self).command(*args, **kwargs)(f)
            help_priorities[cmd.name] = help_priority
            return cmd

        return decorator


@click.group(cls=SpecialHelpOrder)
def cli():
    """\
Dental Patient Management System CLI

\b
DPMS stands for Dental Patient Management System.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
<https://github.com/ShobanChiddarth/Dental-Patient-Management-System/blob/dpms-cli/LICENSE>

\b
This is a CLI application, used to manage a database like the one in
https://github.com/ShobanChiddarth/Dental-Patient-Management-System/blob/5019db80eaf7897b9065efb5b12d661d0a62fdd4/backup.sql.

\b
Pre-requisites
--------------
- MySQL server with a database "SrisakthiPatients"
- The database "SrisakthiPatients" should have the data in backup.sql loaded
- Python (3.10.2 is better)
- The modules listed in requirements.txt

Usage

This is solely indented to be used by the doctor of a dental clinic.
After all, this is a Dental Patient Management System.
The database has 3 tables, namely, `patients`, `appointments` and `treatments`.
You have to store the record of each patient in the table `patients`, their
appointments in `appointments` table and the treatment records in `treatments` table.
The link between a patient and his appointment, and the appointment with the treatment
for the appointment is the `treatmentID`.

Whenever you add a patient, you will have to use the phone number of that patient to
create an appointment for him and you will get a treatmentID automatically. You have
to create a treatment record for him with the treatmentID. This setup is indented for
a clinic which functions like you give a treatment for the patient only with the
appointment (patient has to come only with an appointment), patient, appointment,
treatment records are stored separately.

\b
NOTE
----
- Payment related stuff are not brought in as this is a school project.
- You get the output in the terminal you are using this.
"""
    pass


# begin `myHelpDeterminer`
total=14
myHelpDeterminer=iter(range(total))
# I have put this piece of code here in order to
# set the help_order of every command in the same
# order they are created in this script. This is
# very useful as one does not have to edit every
# first line of command declaration when declaring
# a new command in the begginning or somewhere in
# the middle (`@cli.command(help_priority=int)`)
# just use `next(myHelpDeterminer)` in the place of
# `int` to show the command in the same order in the
# script. Make sure to edit the value of `total` (set
# it to the total number of commands so that we don't
# get StopIteration error when iterating more than the
# length of range)


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--jsonoutput', is_flag=True, default=False)
def load_allowed(jsonoutput):
    """\
Print the list of all "allowed" configuration arguement keys.

\b
Input Flags
-----------
- `--jsonOutput`
  decides wether or not to give the output in json format
  If given -> print it using json.dumps
  Else -> print it in python format
"""
    if jsonoutput:
        print(json.dumps(sqlconfig.load.load_allowed(1), indent=4))
    else:
        print(pprint.pformat(sqlconfig.load.load_allowed(1), indent=4, sort_dicts=False).replace("'", '"'))


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--jsonoutput', is_flag=True, default=False)
def read_config(jsonoutput):
    """\
Print the list of all "allowed" configuration arguement keys.

\b
Input Flags
-----------
- `--jsonOutput`
  decides wether or not to give the output in json format
  If given -> print it using json.dumps
  Else -> print it in python format
"""
    if jsonoutput:
        print(json.dumps(sqlconfig.load.load_data(1), indent=4))
    else:
        print(pprint.pformat(sqlconfig.load.load_data(1), indent=4, sort_dicts=False).replace("'", '"'))


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--key', 'key', required=True, type=click.STRING, prompt=False)
@click.option('--value', 'value', required=True, prompt=False)
@click.option('--evaluate', is_flag=True, default=False)
def config(key, value, evaluate):
    """\
Configuration command: Uses the module `sqlconfig`


Input Format
------------
- key (--key) must be an "allowed" value.

\b
Allowed values are values that can be passed as an kwarg to
mysql.connector.connect function. They can be found here
https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html

To get the list of allowed values, use `loadAllowed` command.
"""
    if evaluate:
        value=eval(value)

    connectionDict=sqlconfig.load.load_data(1)
    sqlconfig.manage.safe_edit(connectionDict, key=key, value=value)
    sqlconfig.manage.flushdict(connectionDict)


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--key', 'key', required=True, type=click.STRING, prompt=False)
def del_config(key):
    """"""
    connectionDict=sqlconfig.load.load_data(1)
    del connectionDict[key]
    sqlconfig.manage.flushdict(connectionDict)


@cli.command(help_priority=next(myHelpDeterminer))
@click.password_option('-p', '--password', confirmation_prompt=False, required=True, type=click.STRING)
def show_patients(password):
    '''\
Prints table `patients`
'''
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)
    patients=tableFromDB(innerConnection, 'patients')

    addSerialNo(patients)

    print(patients)
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--name', 'name', type=click.STRING, required=True, prompt=True)
@click.option('--phone', 'phone', type=click.STRING, required=True, prompt=True)
@click.option('--dob', 'dob', type=click.STRING, required=True, prompt=True)
@click.option('--gender', 'gender', type=click.STRING, required=True, prompt=True)
@click.option('--address', 'address', type=click.STRING, required=True, prompt=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def add_patient(name, phone, dob, gender, address, password):
    """\
Adds a new record to table `patients`

\b
Input Format
------------
- Date Of Birth (--dob): `YYYY-MM-DD`. Example: `1999-03-12`
- Gender (--gender): Must be "M" or "F"
- Address (--address): can be multi-lined
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)


    if not isinstance(name, str):
        raise TypeError('arguement `name` must be a string')

    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif isValidPhone(phone):
        raise ValueError('It is not a proper phone number')
    elif exists(value=phone, column='phone', table='patients', connection=innerConnection):
        raise ValueError('A patient with that phone number already exists')

    if not isinstance(dob, str):
        raise TypeError('arguement `dob` must be a string')
    elif not isValidDate(dob):
        raise ValueError('This is not a proper Date Of Birth')

    if gender not in ('M', 'F'):
        raise ValueError('`gender` must be "M" or "F"')

    if not isinstance(address, str):
        raise TypeError('arguement `address` must be a string')

    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''INSERT INTO patients (name, phone, dob, gender, address)
VALUES ("{name}",  "{phone}", '{dob}', "{gender}", "{address}");''')
    innerConnection.commit()
    print('Successfully added a new patient')
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--phone', 'phone', required=True, type=click.STRING, prompt=True)
@click.option('--column', 'column', required=True, type=click.STRING, prompt=True)
@click.option('--value', 'value', required=True, prompt=True)
@click.option('--quote/--no-quote', default=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def update_patient(phone, column, value, quote, password):
    """
Updates the record of a patient with the given `value` in the given `column`

\b
Input Format
------------
- Column (--column): must be a string any of ('name', 'phone', 'dob', 'gender', 'address')
- --quote (wether or not to add quotations(") in the front and back of `--value` (is a flag)
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)



    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif not exists(value=phone, column='phone', table='patients', connection=innerConnection):
        raise ValueError('A patient with that phone number does not exists.')

    allowed_update_patient_columns=('name', 'phone', 'dob', 'gender', 'address')

    if not isinstance(column, str):
        raise TypeError('arguement `phone` must be a string')
    elif column not in allowed_update_patient_columns:
        raise ValueError(f"`column` must be any of {allowed_update_patient_columns}")
    else:
        if column=='phone':
            if not isValidPhone(value):
                raise ValueError('The given phone number is not a proper phone number')
        elif column=='dob':
            if not isValidDate(value):
                raise ValueError('The given date of birth is not a valid date')
        elif column=='gender':
            if not value in ('M', 'F'):
                raise ValueError('Gender must be (M)ale or (F)emale')

    if quote:
        value='"'+value+'"'

    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
UPDATE patients
SET {column}={value}
WHERE phone="{phone}";''')
    innerConnection.commit()
    print('Updated successfully')
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def show_appointments(password):
    """\
Print the table `appointments`
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    innerCursor=innerConnection.cursor()
    innerCursor.execute('''\
SELECT patients.Name, patients.Phone, appointments.treatmentID, appointments.Date, appointments.Time
FROM patients, appointments
WHERE patients.phone=appointments.phone;''')
    appointments=from_db_cursor(innerCursor)

    addSerialNo(appointments)
    
    print(appointments)
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--phone', 'phone', required=True, type=click.STRING, prompt=True)
@click.option('--date', 'date', required=True, type=click.STRING, prompt=True)
@click.option('--time', 'time', required=True, type=click.STRING, prompt=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def add_appointment(phone, date, time, password):
    """\
Adds a new record to table `patients`

\b
Input Format
------------
- Time (--time): `HH:MM` (Example: "13:50")
- Date (--date): `YYYY-MM-DD` (Example: `1993-04-20`)
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif not isValidPhone(phone):
        raise ValueError('It is not a proper phone number')
    elif not exists(value=phone, column='phone', table='patients', connection=innerConnection):
        raise ValueError('A patient with that phone does not exists')

    if not isValidDate(date):
        raise ValueError('improper `date` format')

    if not isValidTime(time):
        raise ValueError('improper `time` format')
    
    treatmentID=randomString(8)
    while exists(value=treatmentID, column='treatmentID', table='appointments', connection=innerConnection):
        treatmentID=randomString(8)
    
    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
INSERT INTO Appointments (phone, treatmentID, date, time)
VALUES ("{phone}", "{treatmentID}", "{date}", "{time}");''')
    innerConnection.commit()
    print('Added successfully')
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.option('--column', 'column', required=True, type=click.STRING, prompt=True)
@click.option('--value', 'value', required=True, prompt=True)
@click.option('--quote/--no-quote', default=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def update_appointment(treatmentID, column, value, quote, password):
    """
Update an appointment with the given `value` in the given `column`

\b
Input Format
------------
- Column (--column): must be a string and any of ("date", "time")
- --quote (wether or not to add quotations(") in the front and back of `--value` (is a flag)
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)


    if not isinstance(treatmentID, str):
        raise TypeError('arguement `phone` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='appointments', connection=innerConnection):
        raise ValueError('An appointment with that phone number does not exists.')

    allowedUpdateAppointmentColumns=('date','time')

    if not isinstance(column, str):
        raise TypeError('arguement `phone` must be a string')
    elif column not in allowedUpdateAppointmentColumns:
        raise ValueError(f"`column` must be any of {allowedUpdateAppointmentColumns}")
    else:
        if column=='date':
            if not isValidDate(value):
                raise ValueError('The given date is not a valid date')
        elif column=='time':
            if not isValidTime(value):
                raise ValueError('The given time is not a valid time')

    if quote:
        value='"'+value+'"'

    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
UPDATE appointments
SET {column}={value}
WHERE treatmentID="{treatmentID}";''')
    innerConnection.commit()
    print('Updated successfully')
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def remove_appointment(treatmentID, password):
    """\
Removes an appointment record if only there is no treatment related to it.
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    if not isinstance(treatmentID, str):
        raise ValueError('`treatmentID` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='appointments', connection=innerConnection):
        raise ValueError('given `treatmentID` does not exist in appointments')
    elif exists(value='treatments', column='treatmentID', table='treatments', connection=innerConnection):
        raise ValueError('a treatment exists with the given `treatmentID`')

    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
DELETE FROM appointments
WHERE treatmentID="{treatmentID}";''')
    innerConnection.commit()
    print("Deleted successfully")
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.password_option('-p','--password', required=True, type=click.STRING, confirmation_prompt=False)
def show_treatments(password):
    """\
Print the table `treatments`
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    innerCursor=innerConnection.cursor()
    innerCursor.execute("""\
SELECT
patients.Name, patients.Phone,
treatments.treatmentID, treatments.Date, treatments.Time, treatments.Treatment, treatments.Status, treatments.Fee,
CASE treatments.Paid
WHEN 0 THEN "False"
WHEN 1 THEN "True"
END AS Paid
FROM
patients
JOIN appointments
ON patients.phone=appointments.phone
JOIN treatments
ON treatments.treatmentID=appointments.treatmentID;""")
    treatments=from_db_cursor(innerCursor)

    addSerialNo(treatments)

    treatments.align['Treatment']='l'
    treatments.align['Status']='l'
    print(treatments)
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.option('--date', 'date', required=True, type=click.STRING, prompt=True)
@click.option('--time', 'time', required=True, type=click.STRING, prompt=True)
@click.option('--treatment', 'treatment', required=True, type=click.STRING, prompt=True)
@click.option('--status', 'status', required=True, type=click.STRING, prompt=True)
@click.option('--fee', 'fee', required=True, type=click.FLOAT, prompt=True)
@click.option('--paid/--not-paid', required=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def add_treatment(treatmentID, date, time, treatment, status, fee, paid, password):
    """\
Add a new record to the table `treatments`

\b
Input Format
------------
- date: `YYYY-MM-DD`. Example: `1999-03-12`
- time: `HH:MM` (24-hr format). Example: `13:50`
- status: can be multi lined
- fee: must be a floating point number
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    if not isinstance(treatmentID, str):
        raise TypeError('`treatmentID` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='appointments', connection=innerConnection):
        raise ValueError('an appointment with the given `treatmentID` does not exist')

    if not isinstance(date, str):
        raise TypeError('`date` must be a string')
    elif not isValidDate(date):
        raise ValueError('improper `date` format')

    if not isinstance(time, str):
        raise TypeError('`time` must be a string')
    elif not isValidTime(time):
        raise ValueError('improper `time` format')

    if not isinstance(treatment, str):
        raise TypeError('`treatment` must be a sting')

    if not isinstance(status, str):
        raise TypeError('`status` must be a string')

    fee=float(fee) # It will raise error automatically if it is a wrong input for `fee`

    # no need to check type for `paid` because it is already boolean
    # https://click.palletsprojects.com/en/8.1.x/options/#boolean-flags

    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
INSERT INTO treatments (treatmentID, date, time, treatment, status, fee, paid)
VALUES ("{treatmentID}", "{date}", "{time}", "{treatment}", "{status}", {fee}, {paid});''')
    innerConnection.commit()
    print('Added successfully')
    innerConnection.close()


@cli.command(help_priority=next(myHelpDeterminer))
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.option('--column', 'column', required=True, type=click.STRING, prompt=True)
@click.option('--value', 'value', required=True, prompt=True)
@click.option('--quote/--no-quote', default=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def update_treatment(treatmentID, column, value, quote, password):
    """\
Update a treatment with the `given` value in the given `column`

\b
Input Format
------------
- Column (--column): must be any of ("date", "time", "treatment", "status", "fee", "paid")
"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    innerConnection=connector.connect(**connectionDict)

    if not isinstance(treatmentID, str):
        raise TypeError('`treatmentID` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='treatments', connection=innerConnection):
        raise ValueError('Given `treatmentID` does not exist in table `treatments`')
    
    allowedTreatmentUpdateValues=("date", "time", "treatment", "status", "fee", "paid")
    if not isinstance(column, str):
        raise TypeError('`column` must be a string')
    elif column not in allowedTreatmentUpdateValues:
        raise ValueError(f'`column` must be any of {allowedTreatmentUpdateValues}')
    else:
        if column=='date':
            if not isValidDate(value):
                raise ValueError('It is not a proper date')
        elif column=='time':
            if not isValidTime(value):
                raise ValueError('It is not a proper time')
    
    if quote:
        value='"'+value+'"'
    
    innerCursor=innerConnection.cursor()
    innerCursor.execute(f'''\
UPDATE treatments
SET {column}={value}
WHERE treatmentID="{treatmentID}";''')
    innerConnection.commit()
    print('Updated successfully')
    innerConnection.close()



if __name__=='__main__':
    cli(prog_name='dpms')
