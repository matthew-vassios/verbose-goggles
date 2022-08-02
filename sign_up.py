import psycopg2
import PySimpleGUI as sg


#CONNECT TO DATABASE
conn = None
cur = None


#USERNAME AND PASSSWORD ARRAY
username = ''
password = ''

#CUSTOMER QUERY 
select_customer_query = ('''
                        SELECT policy_id,
		                first_name ||' '|| last_name AS full_name,
		                date_of_birth,
		                address_1 ||', '|| city ||', '|| state ||' '|| zip_code AS primary_address,
		                phone_number,
		                email, 
		                gender
                        FROM customers AS c
                        JOIN customer_address AS ca ON c.address_id = ca.address_id;
''')


#PROGRESS BAR FUNCTION
def progress_bar():
    sg.theme('DarkGrey2')
    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()

#SIGN-UP FUNCTION
def create_account():
    global username, password
    sg.theme('DarkGrey2')
    layout = [[sg.Text("Sign-Up", size=(17,1), font=25, justification='c')],
            [sg.Text("First Name", size=(17,1), font=14), sg.InputText(key='--FNAME--', font=16)],
            [sg.Text("Last Name", size=(17,1), font=14), sg.InputText(key='--LNAME--', font=16)],
            [sg.Text("Date of Birth", size=(17,1), font=14), sg.InputText(key='--DOB--', font=16)],
            [sg.Text("Address", size=(17,1), font=14), sg.InputText(key='--ADDRESS--', font=16)],
            [sg.Text("City", size=(17,1), font=14), sg.InputText(key='--CITY--', font=16)],
            [sg.Text("State", size=(17,1), font=14), sg.InputText(key='--STATE--', font=16)],
            [sg.Text("Zip Code", size=(17,1), font=14), sg.InputText(key='--ZIP--', font=16)],
            [sg.Text("E-Mail", size=(17,1), font=14), sg.InputText(key='--EMAIL--', font=16)],
            [sg.Text("Re-enter E-Mail", size=(17,1), font=14), sg.InputText(key='--REMAIL--', font=16)],
            [sg.Text("Create Username", size=(17,1), font=14), sg.InputText(key='--UNAME--', font=16)],
            [sg.Text("Create Password", size=(17,1), font=14), sg.InputText(key='--PASSWORD--', password_char='*', font=16)],
            [sg.Text("Re-enter Password", size=(17,1), font=14), sg.InputText(key='--PASSWORD--', password_char='*', font=16)],
            [sg.Button("Submit"), sg.Button("Cancel"), sg.Button("Login")]]

    window = sg.Window("Sign Up", layout)


    #CREATE A LOOP
    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Submit':
                username = values['--UNAME--']
                password = values['--PASSWORD--']
                if values['--EMAIL--'] != values['--REMAIL--']:
                    sg.popup_error("Incorrect Password", font=16)
                    continue
                elif values['--EMAIL--'] == values['--REMAIL--']:
                    progress_bar()
                    window.close()
    window.close()
create_account()


#LOGIN TO ACCOUNT FUNCTION
def login():
        global username, password
        sg.theme("DarkGrey2")
        layout = [[sg.Text("Log In", size=(15, 1), font=25)],
                [sg.Text("Username", size=(15, 1), font=14), sg.InputText(key='--UNAME--')],
                [sg.Text("Password", size=(15, 1), font=14), sg.InputText(key='--PASSWORD--', password_char='*')],
                [sg.Button("Login"), sg.Button("Cancel")]
        ]

        window = sg.Window("Log In", layout)

        #CREATE A LOOP
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            else:
                if event == "Login":
                    if values['--UNAME--'] == username and values['--PASSWORD--'] == password:
                        sg.popup("Welcome!")
                        break
                    elif values['--UNAME--'] != username or values['--PASSWORD--'] != password:
                        sg.popup("Invalid login. Try again.")

        window.close()
login()



#CONNECT TO DATABASE
conn = None
cur = None


try:
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'test_insurance_project',
        user = 'postgres',
        password = 'Left0ver$',
        port= '5432'    
    )

    cur = conn.cursor()


    #QUERY FUNCTION
    #FUNCTION TO QUERY CUSTOMER DATA


    #FUNCTION TO QUERY EMPLOYEE DATA

    #CREATE
    #CREATE BANK
    # create_bank = ''' CREATE TABLE IF NOT EXISTS bank (
    #                     bank_id         VARCHAR PRIMARY KEY,
    #                     bank_name       varchar,
    #                     routing_number  varchar(9),
    #                     account_number  varchar(12)
    # )'''
    # cur.execute(create_bank)


    #CREATE CARD
    create_card = ''' CREATE TABLE IF NOT EXISTS card (
                        card_id         varchar(9),
                        card_type       varchar,
                        card_number     varchar(16),
                        expirate_date   varchar,
                        cvv_code        varchar(3)
    )'''
    cur.execute(create_card)


    #CREATE CREDENTIALS
    create_credentials = ''' CREATE TABLE IF NOT EXISTS credentials (
                                credential_id   varchar,
                                username_id     varchar(10),
                                password_id     varchar(20)
    )'''
    cur.execute(create_credentials)


    #CREATE CUSTOMER ADDRESS
    create_customer_address = ''' CREATE TABLE IF NOT EXISTS customer_address (
                                    address_id  varchar PRIMARY KEY,
                                    address_1   varchar,
                                    city        varchar,
                                    state       varchar,
                                    zip_code    varchar
    )'''    
    cur.execute(create_customer_address)


    #CREATE CUSTOMERS
    create_customers = ''' CREATE TABLE IF NOT EXISTS customers (
        customer_id     varchar(9) PRIMARY KEY,
        credential_id   varchar(9),
        first_name      varchar(30),
        last_name       varchar(40),
        date_of_birth   varchar,
        address_id      varchar,
        phone_number    varchar(20),
        email           varchar(100),
        gender          varchar(9),
        policy_id       varchar(10)
    )'''
    cur.execute(create_customers)
    cur.fetchall()


    #CREATE EMPLOYEES
    create_employees = ''' CREATE TABLE IF NOT EXISTS employees (
                            employee_id     varchar(9),
                            credential_id   varchar,
                            first_name      varchar(30),
                            last_name       varchar(40),
                            email           varchar(100)
    )'''
    cur.execute(create_employees)


    #CREATE PAYMENTS
    create_payments = ''' CREATE TABLE IF NOT EXISTS payments (
                            payment_id      varchar,
                            amount_due      varchar, 
                            amount_paid     varchar,
                            bank_id         varchar(9),
                            card_id         varchar
    )'''
    cur.execute(create_payments)
    

    #CREATE POLICIES
    create_policies = ''' CREATE TABLE IF NOT EXISTS policies (
                            policy_id       varchar(10),
                            policy_type     varchar,
                            policy_status   varchar,
                            effect_date     varchar,
                            paid_to_date    varchar,
                            term_date       varchar,
                            payment_id      varchar
    )'''
    cur.execute(create_policies)


    #INSERT SCRIPT INTO DB
    #INSERT BANK
    insert_bank = ''' INSERT INTO bank (
                        bank_id         varchar PRIMARY KEY,
                        bank_name       varchar,
                        routing_number  varchar(9),
                        account_number  varchar(12))
                    VALUES
                        (%s, %s, %s, %s)
    )'''
    cur.execute(insert_bank)
    for r in cur.fetchall():
        print(insert_bank)


    #INSERT CARD
    insert_card = ''' INSERT INTO card (
                        card_id         varchar(9),
                        card_type       varchar,
                        card_number     varchar(16),
                        expirate_date   varchar,
                        cvv_code        varchar(3)
                    VALUES 
                        (%s, %s, %s, %s, %s)
    )'''

    
    #INSERT CREDENTIALS
    insert_credentials = ''' INSERT INTO credentials (
                                credential_id   varchar,
                                username_id     varchar(10),
                                password_id     varchar(20)
                            VALUES 
                                (%s, %s, %s,)
    )'''
    
    
    #INSERT CUSTOMER_ADDRESS 
    insert_customer_address = ''' INSERT INTO customer_address (
                                    address_id  varchar PRIMARY KEY,
                                    address_1   varchar,
                                    city        varchar,
                                    state       varchar,
                                    zip_code    varchar
                                VALUES (%s, %s, %s, %s, %s)
    )'''


    #INSERT CUSTOMERS
    insert_customer = ''' INSERT INTO customer (
                            customer_id, 
                            credential_id, 
                            first_name, 
                            last_name, 
                            date_of_birth, 
                            address_id, 
                            phone_number, 
                            email, 
                            gender, 
                            policy_id)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    )'''

    #UPDATE CUSTOMERS
    cur.execute('SELECT customer_id, ')


    #EXECUTE QUERY
    #execute query
    cur.execute('SELECT * FROM customers')
    for r in cur.fetchall():
        print(f'Policy Number: {r}')




    #close the connection
    conn.commit()

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()