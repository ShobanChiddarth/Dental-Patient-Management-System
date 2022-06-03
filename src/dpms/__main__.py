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
from mysql.connector.connection_cext import CMySQLConnection
from prettytable import PrettyTable, from_db_cursor
from pyautogui import password
from pwinput import pwinput
import click

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

def exists(
            value : Any,
            column : str,
            table : str,
            connection : CMySQLConnection,
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

def table_from_db(connection:CMySQLConnection, table:str, v='*', align='l') -> PrettyTable:
    '''Return the given table name as prettytable from database'''
    inner_cursor=connection.cursor()
    inner_cursor.execute(f'SELECT {v} FROM {table};')
    ptable = from_db_cursor(inner_cursor)
    if align is not False:
        ptable.align=align
    return ptable


class SpecialHelpOrder(click.Group):
    """This code was taken from [StackOverflow](https://stackoverflow.com/a/47984810/14195452)"""
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
    pass

@cli.command(help_priority=0)
@click.password_option('-p', '--password', confirmation_prompt=False, required=True, type=click.STRING)
def show_patients(password):
    '''Prints table `patients`'''
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    inner_connection=connector.connect(**connectionDict)
    patients=table_from_db(inner_connection, 'patients')

    fieldname='Sno'
    patients.field_names.insert(0, fieldname)
    patients.align[fieldname]='c'
    patients.valign[fieldname]='t'
    for i, _ in enumerate(patients.rows):
        patients.rows[i].insert(0, i+1)

    print(patients)


@cli.command(help_priority=1)
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
    inner_connection=connector.connect(**connectionDict)


    if not isinstance(name, str):
        raise TypeError('arguement `name` must be a string')

    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif (len(phone)>17 and (not phone.replace('+', '').replace('-', '').isdigit())):
        raise ValueError('It is not a proper phone number')
    elif exists(value=phone, column='phone', table='patients', connection=inner_connection):
        raise ValueError('A patient with that phone number already exists')

    if not isinstance(dob, str):
        raise TypeError('arguement `dob` must be a string')
    elif not (dob[0:4].isdigit() and 
                            dob[4]=='-' and 
                            dob[5:7].isdigit() and 
                            dob[7]=='-' and
                            dob[8:10].isdigit()
                            and len(dob)==10 ):
        raise ValueError('This is not a proper Date Of Birth')

    if gender not in ('M', 'F'):
        raise ValueError('`gender` must be "M" or "F"')

    if not isinstance(address, str):
        raise TypeError('arguement `address` must be a string')

    inner_cursor=inner_connection.cursor()
    inner_cursor.execute(f'''INSERT INTO patients (name, phone, dob, gender, address)
VALUES ("{name}",  "{phone}", '{dob}', "{gender}", "{address}");''')
    inner_connection.commit()
    print('Successfully added a new patient')


@cli.command(help_priority=2)
@click.option('--phone', 'phone', required=True, type=click.STRING, prompt=True)
@click.option('--column', 'column', required=True, type=click.STRING, prompt=True)
@click.option('--value', 'value', required=True, prompt=True)
@click.option('--quote', is_flag=True)
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
    inner_connection=connector.connect(**connectionDict)

    if quote:
        value='"'+value+'"'

    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif not exists(value=phone, column='phone', table='patients', connection=inner_connection):
        raise ValueError('A patient with that phone number does not exists.')

    allowed_update_patient_columns=('name', 'phone', 'dob', 'gender', 'address')

    if not isinstance(column, str):
        raise TypeError('arguement `phone` must be a string')
    elif column not in allowed_update_patient_columns:
        raise ValueError(f"`column` must be any of {allowed_update_patient_columns}")
    
    inner_cursor=inner_connection.cursor()
    inner_cursor.execute(f'''\
UPDATE patients
SET {column}={value}
WHERE phone="{phone}";''')
    inner_connection.commit()
    print('Updated successfully')


@cli.command(help_priority=3)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def show_appointments(password):
    """Print the table `appointments`"""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    inner_connection=connector.connect(**connectionDict)

    inner_cursor=inner_connection.cursor()
    inner_cursor.execute('''\
SELECT patients.name, patients.phone, appointments.treatmentID, appointments.date, appointments.time
FROM patients, appointments
WHERE patients.phone=appointments.phone;''')
    appointments=from_db_cursor(inner_cursor)

    fieldname='Sno'
    appointments.field_names.insert(0, fieldname)
    appointments.align[fieldname]='c'
    appointments.valign[fieldname]='t'
    for i, _ in enumerate(appointments.rows):
        appointments.rows[i].insert(0, i+1)
    
    print(appointments)


@cli.command(help_priority=4)
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
    inner_connection=connector.connect(**connectionDict)

    if not isinstance(phone, str):
        raise TypeError('arguement `phone` must be a string')
    elif (len(phone)>17 and (not phone.replace('+', '').replace('-', '').isdigit())):
        raise ValueError('It is not a proper phone number')
    elif not exists(value=phone, column='phone', table='patients', connection=inner_connection):
        raise ValueError('A patient with that phone does not exists')

    if not (date[0:4].isdigit() and 
                            date[4]=='-' and 
                            date[5:7].isdigit() and 
                            date[7]=='-' and
                            date[8:10].isdigit()
                            and len(date)==10 ):
        raise ValueError('improper `date` format')

    if not (time[0:2].isdigit() and
                        time[2]==':' and
                        time[3:5] and
                        len(time)==5):
        raise ValueError('improper `time` format')
    
    treatmentID=randomstring(8)
    while exists(value=treatmentID, column='treatmentID', table='appointments', connection=inner_connection):
        treatmentID=randomstring(8)
    
    inner_cursor=inner_connection.cursor()
    inner_cursor.execute(f'''\
INSERT INTO Appointments (phone, treatmentID, date, time)
VALUES ("{phone}", "{treatmentID}", '{date}', '{time}');''')
    inner_connection.commit()
    print('Added successfully')


@cli.command(help_priority=5)
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.option('--column', 'column', required=True, type=click.STRING, prompt=True)
@click.option('--value', 'value', required=True, prompt=True)
@click.option('--quote', is_flag=True)
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
    inner_connection=connector.connect(**connectionDict)

    if quote:
        value='"'+value+'"'

    if not isinstance(treatmentID, str):
        raise TypeError('arguement `phone` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='appointments', connection=inner_connection):
        raise ValueError('An appointment with that phone number does not exists.')

    allowed_update_appointment_columns=('date','time')

    if not isinstance(column, str):
        raise TypeError('arguement `phone` must be a string')
    elif column not in allowed_update_appointment_columns:
        raise ValueError(f"`column` must be any of {allowed_update_appointment_columns}")

    inner_cursor=inner_connection.cursor()
    inner_cursor.execute(f'''\
UPDATE appointments
SET {column}={value}
WHERE treatmentID="{treatmentID}";''')
    inner_connection.commit()
    print('Updated successfully')


@cli.command(help_priority=6)
@click.option('--treatmentID', 'treatmentID', required=True, type=click.STRING, prompt=True)
@click.password_option('-p', '--password', required=True, type=click.STRING, confirmation_prompt=False)
def remove_appointment(treatmentID, password):
    """Removes an appointment record if only there is no treatment related to it."""
    connectionDict=sqlconfig.load.load_data(1)
    connectionDict['password']=password
    inner_connection=connector.connect(**connectionDict)

    if not isinstance(treatmentID, str):
        raise ValueError('`treatmentID` must be a string')
    elif not exists(value=treatmentID, column='treatmentID', table='appointments', connection=inner_connection):
        raise ValueError('given `treatmentID` does not exist in appointments')
    elif exists(value='treatments', column='treatmentID', table='treatments', connection=inner_connection):
        raise ValueError('a treatment exists with the given `treatmentID`')

    inner_cursor=inner_connection.cursor()
    inner_cursor.execute(f'''\
DELETE FROM appointments
WHERE treatmentID="{treatmentID}";''')
    inner_connection.commit()
    print("Deleted successfully")







if __name__=='__main__':
    cli()
