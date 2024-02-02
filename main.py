from tkinter import *
import mysql.connector
import random
from datetime import datetime
import re

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password123',
)
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS bank")

cursor.execute("USE bank")

cursor.execute("""CREATE TABLE IF NOT EXISTS transactions(
    sender_id VARCHAR(100),
    receiver_id VARCHAR(100),
    amount FLOAT,
    date DATE
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bank(
    first_name VARCHAR (100),
    last_name VARCHAR (100),
    dob DATE,
    e_mail VARCHAR(100) NOT NULL,
    postcode VARCHAR (7),
    password VARCHAR (24),
    balance FLOAT DEFAULT 0.0,
    accountID VARCHAR(8),
    PRIMARY KEY (e_mail, accountID)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS requests(
    target_id VARCHAR(8),
    requester_id VARCHAR(8),
    amount FLOAT (20,2)
    )""")
mydb.commit()
################################################
font_default = ('Helvetica', 10, 'bold')
font_big = ('Helvetica', 20, 'bold')
alert_row = 15
entries = {}

labels_main = [
    'E-mail',
    'Password'
]

labels_sign_up = [
    'First Name',
    'Last Name',
    'Date of Birth',
    'E-mail',
    'Confirm E-mail',
    'Post Code',
    'Password',
    'Confirm Password'
]

labels_transfer_menu = [
    'Target ID',
    'Amount'
]

labels_request_menu = [
    'Request From',
    'Amount'
]

labels_admin_panel = [
    'Target ID',
    'Target E-mail'
]

labels_user_details = [
    'First Name',
    'Last Name',
    'Date of Birth',
    'E-mail',
    'Post Code',
    'Password',
    'Balance',
    'AccountID'
]

labels_change_user = [
    'First Name',
    'Last Name',
    'Date of Birth',
    'E-mail',
    'Post Code',
    'Password',
    'Balance',
    'AccountID'
]


################################################
def main_page(destroy_, window):
    global root
    if destroy_ == True:
        purge(window)    
    else:
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.title("Sign in to Bank")
        root.geometry(('400x400'))
    
    create_labels_and_entries(root, labels_main)
    
    label = Label(root, text="Sign in to Kaya Bank", font=font_big)
    label.grid(row=0, column=0, columnspan=2)
    
    frame = Frame(root)
    frame.grid(row=2, column=0, columnspan=2, padx=90)
    button = Button(frame, text="Sign In", command=sign_in, font=font_default)
    button.grid(row=0, column=0, sticky=W, pady=(5,0))
    
    button = Button(frame, text="Sign Up", command=sign_up_page, font=font_default)
    button.grid(row=0, column=1, sticky=W, pady=(5,0))
##
def sign_in():
    e_mail = entries['E-mail'].get()
    password = entries['Password'].get()
    
    sql_command = f"SELECT password FROM bank WHERE e_mail = + '{e_mail}'"
    cursor.execute(sql_command)
    result = cursor.fetchone()

    if result:
        if result[0] == password:
            if e_mail == None: ##change to admin
                admin_panel()
            else:
                balance_window(e_mail)
        elif result[0] != password:
            alert(root, 'Incorrect Password', alert_row ,0, 'red', 1)
            entries_delete(['Password'])
    else:
        alert(root, 'Incorrect E-mail', alert_row ,0, 'red', 1)
        entries_delete(['E-mail', 'Password'])
##
def balance_window(pk) :
    purge(root)
    
    details = get_details('e_mail', pk)

    label = Label(root, text=f"Welcome {details[0]}, \n £{str(details[6])}", font=font_big)
    label.grid(row=0, column=0)
    
    label = Label(root, text=details[-1], font=font_default)
    label.grid(row=1, column=0)
    
    button = Button(root, text='Transfer Money', command=lambda: transfer_menu(root, details[-2], pk), font=font_default)
    button.grid(row=2, column=0)
    
    button = Button(root, text="Request Money", command=lambda: request_menu(root, details, pk), font=font_default)
    button.grid(row=3, column=0)
    
    button = Button(root, text="Sign Off", command=lambda: main_page(True, root), font=font_default)
    button.grid(row=4, column=0)
    
    frame = LabelFrame(root, borderwidth=1, text="Requests")
    frame.grid(row=6, column=0, columnspan=3)
    frame.columnconfigure(0, weight=0)
    label = Label(frame, text='Requester', font=font_default)
    label.grid(row=0, column=0)
    label = Label(frame, text='Amount', font=font_default)
    label.grid(row=0, column=1)
    
    label = Label(frame, text='Accept/Reject', font=font_default)
    label.grid(row=0, column=2)
    
    show_requests(frame, details, pk, myrequests=False)
    
def transfer_menu(window, balance, pk):
    purge(window)
    window.columnconfigure(0, weight=1)

    label = Label(window, text=f"Your balance: £{balance}", font=font_big)
    label.grid(row=0, column=0)
    
    create_labels_and_entries(window, labels_transfer_menu)
    
    frame = Frame(window, borderwidth=0, highlightthickness=0)
    frame.grid(row=2, column=0)
    
    button = Button(frame, command=lambda: transfer_check(window, balance, pk), text="Transfer Money", font=font_default)
    button.grid(row=0, column=0, padx=10)
    
    button = Button(frame, command=lambda: balance_window(pk) , text="Go Back", font=font_default)
    button.grid(row=1, column=0, padx=10)
##
def transfer_check(window, balance, pk):
    target_id = entries['Target ID'].get()
    amount = entries['Amount'].get()
    
    if target_id and amount:
        try:
            amount = float(amount)
        except ValueError:
            alert(window, 'Amount must be integer', alert_row, 0, 'red', 1)
    else:
        alert(window, 'Invalid target id or amount.', alert_row, 0, 'red', 1)
    details_target = get_details('accountID', target_id)
    details = get_details('e_mail', pk)
    
    if target_id and amount:
        if details_target != None:
            if balance > amount:
                def handle_verification(result):
                    verify(root, details, details_target, amount, handle_verification, 'transfer')
                    if result == True:
                        transfer(details_target, details, amount)
                        balance_window(pk) 
                    elif result == False:
                        balance_window(pk) 
                        alert(root, 'Verification failed.', alert_row, 0, 'red', 1)
                verify(root, details, details_target, amount, handle_verification, 'transfer')   
            else:
                alert(window, 'Balance is too low.', alert_row, 0, 'red', 1)
                entries_delete(['Amount'])
        else:
            entries_delete(['Amount', 'Target ID'])
            alert(window, 'Incorrect Target ID', alert_row, 0, 'red', 1)
    else:
        alert(window, 'Incorrect Target ID or Amount.', alert_row, 0, 'red', 1)

def transfer(accountID, targetID, amount):
    details_target = get_details('accountID', targetID)
    details = get_details('accountID', accountID)

    balance_sender = details[6]
    balance_receiver = details_target[6]
    sender_id = details[7]
    receiver_id = details_target[7]

    sql_command = f"UPDATE bank SET balance = {balance_sender - amount} WHERE accountID = '{sender_id}'"
    cursor.execute(sql_command)
    sql_command = f"UPDATE bank SET balance = {balance_receiver + amount} WHERE accountID = '{receiver_id}'"
    cursor.execute(sql_command)
    
    store_transfer(sender_id, receiver_id, amount)
    
    mydb.commit()
  
def store_transfer(sender_id, receiver_id, amount):
    date = datetime.now().date()
    
    sql_command = f"INSERT INTO transactions (sender_id, receiver_id, amount, date) VALUES (%s, %s, %s, %s)"
    values = (sender_id, receiver_id, amount, date) 
    
    cursor.execute(sql_command, values)
    
    
def request_menu(window, details, pk):
    purge(window)
    
    label = Label(window, text=f"Your balance: £{details[6]}", font=font_big)
    label.grid(row=0, column=0)
    
    create_labels_and_entries(window, labels_request_menu)
    
    frame = Frame(window, borderwidth=0, highlightthickness=0)
    frame.grid(row=2, column=0)
    
    button = Button(frame, command=lambda: request(window, details, pk), text="Request Money", font=font_default)
    button.grid(row=0, column=0, padx=10)
    
    button = Button(frame, command=lambda: balance_window(pk) , text="Go Back", font=font_default)
    button.grid(row=1, column=0, padx=10)
    
    frame = LabelFrame(root, borderwidth=1, text="My Requests")
    frame.grid(row=6, column=0, columnspan=3)
    frame.columnconfigure(0, weight=0)
    label = Label(frame, text='Requested From', font=font_default)
    label.grid(row=0, column=0)
    label = Label(frame, text='Amount', font=font_default)
    label.grid(row=0, column=1)
    
    show_requests(frame, details, pk, myrequests=True)

def show_requests(window, details, pk, myrequests):
    if myrequests == True:
        sql_command = "SELECT * FROM requests WHERE requester_id = %s"
        values = [details[7]]
        cursor.execute(sql_command, values)
        requests = cursor.fetchall()
    else:
        sql_command = "SELECT * FROM requests WHERE target_id = %s"
        values = [details[7]]
        cursor.execute(sql_command, values)
        requests = cursor.fetchall()
    
    receivers = []
    
    if requests:
        for index, request in enumerate(requests):
            requesterID = (request[1]) 
            receivers.append(request[0]) 
            amount = request[2]

            if myrequests == True:
                details_target = get_details('accountID', receivers[index])
                label = Label(window, text=(f"{receivers[index]} \n ({details_target[0]} {details_target[1]})"))
            else:
                details_target = get_details('accountID', requesterID)
                label = Label(window, text=(f"{requesterID} \n ({details_target[0]} {details_target[1]})"))
            
            label.grid(row=index + 1, column=0)
            
            label = Label(window, text=(f"£{amount}"))
            label.grid(row=index + 1, column=1) 
            
            frame_buttons = Frame(window)
            frame_buttons.grid(row=index + 1, column=2, columnspan=2, pady=(5, 0))
            
            if myrequests:
                button = Button(frame_buttons, text='Cancel', command=lambda r=request[1], rec=request[0]: delete_request(r, rec, details, pk, True))

                button.grid(row=0, column=0)
            else:
                button = Button(frame_buttons, text='Accept', command=lambda r=request[1], rec=request[0], amt=request[2]: accept_request(r, rec, details, amt, pk))
                button.grid(row=0, column=0)

                button = Button(frame_buttons, text='Reject', command=lambda r=request[1], rec=request[0]: reject_request(r, rec, details, pk))
                button.grid(row=0, column=1)
    
    else:
        alert(window, 'You have no pending requests.', alert_row, 0, 'black', 3)
        
    def reject_request(requesterID, targetID, details, pk):
        delete_request(targetID, requesterID, details, pk, reset=False)
        balance_window(pk) 
        
def accept_request(requesterID, targetID, details_receiver, amount, pk):
    details_requester = get_details('accountID', requesterID)
    
    if details_receiver[6] < amount:
        alert(root, 'Balance is too low.', alert_row, 0, 'red', 1)
    else:
        def handle_verification(result):
            verify(root, details_requester, details_receiver, amount, handle_verification, 'transfer')
            if result:
                transfer(targetID, requesterID, amount)
                delete_request(requesterID, targetID, details_requester, pk, False)
                balance_window(pk) 
                alert(root, f'Successfully transferred £{amount} to {details_requester[0]} {details_requester[1]}', alert_row, 0, 'green', 1)
            else:
                balance_window(pk) 
                alert(root, 'Verification failed.', alert_row, 0, 'red', 1)

        verify(root, details_requester, details_receiver, amount, handle_verification, 'transfer')

def verify(window, details, details_target, amount, callback, reason):
    purge(window)
    
    def verified(condition):
        return condition

    def handle_verification(result):
        callback(result)
    
    if reason == 'request':
        label = Label(window, text="Confirm Request", font=font_big)
        label.grid(column=0, row=0)
        
        button = Button(window, text="Verify Request", command=lambda:handle_verification(verified(True)), font=font_default)
        button.grid(column=0, row=4, pady=(10,0))
    else:
        label = Label(window, text="Confirm Transfer", font=font_big)
        label.grid(column=0, row=0)
        
        button = Button(window, text="Verify Transaction", command=lambda:handle_verification(verified(True)), font=font_default)
        button.grid(column=0, row=4, pady=(10,0))
    

    label = Label(window, text=f"From: {details_target[0]} {details_target[1]}", font=font_default)
    label.grid(column=0, row=1)
    
    label = Label(window, text=f"To: {details[0]} {details[1]}", font=font_default)
    label.grid(column=0, row=2)

    
    label = Label(window, text=f"Amount: £{str(amount)}", font=font_big)
    label.grid(column=0, row=3)
    
    button = Button(window, text="Cancel", command=lambda:handle_verification(verified(False)), font=font_default)
    button.grid(column=0, row=5)

def delete_request(requesterID, targetID, details, pk, reset):
    sql_command = "DELETE FROM requests WHERE requester_id = %s AND target_id = %s"
    values = [requesterID, targetID]

    cursor.execute(sql_command, values)
    mydb.commit()

    if reset:
        purge(root)
        request_menu(root, details, pk)

def request(window, details, pk):
    def check_requests(accountID, targetID):
        sql_command = "SELECT * FROM requests WHERE requester_id = %s AND target_id = %s"
        values = [accountID, targetID]
        
        cursor.execute(sql_command, values)
        return cursor.fetchone()
    targetID = entries['Request From'].get()
    amount = entries['Amount'].get()
    
    details_target = get_details('accountID', targetID)
    accountID = details[7]
    
    if targetID and amount:
        try:
            float(amount)
        except ValueError:
            alert(window, 'Amount must be a number.', alert_row, 0, 'red', 1)
            return
        if details_target:
            if targetID != accountID:
                prev_requested = check_requests(accountID, targetID)
                if prev_requested == None:
                    def handle_verification(result):
                        verify(root, details, details_target, amount, handle_verification, 'request')
                        
                        if result == True:
                            sql_command = f"INSERT INTO requests (target_id, requester_id, amount) VALUES (%s, %s, %s)"
                            values = [targetID, accountID, amount]
                            cursor.execute(sql_command, values)
                            mydb.commit()
                            
                            request_menu(window, details, pk)
                            alert(window, f'Successfully requested {amount} from {details_target[0]} {details_target[1]}', alert_row, 0, 'green', 3)
                        elif result == False:
                            request_menu(window, details, pk)
                            alert(root, 'Verification failed.', alert_row, 0, 'red', 1)
                    verify(root, details, details_target, amount, handle_verification, 'request')
                else:
                    alert(window, 'Cannot request from same person twice.', alert_row, 0, 'red', 1)
                    entries_delete(['Request From'])
            else:
                alert(window, 'Cannot request from yourself.', alert_row, 0, 'red', 1)
                entries_delete(['Request From'])
        else:
            alert(window, 'Invalid Target ID', alert_row, 0, 'red', 1)
            entries_delete(['Request From'])
    else:
        alert(window, 'Invalid target id or amount.', alert_row, 0, 'red', 1)
    
def admin_panel():
    purge(root)
    
    label = Label(root, text="Admin Panel", font=font_big)
    label.grid(row=0, column=0)
    
    create_labels_and_entries(root, labels_admin_panel)
    
    frame = LabelFrame(root, borderwidth=1, text="Show User Details")
    frame.grid(row=2, column=0)
    
    button = Button(frame, text="Show User Details by ID", command=lambda: show_user('accountID'))
    button.grid(row=0, column=0)
    
    button = Button(frame, text="Show User Details by E-mail", command=lambda: show_user('e_mail'))
    button.grid(row=0, column=1, padx=10)
    
    frame = LabelFrame(root, borderwidth=1, text="Change User Details")
    frame.grid(row=3, column=0)
    
    button = Button(frame, text="Change User Details by ID", command=lambda: change_user('accountID'))
    button.grid(row=0, column=0)
    
    button = Button(frame, text="Change User Details by E-mail", command=lambda: change_user('e_mail'))
    button.grid(row=0, column=1, padx=10)
    
def show_user(target):
    if target == 'accountID':
        criteria = entries['Target ID'].get()
    else:
        criteria = entries['Target E-mail'].get()
    if criteria:
        details = get_details(target, criteria)
    
    else:
        alert(root, 'Invalid Target ID / E-mail', alert_row, 0, 'red', 1)
        return
    
    if details:
        details_root = Tk()
        details_root.columnconfigure(0, weight=1)
        
        frame = Frame(details_root)
        frame.grid(row=0, column=0)
        
        create_labels_only(frame, labels_user_details, 0)

        create_labels_only(frame, details, row=1)
            
        button = Button(details_root, text="Close", command=lambda: close_window(details_root))
        button.grid(row=1, column=0, sticky=W, padx=10)
    else:
        alert(root, 'No records were found for Target ID / E-mail', alert_row, 0, 'red', 1)
    
def change_user(criteria):
    if criteria == 'accountID':
        target = entries['Target ID'].get()
    else:
        target = entries['Target E-mail'].get()
    if target:
        details = get_details(criteria, target)
    else:
        alert(root, 'Invalid Target ID / E-mail', alert_row, 0, 'red', 1)
        return
    
    if details:
        details_root = Tk()
        details_root.columnconfigure(0, weight=1)
        
        frame = Frame(details_root)
        frame.grid(row=0, column=0)
        
        create_labels_and_entries(frame, labels_sign_up) #FIX change to labels_change_user
            
        for detail in details:
            entries[detail].insert(details[detail])
    
def close_window(rootValue):
    rootValue.destroy()
## 
def sign_up_page():
    purge(root)
    
    label = Label(root, text="Sign Up", font=font_big)
    label.grid(row=0, column=0)
    
    create_labels_and_entries(root, labels_sign_up)
    
    button = Button(root, text='Sign Up', font=font_default, command=lambda: sign_up(labels_sign_up, root))
    button.grid(row=10, column=0)
    
    button = Button(root, text='Go Back', font=font_default, command=lambda: main_page(True, root))
    button.grid(row=11, column=0)
    
def sign_up(labels, window):
    variables = {}
    for label in labels:
        value = entries[label].get()
        if not value:
            alert(window, f'Field {label} is empty.', alert_row, 0, 'red', 1)
            return
        variables[label] = value
           
    validated = validate(variables, window)

    if validated == True:
        
        values = []
        dob = datetime.strptime(variables['Date of Birth'], '%d/%m/%Y').strftime('%Y-%m-%d')
        date_index = list(variables.keys()).index('Date of Birth')
        
        for key, value in enumerate(variables.values()):
            if key == date_index:
                values.append(dob)
            else:
                values.append(value)    
                                               
        if variables['E-mail'] == variables['Confirm E-mail']:
            if variables['Password'] == variables['Confirm Password']:
                email_used = check_email(values)
                if email_used == None:
                    sign_up_success(window, values)
                else:
                    alert(window, 'E mail already in use.', alert_row, 0, 'red', 1)
                    entries_delete(['E-mail', 'Confirm E-mail'])
            else:
                alert(window, 'Passwords do not match up.', alert_row, 0, 'red', 1)
                entries_delete(['Confirm Password'])
        else:
                alert(window, 'E-mails do not match up.', alert_row, 0, 'red', 1)
                entries_delete(['Confirm E-mail'])

def check_email(values):
    email = values[3]
    sql_command = "SELECT * FROM bank WHERE e_mail = %s"
    cursor.execute(sql_command, (email,))
    fetched = cursor.fetchone()
    return fetched

def sign_up_success(window, values):
    
    sql_command = """INSERT INTO bank 
    (first_name, last_name, dob, e_mail, postcode, password, balance, accountID) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
    accountID = generate_accountID(values)

    values.pop()
    values.pop(4)
    values.extend([0, accountID])

    cursor.execute(sql_command, values)
    mydb.commit()
    alert(window, 'Successfully signed up, please go back to log in.', alert_row, 0, 'green', 1)
    
def validate(variables, window):
    pattern_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    pattern_password = r'^.{8,}$'
    pattern_date = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
    pattern_postcode = r'^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$'

    
    e_mail_regex = re.match(pattern_email, variables['E-mail'])
    password_regex = re.match(pattern_password, variables['Password'])
    date_regex = re.match(pattern_date, variables['Date of Birth'])
    postcode_regex = re.match(pattern_postcode, variables['Post Code'])

    if e_mail_regex and password_regex and date_regex and postcode_regex:
        return True
    else:
        if not date_regex:
            alert(window, 'Date format must be DD/MM/YYYY.', alert_row, 0, 'red', 1)
            entries_delete(['Date of Birth'])
        elif not e_mail_regex:
            alert(window, 'E-mail format must be example@smth.com.', alert_row, 0, 'red', 1)
            entries_delete(['E-mail'])
        elif not postcode_regex:
            alert(window, 'Invalid UK post code. (Must be all CAPITALISED)', alert_row, 0, 'red', 1)
            entries_delete(['Post Code'])
        else:
            alert(window, 'Password must be at least 8 characters long.', alert_row, 0, 'red', 1)
            entries_delete(['Password'])
        return False

######################################
def generate_accountID(values):
    first_name = values[0]
    last_name = values[1]
    while True:
        random_no = random.randint(100000, 999999)
        accountID = first_name.capitalize()[0] + last_name.capitalize()[0] + str(random_no)

        cursor.execute("SELECT COUNT(*) FROM bank WHERE accountID = %s", (accountID,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            return accountID
def entries_delete(values):
    for value in values:
        entries[value].delete(0, END)

def alert(window, value, row, column, colour, columnspan):
    global labelalert
    if 'labelalert' in globals() and labelalert:
        labelalert.destroy()
    labelalert = Label(window, text=value, font=font_default, fg=colour)
    labelalert.grid(row=row, column=column, columnspan=columnspan)
    return labelalert

def purge(window):
    for widget in window.winfo_children():
        widget.destroy()

def get_details(target, crit):
    cursor.execute(f"SELECT * FROM bank WHERE {target} = '{crit}'")
    details = cursor.fetchone()
    if details == None:
        return None
    else:
        #Table
        """
        firstName = details[0]
        lastName = details[1]
        dob = details[2]
        e_mail = details[3]
        postcode = details[4]
        password = details[5]
        balance = details[6]
        accountID = details[7]
        """ 
        
        return details

def create_labels_and_entries(rootValue, labelList):
    frame = Frame(rootValue)
    frame.grid(row=1, column=0)
    for label in labelList:
        label_widget = Label(frame, text=label, font=font_default)
        label_widget.grid(row=labelList.index(label) + 1, column=0, padx=5)
        
        entry_widget = Entry(frame)
        entry_widget.grid(row=labelList.index(label) + 1, column=1)

        entries[label] = entry_widget
        
def create_labels_only(rootValue, labelList, row):
    for label in labelList:
        label_widget = Label(rootValue, text=label, font=font_default)
        label_widget.grid(row=row, column=labelList.index(label) + 1, padx=5)
    

main_page(False, None) #created buttons for main

balance_window('admin')

# admin_panel()``

root.mainloop()