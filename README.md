<h1 align="center">
DENTAL PATIENT MANAGEMENT SYSTEM<br>
<img src="Assets/Teeth-logo.png" width="300">
</h1>

### Introduction
Just a school project, running in Python. It is purely written in python. 
It is just run in Python directly and the output in the terminal is everything.
This is a school project to use python with [class 12 concepts](https://csstudy.in/sumita-arora-python-class-12-pdf-cs-book/).
This is currently a script that uses a CLI interface as an API. It gets user
input and runs the CLI, gives the output in the main script. 
My aim was not to use the concepts but to make it a good software and anyways I 
ended up using all the concepts taught in school for this project.

When I say it is just a school project, I mean it can't be used in real life, as
a real software to manage patient records in a  real dental clinic. It is very very
very limited and has very less features. If you are looking for an open-source Dental
management system, this is not the one you are looking for.

### Whom this is for
This is an educational material for students who wan't to make their school project.
Students can refer this for their projects and etc. This is solely for educational
purpose and not anything commercial, and also won't be a commercial product in the 
future. It is always a free and open source project.

### PRE REQUISITES
1. [Python (3.10.2 is preferable)](https://realpython.com/installing-python/)
2. [A MySQL Server](https://www.mysql.com/)
3. Virtual Environment in Python (Optional)

### SETUP
1. [Clone](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/)/[download zip](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github/) this repo (you can also download the source code from the [latest release](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/releases/latest))
1. [Create a Virtual Environment and activate it](https://thepythonguru.com/python-virtualenv-guide/) (Optional)
1. Install required modules (available in [requirments.txt](/requirements.txt))
   ```cmd
   pip install -r "requirements.txt"
   ```
   Virtual Environment is optional
1. Restore the backed up MySQL database in [backup.sql](backup.sql)
   ```cmd
   mysql -u root -p SrisakthiPatients < backup.sql
   ```
1. Success. Now you can run [main.py](/src/main.py).

### LINKS
- [Documentation](./docs/)
- [Developer Documentation](./docs/devdocs)
- [Bugs and Features](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/issues)
- [Discussions](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/discussions)
- [Contributing](.github/CONTRIBUTING.md)

### DISCLAIMER
1. All the patient names, phone numbers, addresses, etc. shown anywhere
in comments, issues, pull requests, etc. are imaginary and resemblance
to any person living or dead is **purely co-incidental**.
1. The clinic's name "Sri Sakthi Dental Clinic" is used as a **Sample** for
a clinic name in places where it is needed. The database backup file
[backup.sql](https://github.com/ShobanChiddarth/Dental-Patient-Management-System/blob/d985c7a09cd2a052a3d47ce70db3bea31c2e79fd/backup.sql#L22) <!-- Permalink is used in case the database is updated in the future, the line where the `CREATE DATABASE` statement would be present may not be the same -->
has the database name stored as `SrisakthiPatients` and the program also
mentions the clinic's name during run. These are all purely demonstration
purposes and this is not a commercial product owned by Sri Sakthi Dental Clinic.
