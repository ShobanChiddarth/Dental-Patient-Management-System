<h1 align="center">
DENTAL PATIENT MANAGEMENT SYSTEM

<img src="Assets/Teeth-logo.png" width="300">
</h1>


Just a school project, running in Python Interpreter. It is purely written in python. 
This is not a GUI or CLI application. It is just run in Python Interpreter directly 
and the output is everything. This is a school project to use python with [class 12 concepts](https://csstudy.in/sumita-arora-python-class-12-pdf-cs-book/). 
My aim was not to use the concepts but to make it a good software and anyways I 
ended up using all the concepts taught in school for this project.

This is a project made in python, it can keep a record of patients who visit a Dental
clinic, keep a record of their appointments and treatments. It will take care of everything related to keeping record of
- patients
- treatments
- appointments

When I say it is just a school project, I mean it can't be used in real life, as
a real software to manage patient records in a clinic. It is very very very limited
and has very less features. If you are looking for an open-source Dental management
system, this is not the one you are looking for.

This is an educational material for students who wan't to make their school project.
Students can refer this for their projects and etc. This is solely for educational
purpose and not anything commercial, and also won't be a commercial product in the 
future. It is always a free and open source project.

### PRE REQUISITES
1. [Python >= 3.6](https://realpython.com/installing-python/)
2. [MySQL](https://www.mysql.com/)
3. Virtual Environment in Python (Optional)

### SETUP
1. [Clone](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/)/[download zip](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github/) this repo
1. [Create a Virtual Environment and activate it](https://thepythonguru.com/python-virtualenv-guide/)
1. Install required modules (available in [requirments.txt](/requirements.txt))
   ```cmd
   pip install -r "requirements.txt"
   ```
   Virtual Environment is optional
1. Restore the backed up MySQL database in [backup.sql](/SQL-credentials/backup.sql)
   ```cmd
   mysql -u root -p SrisakthiPatients < SQL-credentials/backup.sql
   ```
1. Success. Now you can run [main.py](/src/main.py).

#### LINKS
Links will be updated later
- [Documentation]()
- [Dev Docs]()
- [Bugs and Features + Discussions](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/issues)
- [Contributing](.github/CONTRIBUTING.md)

