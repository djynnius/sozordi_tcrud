from platform import system
from getpass import getpass
from bcrypt import hashpw, gensalt, checkpw

#imports for our model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from packages import schema
from prettytable import PrettyTable

engine = create_engine("sqlite:///school.db")
sess = sessionmaker(engine)()

#variables for managing app
i = 1
logged_in = False
action = None

#Application loop
while True:
    if i == 1: 
        print('''
         ____   ___  ____ ___ __  __ ____  
        / ___| / _ \/ ___|_ _|  \/  / ___| 
        \___ \| | | \___ \| || |\/| \___ \ 
         ___) | |_| |___) | || |  | |___) |
        |____/ \___/|____/___|_|  |_|____/ 
        ''')
        user = input("Please enter your username: ").strip().lower()
        pswd = hashpw(getpass("Please enter your password: ").strip().encode(), gensalt())

        if checkpw('education'.encode(), pswd):
            logged_in = True
        else:
            print("Sorry your account could not be verified.\nGoodbye.")
            break
    
    if logged_in:
        action = input("What do you want to do?: ")
        
        #Take some action
        axn = action.strip().lower()
        if(axn in ['x', 'exit']):    
            print("Goodbye.\n")
            break
        elif axn == 'cs': #create student
            firstname = input("Firstname: ")
            lastname = input("Surname: ")
            age = int(input("Age: "))
            sex = input("Sex: ")
            reg_num = input("Reg Num: ")

            newstudent = schema.Student(firstname=firstname, lastname=lastname, sex=sex, age=age, reg_num=reg_num)
            sess.add(newstudent)
            sess.commit()

            print(f"{firstname} {lastname} with registeration number {reg_num} was successfully added")

        elif axn in ['s', 'students']:
            #view students
            students = sess.query(schema.Student).all()
            st = PrettyTable()
            st.field_names = ['Reg Number', 'Firstname', 'Surname', 'Age', 'Sex']
            for student in students:
                st.add_row([student.reg_num, student.firstname, student.lastname, student.age, student.sex])
            print(st)
        elif axn in ['t', 'l', 'teachers', 'lecturers']:
            #view teachers
            ...
        elif axn in['c', 'courses']:
            #view courses
            ...
        elif axn in ['h', 'help']:
            print('''
s or students to view students
t, l, teachers or lecturers to view lecturers
c or courses to view subjects            
h or help: see this menu
x or exit: exits app
''')

    i = i + 1

#if 'win' in  system.lower(): input("Hit enter to close the teminal.")