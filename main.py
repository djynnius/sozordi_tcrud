from platform import system
from getpass import getpass
from bcrypt import hashpw, gensalt, checkpw

#imports for our model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from packages import schema
from prettytable import PrettyTable
from pathlib import Path



class SOSIMS():
    def __init__(self, sess):
        self.sess = sess
        #variables for managing app
        self.i = 1
        self.logged_in = False
        self.action = None

    def print_banner(self):
        print('''
         ____   ___  ____ ___ __  __ ____  
        / ___| / _ \/ ___|_ _|  \/  / ___| 
        \___ \| | | \___ \| || |\/| \___ \ 
         ___) | |_| |___) | || |  | |___) |
        |____/ \___/|____/___|_|  |_|____/ 
        ''')

    
    #Student Methods
    def view_students(self):
        students = self.sess.query(schema.Student).all()
        st = PrettyTable()
        st.field_names = ['Reg Number', 'Firstname', 'Surname', 'Age', 'Sex']
        for student in students:
            st.add_row([student.reg_num, student.firstname, student.lastname, student.age, student.sex])
        print(st)

    
    def create_student(self):
        firstname = input("Firstname: ")
        lastname = input("Surname: ")
        age = int(input("Age: "))
        sex = input("Sex: ")
        reg_num = input("Reg Num: ")

        newstudent = schema.Student(firstname=firstname, lastname=lastname, sex=sex, age=age, reg_num=reg_num)
        self.sess.add(newstudent)
        self.sess.commit()

        print(f"{firstname} {lastname} with registeration number {reg_num} was successfully added")


    def update_student(self):
        reg_num = input("Enter students registeration number: ")
        student = self.sess.query(schema.Student).filter_by(reg_num = reg_num).one()
            
        firstname = input(f"Firstname [{student.firstname}]: ")
        lastname = input(f"Surname [{student.lastname}]: ")
        try:
            age = int(input(f"Age [{student.age}]: "))
        except:
            age = student.age
        sex = input(f"Sex [{student.sex}]: ")
        reg_num = input(f"Reg Num [{student.reg_num}]: ")

        student.firstname = student.firstname if firstname == '' else firstname
        student.lastname = student.lastname if lastname == '' else lastname
        try:
            student.age = student.age if age == '' else int(age)
        except:
            student.age = student.age
            
        student.sex = student.sex if sex == '' else sex
        student.reg_num = student.reg_num if reg_num == '' else reg_num

        self.sess.commit()
    
    def delete_student(self):
        reg_num = input("What is the Registeration Number of the student you want to delete?: ")
        student = self.sess.query(schema.Student).filter_by(reg_num = reg_num).one()
        summary = f"{student.firstname} {student.lastname} ({student.reg_num})"
        print(f"You are about to delete {student.firstname} {student.lastname} with registeration number {student.reg_num}.")
        proceed = input("Do you want to proceed? [Y/N]: ")        

        return dict(student=student, proceed=proceed.strip().lower(), summary=summary)

    #Help 
    def help(self):
        print('''
s or students to view students
cs to create a new student
us to update a student record
ds to delete a student record
t, l, teachers or lecturers to view lecturers
c or courses to view subjects            
h or help: see this menu
x or exit: exits app
''')



db_file = Path("./school.db")
if db_file.is_file():
    ...
else:
    print("Plese setup the database by running the schema file from the packages folder.")
    exit()

engine = create_engine("sqlite:///school.db")
sess = sessionmaker(engine)()

#Instantiate the SOSIMS app
sosims = SOSIMS(sess)

#Application loop
while True:
    if sosims.i == 1: 
        sosims.print_banner()
        user = input("Please enter your username: ").strip().lower()
        pswd = hashpw(getpass("Please enter your password: ").strip().encode(), gensalt())

        if checkpw('education'.encode(), pswd):
            sosims.logged_in = True
        else:
            print("Sorry your account could not be verified.\nGoodbye.")
            break
    
    if sosims.logged_in:
        sosims.action = input("What do you want to do?: ")
        
        #Take some action
        axn = sosims.action.strip().lower()
        if(axn in ['x', 'exit']):    
            print("Goodbye.\n")
            break
        elif axn == 'cs':
            #create student
            sosims.create_student()
        elif axn == 'us': 
            #update student
            sosims.update_student()        
        elif axn in ['ds']: 
            #delete student
            action = sosims.delete_student()
            if action['proceed'] == 'y':
                sess.delete(action['student'])
                sess.commit() 
                print(f"You have deleted {action['summary']}")
            else:
                continue

        elif axn in ['s', 'students']:
            #view students
            sosims.view_students()
        elif axn in ['t', 'l', 'teachers', 'lecturers']:
            #view teachers
            ...
        elif axn in['c', 'courses']:
            #view courses
            ...
        elif axn in ['h', 'help']:
            sosims.help()

    #increment internal counter        
    sosims.i = sosims.i + 1

#if 'win' in  system.lower(): input("Hit enter to close the teminal.")
