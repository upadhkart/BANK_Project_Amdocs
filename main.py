# main file
import random
import time
import sqlite3 
import datetime
# database creation
# print("creating database")
conn=sqlite3.connect('bank_database.db')  
curs=conn.cursor()
# print("database created")

def createaccount():
    # USER table creation
    # print("creating table user")
    curs.execute('CREATE TABLE IF NOT EXISTS USER(id char(8) NOT NULL PRIMARY KEY,Name char(20),Address TEXT,Contact INTEGER(10),password varchar(8),Account_number INTEGER(10),balance INTEGER)')  
    # print("table created")
    Name = str(input("enter your name "))
    Address = str(input("enter your address "))
    Contact =int(input("enter your phone number "))
    id=str(input("enter id of your choice "))
    password=str(input("create your password "))
    Account_number = random.randint(0000000000,9999999999)
    balance=2000
    # print("inserting value into table")
    curs.execute('INSERT INTO USER (id,Name,Address,Contact,password,Account_number,balance) VALUES (?,?,?,?,?,?,?);', (id,Name,Address,Contact,password,Account_number,balance))
    # print("value inserted in table")
    conn.commit()
    #TRANSACTION TABLE CREATION
    # print("creating transaction table")
    curs.execute('CREATE TABLE IF NOT EXISTS TRANS(trans_id INTEGER(12) NOT NULL PRIMARY KEY,trans_date DATE DEFAULT CURRENT_DATE,trans_time TIME DEFAULT CURRENT_TIME,id char(8) NOT NULL,debit INTEGER,credit INTEGER,Account_number INTEGER(10),balance INTEGER,FOREIGN KEY(id) REFERENCES USER(id))')
    trans_id = random.randint(0000000000,9999999999)
    curs.execute('INSERT INTO TRANS(trans_id,id,debit,credit,Account_number,balance) VALUES (?,?,0,?,?,?)',(trans_id,id,2000,Account_number,2000))
    conn.commit()
    # print("transaction table created")  
    print("Account Successfully Created")  
    time.sleep(3)

def Statment(user_id):
    curs.execute('SELECT Name,Account_Number FROM USER WHERE id = ?',(user_id,))
    user_data=curs.fetchone()
    if user_data:
        name,account_number = user_data
        with open("sheet.txt","w") as f:
            f.write(("=============================XYZ BANK============================\n"))
            f.write(f"AC Name: {name}     AC No: {account_number} \n")
            f.write(("=================================================================\n"))

    curs.execute('SELECT trans_id,trans_date,trans_time,debit,credit,balance FROM TRANS WHERE id = ? ORDER BY trans_date,trans_time DESC LIMIT 4',(user_id,))
    user_trans=curs.fetchall()
    if user_trans:
        with open("sheet.txt","a") as g:
            g.write(f"TRANSACTION ID\t\tDATE\t\tTIME\t\tDEBIT\t\tCREDIT\t\tBALANCE \n")
            for trans_id,trans_date,trans_time,debit,credit,balance in user_trans:
                g.write(f"{trans_id}\t\t{trans_date}\t\t{trans_time}\t\t{debit}\t\t{credit}\t\t{balance}\n")
            g.write(("=================================================================\n"))   

def profile(user_id):
    print("--------------XYZ BANK---------------")
    curs.execute('SELECT Name,Address,Contact,Account_Number FROM USER WHERE id = ?',(user_id,))
    user_data=curs.fetchone()
    if user_data:
        name, address, contact, account_number = user_data
        print("Name:",name)
        print("Address:",address)
        print("Contact:",contact)
        print("Account_Number:",account_number)
        print("ID:",user_id)
    else:
        print("user not found") 
    print("--------------------------------------")

def exit():
    while(True):
        ex=str(input("enter e or E to exit "))
        if(ex=="e" or ex=="E"):
            break
        else:
            print("entered wrong choice")

def login():
    Login_id = str(input("Enter Your ID "))
    Pass = str(input("Enter Your Password "))
    curs.execute('SELECT id,password,Account_number FROM USER WHERE id = ? AND password = ?',(Login_id,Pass))
    user_data=curs.fetchone()
    if(user_data):
        print("Logged IN")
        user_id=user_data[0]
        Account_number=user_data[2]
        #Account_number = curs.execute('SELECT Account_number FROM USER WHERE id = ?', (user_id,)).fetchone()[0]
        try:
            while (True):
                y=int(input("Enter Choice \n1.Balance \n2.Bank Statment \n3.Debit \n4.Profile \n5.Credit \n6.Money Transfer \n7.Exit \n"))
                if y==1:
                    curs.execute('SELECT balance FROM USER WHERE id = ?',(user_id,))
                    current_balance=curs.fetchone()[0]
                    print("Your Account Balance is: ",current_balance)
                    conn.commit()
                    time.sleep(3)
                elif y==2:
                    print("Your Bank Statment")
                    Statment(user_id)
                    with open('sheet.txt','r') as File:
                        print(File.read())
                    exit()    
                elif y==3:
                    debit_amt=int(input("enter amount to be debited: "))
                    curs.execute('SELECT balance FROM USER WHERE id = ?',(user_id,))
                    current_balance=curs.fetchone()[0]
                    if(debit_amt > current_balance):
                        print("Insufficient Balance")
                    else:
                        new_balance_debit=current_balance-debit_amt
                        trans_id = random.randint(0000000000,9999999999)
                        trans_date = datetime.datetime.now().strftime('%Y-%m-%d')
                        trans_time = datetime.datetime.now().strftime('%H:%M:%S')
                        curs.execute('INSERT INTO TRANS(trans_id,trans_date,trans_time,id,debit,credit,Account_number,balance) VALUES (?,?,?,?,?,0,?,?)', (trans_id,trans_date,trans_time,user_id,debit_amt,Account_number,new_balance_debit))
                        curs.execute('UPDATE USER SET balance = ? WHERE id = ?',(new_balance_debit,user_id))
                        conn.commit()
                    print("Successfull Transaction")    
                    time.sleep(3)
                elif y==4:
                    print("Your Profile")
                    profile(user_id)
                    exit()
                elif y==5:
                    credit_amt=int(input("enter amount to be credited: "))
                    curs.execute('SELECT balance FROM USER WHERE id = ?',(user_id,))
                    current_balance=curs.fetchone()[0]
                    new_balance_credit=current_balance+credit_amt
                    trans_id = random.randint(0000000000,9999999999)
                    trans_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    trans_time = datetime.datetime.now().strftime('%H:%M:%S')
                    curs.execute('INSERT INTO TRANS (trans_id,trans_date,trans_time,id, debit, credit, Account_number, balance) VALUES (?, ?,?, ?, 0, ?, ?, ?)', (trans_id,trans_date ,trans_time,user_id, credit_amt, Account_number, new_balance_credit))
                    curs.execute('UPDATE USER SET balance = ? WHERE id = ?', (new_balance_credit, user_id))
                    conn.commit()
                    print("Amount credited in your account")
                    time.sleep(3)
                elif y==6:
                    print("Money Transfer")
                    acco_no=int(input("Enter account number to Transfer Money "))
                    curs.execute('SELECT Account_number FROM USER WHERE Account_number = ?',(acco_no,))
                    data_retrived=curs.fetchone()
                    if data_retrived:
                        acco_no_1=data_retrived[0]    
                        if(acco_no == acco_no_1):
                            amount=int(input("enter amount to credit in user "))
                            # balance of user who has to transfer
                            curs.execute('SELECT balance FROM USER WHERE id = ?',(user_id,))
                            current_balance_login=curs.fetchone()[0]
                            if(amount<=current_balance_login):
                                new_current_balance_login=current_balance_login-amount
                                trans_id = random.randint(0000000000,9999999999)
                                trans_date = datetime.datetime.now().strftime('%Y-%m-%d')
                                trans_time = datetime.datetime.now().strftime('%H:%M:%S')
                                curs.execute('INSERT INTO TRANS (trans_id,trans_date,trans_time, id, debit, credit, Account_number, balance) VALUES (?,?,?,?, ?, 0, ?, ?)', (trans_id,trans_date,trans_time, user_id,amount, Account_number, new_current_balance_login))
                                curs.execute('UPDATE USER SET balance = ? WHERE id = ?', (new_current_balance_login, user_id))
                                conn.commit()
                                # account number of user where money has to be transfered
                                curs.execute('SELECT balance,id FROM USER WHERE Account_number = ?',(acco_no,))
                                receiver_data = curs.fetchone()
                                if receiver_data:
                                    # balance of the account holder where money has to be transfered
                                    current_balance_trans,id_user_trans = receiver_data 
                                    new_current_balance_trans=current_balance_trans + amount
                                    trans_id = random.randint(0000000000,9999999999)
                                    trans_date = datetime.datetime.now().strftime('%Y-%m-%d')
                                    trans_time = datetime.datetime.now().strftime('%H:%M:%S')
                                    curs.execute('INSERT INTO TRANS (trans_id,trans_date,trans_time, id, debit, credit, Account_number, balance) VALUES (?, ?,?, ?, 0, ?, ?, ?)', (trans_id,trans_date,trans_time,id_user_trans,amount, Account_number,new_current_balance_trans))
                                    curs.execute('UPDATE USER SET balance = ? WHERE Account_number = ?', (new_current_balance_trans, acco_no))
                                    conn.commit()
                                    print("Money successfully transfered")
                            else:
                                print("Insufficient balance") 
                    else:
                        print("Wrong account number")             
                elif y==7:
                    break
        except Exception as e:
            print("An error occurred please try again") 
        else:
            print("User not exists")                     
try:               
    while (True):
        x=int(input("Enter Choice \n1.Create Account \n2.Login \n3.Exit\n"))
        if x==1:
            print("Welcome to XYZ Bank please Create Your Account")
            createaccount()
        elif x==2:
            login()
        elif x==3:
            print("Thank you for using XYZ bank")
            break
except Exception as e:
    print("An error occurred please try again")       
        