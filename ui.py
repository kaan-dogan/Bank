from tkinter import *

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

labels_change_user = [
    'First Name',
    'Last Name',
    'Date of Birth',
    'E-mail',
    'Post Code',
    'Password',
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
    'Balance'
]

labels_transaction_history = [
    'Sender ID',
    'Receiver ID',
    'Amount (£)',
    'Date',
    'Transaction ID'
]

def create_labels_only(rootValue, labelList, row, font_=font_default, width_ = None):
    for label in labelList:
        label_widget = Label(rootValue, text=label, font=font_, width=width_)
        label_widget.grid(row=row, column=labelList.index(label) + 1, padx=5)
        
def create_labels_and_entries(rootValue, labelList):
    frame = Frame(rootValue)
    frame.grid(row=1, column=0)
    for label in labelList:
        label_widget = Label(frame, text=label, font=font_default)
        label_widget.grid(row=labelList.index(label) + 1, column=0, padx=5)
        
        entry_widget = Entry(frame)
        entry_widget.grid(row=labelList.index(label) + 1, column=1)

        entries[label] = entry_widget

def purge(window):
    for widget in window.winfo_children():
        widget.destroy()
        
def alert(window, value, row, column, colour, columnspan):
    if 'labelalert' in globals() and labelalert:
        labelalert.destroy()
    labelalert = Label(window, text=value, font=font_default, fg=colour)
    labelalert.grid(row=row, column=column, columnspan=columnspan)
    return labelalert

def entries_delete(values):
    for value in values:
        entries[value].delete(0, END)
        
def close_window(rootValue):
    rootValue.destroy()
    
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
    

    label = Label(window, text=f"From: {details[0]} {details[1]}", font=font_default)
    label.grid(column=0, row=1)
    
    label = Label(window, text=f"To: {details_target[0]} {details_target[1]}", font=font_default)
    label.grid(column=0, row=2)

    
    label = Label(window, text=f"Amount: £{str(amount)}", font=font_big)
    label.grid(column=0, row=3)
    
    button = Button(window, text="Cancel", command=lambda:handle_verification(verified(False)), font=font_default)
    button.grid(column=0, row=5)