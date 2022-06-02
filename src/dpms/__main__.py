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

@click.group()
def cli():
    pass

@click.command()
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







cli.add_command(show_patients)

if __name__=='__main__':
    # cli(['--help'], prog_name='dpms')
    cli()
