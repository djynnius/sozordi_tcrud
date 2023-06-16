from getpass import getpass
from bcrypt import hashpw, gensalt, checkpw

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
            print("Sorry your account could not be verified.\n Goodbye.")
            break
    
    if logged_in:
        action = input("What do you want to do?: ")
        if(action.strip().lower() in ['x', 'exit']):    
            print("Goodbye.\n")
            break

    i = i + 1
    ...