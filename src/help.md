COMMANDS
========

GENERAL
-------
- help: show this message
- exit: exit the script
- quit: alias of exit

DEBUG
-----
- enter-python-eval : whatever you type in python, will be evaluated and printed
- enter-python-exec : whatever you type in python, will be executed
- enter-sql-mode : whatever you type in python, is sent to mysql as mysql commands
                   But output won't be printed. It is only for managing data.

PATIENTS
--------
- show patients: print the table `patients` in database `SrisakthiPatients`
- add patient: create a new patient
               in database `SrisakthiPatients`, table `patients`
- update patient: update a patient in table `patients` in database `SrisakthiPatients`
                  You must provide `patientID`
NOTE: You can't delete patients

APPOINTMENTS
------------
- show appointments: print the table `Appointments` in database `SrisakthiPatients`
- add appointment: add a new appointment in table `Appointments` in database `
- update appointment: update an existing appointment in table `Appointments` in database `SrisakthiPatients`
                    You must provide `treatmentID`
- remove appointment: remove an appointment in table `Appointments` in database `SrisakthiPatients`
                      You must provide `treatmentID`
NOTE: You can remove appointments only if the treatment didn't take place

TREATMENTS
----------
- show treatments: print the table `treatments` in database `SrisakthiPatients`
- add treatment-exact: add new treatment in table `treatments` in database `SrisakthiPatients`
                       with the exact date and time in table `Appointments`
                       You must provide `treatmentID`
- add treatment: add new treatment in table `treatments` in database `SrisakthiPatients`
                 You must provide `treatmentID`
- update treatment: update treatment in in table `treatments` in database `SrisakthiPatients`
                    You must provide `treatmentID`
NOTE: You can't remove treatments

END OF HELP

---