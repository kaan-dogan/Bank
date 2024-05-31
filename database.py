import mysql.connector
import random #to generate an account id

mydb = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='password123',
    database='BANK'
)
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS bank")

cursor.execute("USE bank")

cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(100),
    sender_id VARCHAR(100),
    receiver_id VARCHAR(100),
    amount FLOAT,
    date DATE,
    PRIMARY KEY (transaction_id)
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

def get_details(target, crit):
    try:
        print(target, crit)
        if target == 'e_mail':
            cursor.execute("SELECT * FROM bank WHERE e_mail = %s", (crit,))
        elif target == 'accountID':
            cursor.execute("SELECT * FROM bank WHERE accountID = %s", (crit,))

        details = cursor.fetchone()
        return details
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

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
        