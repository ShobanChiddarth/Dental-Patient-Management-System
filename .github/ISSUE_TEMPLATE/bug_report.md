---
name: Bug report
about: Create a report to help us improve
title: BUG
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior (the entire text (your command, output, error message, etc.) like this one):
```
SRI SAKTHI DENTAL CLINIC
DENTAL PATIENT MANAGEMENT SYSTEM

Using current SQL connection configuration
{
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "1234",
    "database": "SrisakthiPatients",
    "buffered": true
}
Please look at this dictionary to get an idea about sql connection config dict.
Your dictionary must look somewhat like this.
{
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "1234",
    "database": "SrisakthiPatients",
    "buffered": true
}
But it looks like
{
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "1234",
    "database": "SrisakthiPatients",
    "buffered": true
}
Do you wish to proceed with the following (please make changes according to your need) [Y/n]?Y
Connected to MySQL Database SriSakthiPatients
Welcome admin
Type `help` for help

Enter command> add treatment-exact
Enter treatmentID to add treatment in exact date, time of appointment
(or even `show appointments`) : Traceback (most recent call last):
  File "Dental-Patient-Management-System\src\main.py", line 728, in <module>
    add_treatment_exact()
  File "Dental-Patient-Management-System\src\main.py", line 430, in add_treatment_exact
    treatmentID=input('(or even `show appointments`) : ')
KeyboardInterrupt

```
(this was an intentional KeyboardInterrupt, only for demonstration purposes. You have to replace that
blob of text with the output you got)

**Expected behavior**
A clear and concise description of what you expected to happen.


**Desktop (please complete the following information):**
 - OS: [e.g. Windows 10]
 - Python Version: [e.g. 3.8, 3.10.1]
 - Software Version [e.g. 0.1, 0.2]

**Additional context**
Add any other context about the problem here.
