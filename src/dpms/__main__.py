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
