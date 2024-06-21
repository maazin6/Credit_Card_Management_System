import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import random
import datetime


def addNew(val):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    #1. acc_id
    #2. name
    #3. dob
    #4. email
    #5. aadhar
    #6. address
    #7. password
    #8. role 
    cursor.execute("CREATE TABLE IF NOT EXISTS account (acc_id INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT, dob TEXT, email TEXT, aadhar TEXT, address TEXT, password TEXT,role TEXT)")
    cursor.execute('INSERT INTO account (name,dob,email,aadhar,address,password,role) VALUES (?, ?, ?, ?, ?, ?, ?)', val)
    conn.commit()
    conn.close()

#val=[acc_id,pin,limit]
def addNewCard(val):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    
    def cardnos(str='select cardno from card'):
        
        # Insert data into the table
        cursor.execute(str)
        rows = cursor.fetchall()
        '''for row in rows:
            print(row)'''
        return rows
    
    def gen_cardno():
        x=random.randint(1000000000000000,9999999999999999)
        
        flag=0
        rows=cardnos()
        
        for i in rows:
            if x in i:
                flag=1
                break
        if flag==1:
            return gen_cardno()
        else:
            return x
        return x
    num=gen_cardno()
    val.append(num)
    val.append(str(datetime.datetime.now().date()))
    
    #1. cardno AUTOINCREMENT *randomized not in card table
    #2. acc_id FOREGIN KEY(ACCOUNT TABLE)
    #3. pin
    #4. limit
    
    #cursor.execute("CREATE TABLE IF NOT EXISTS card (cardno INTEGER PRIMARY KEY, pin INTEGER, cardlimit INTEGER, acc_id TEXT FOREIGN KEY REFERENCES account(acc_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS card (cardno INTEGER PRIMARY KEY, pin INTEGER, cardlimit INTEGER, acc_id TEXT, doj date)")

    
    cursor.execute('INSERT INTO card (acc_id,pin,cardlimit,cardno,doj) VALUES (?, ?, ?, ?, ?)', val)
    conn.commit()
    conn.close()

def signup():
    def getid():
        # Connect to SQLite database 
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        # Insert data into the table
        cursor.execute('select acc_id from account')
        # Commit the changes
        conn.commit()
        rows = cursor.fetchall()
        accid=rows[-1][0]
        # Close the connection
        conn.close()
        return accid 
    def check_password_signup():
        val = [
            name_entry.get(),
            DOB_entry.get(),
            email_entry.get(),
            aadhar_entry.get(),
            address_entry.get(),
            password_entry.get(),
            'U']
        cpass = confirm_password_entry.get()
        # Check if passwords match
        if val[-2] != cpass:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
        else:
            addNew(val)
            accid = getid()
            messagebox.showinfo("Success", "Password matched.\n Your Account no.: "+str(accid))
            root.destroy()
            login()
    root = tk.Tk()
    root.title("SIGN UP")
    root.geometry("400x300")
    tk.Label(root, text="      ").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="").grid(row=0, column=1, padx=10, pady=5, sticky="w")
    tk.Label(root, text="").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Name:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Date of Birth(YYYY-MM-DD):").grid(row=3, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Email:").grid(row=4, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Aadhar:").grid(row=5, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Address:").grid(row=6, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Password:").grid(row=7, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Confirm Password:").grid(row=8, column=2, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.grid(row=2, column=3, padx=10, pady=5)
    DOB_entry = tk.Entry(root)
    DOB_entry.grid(row=3, column=3, padx=10, pady=5)
    email_entry = tk.Entry(root)
    email_entry.grid(row=4, column=3, padx=10, pady=5)
    aadhar_entry = tk.Entry(root)
    aadhar_entry.grid(row=5, column=3, padx=10, pady=5)
    address_entry = tk.Entry(root)
    address_entry.grid(row=6, column=3, padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=7, column=3, padx=10, pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.grid(row=8, column=3, padx=10, pady=5)
    submit_button = tk.Button(root, text="SUBMIT", command=check_password_signup)
    submit_button.grid(row=9, column=2, columnspan=2, pady=10)
    root.mainloop()

def login():

    def open_signup_window():
        root.destroy()  # Close the login window
        signup()        # Open the signup window

    def check_login():
        
        username = username_entry.get()
        password = password_entry.get()

        # Connect to the database
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        # Check if the username and password combination exists in the database
        cursor.execute("SELECT * FROM account WHERE acc_id=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + user[1] + "!")
            root.destroy()
            if user[7]=='U':
                user_menu(username)
            else:
                admin_menu()
            
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        # Close the database connection
        conn.close()

        root.mainloop()
    
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("300x200")  # Adjust dimensions as needed

    tk.Label(root, text="      ").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="").grid(row=0, column=1, padx=10, pady=5, sticky="w")
    tk.Label(root, text="").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    
    # Username Entry
    tk.Label(root, text="Account no.:").grid(row=2, column=2)
    username_entry = tk.Entry(root)
    username_entry.grid(row=2, column=3)

    # Password Entry
    tk.Label(root, text="Password:").grid(row=3, column=2)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=3, column=3)

    # Login Button
    login_button = tk.Button(root, text="Login",command=check_login)
    login_button.grid(row=6, columnspan=5, pady=10)

    # Signup Button
    signup_button = tk.Button(root, text="Signup", command=open_signup_window)
    signup_button.grid(row=7, columnspan=5, pady=10)

    root.mainloop()

def queries(str):
    # Connect to SQLite database 
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    # Execute the query
    cursor.execute(str)
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

    
#for select queries
def squeries(str='select * from account'):
    # Connect to SQLite database 
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    # Insert data into the table
    cursor.execute(str)
    # Commit the changes
    conn.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Close the connection
    conn.close()
    
#get cardno given acc_id
def get_cardno(acc_id):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute("select cardno from card where acc_id=?",(acc_id,))
    rows=cursor.fetchone()
    conn.commit()
    conn.close()
    return rows[0]

class User:
    
    def __init__(self,accid):
        self.accid=accid
        
    def show_card_details(self):

        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        # Insert data into the table
        
        stri = "select * from card where acc_id="
        stri = stri + str(self.accid)
        
        cursor.execute(stri)
        #cursor.execute('select * from card ')
        
        # Commit the changes
        conn.commit()
        rows = cursor.fetchall()
        conn.close()
        if len(rows)==0:
            messagebox.showerror("Error", "Card does not exist!")
        else:
            display_list_of_lists(rows)
        
    def create_card_menu(self):

        def check_pin_addcard():
            
                val = [
                    self.accid,
                    pin_entry.get(),
                    limit_entry.get()
                ]
                repin = repin_entry.get()

                # Check if passwords match
                if val[1] != repin:
                    messagebox.showerror("Error", "PINs do not match. Please try again.")
                else:
                    #val=[acc_id,pin,limit]
                    addNewCard(val)
                    messagebox.showinfo("Success", "Pin matched.")
                    root.destroy()
                    user_menu(val[0])
            
   
        root = tk.Tk()
        root.title("Add Card")
        root.geometry("300x200")

        # Labels and Entry Fields
        tk.Label(root, text="Account No.:"+str(self.accid)).pack()
        #tk.Label(root, text="acc_id").pack()

        tk.Label(root, text="Select Limit:").pack()
        limit_entry = tk.Entry(root)
        limit_entry.pack()

        tk.Label(root, text="Enter PIN:").pack()
        pin_entry = tk.Entry(root, show="*")
        pin_entry.pack()

        tk.Label(root, text="Reenter PIN:").pack()
        repin_entry = tk.Entry(root, show="*")
        repin_entry.pack()

        # Button to create the card
        create_card_button = tk.Button(root, text="Create Card",command=check_pin_addcard)
        create_card_button.pack(pady=5)

        root.mainloop()
        

    
def user_menu(accid):
    root = tk.Tk()
    root.title("Customer Menu")
    root.geometry("300x250")

    user=User(accid)

    def logout():
        root.destroy()
        login()
    
    def add_card():
        
        # Connect to SQLite database 
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        # Insert data into the table
        cursor.execute('select count(*) from card where acc_id=?', (accid,))
        # Commit the changes
        conn.commit()
        count = cursor.fetchone()
        # Close the connection
        conn.close()
        
        if (count[0]==0):
            root.destroy()
            user.create_card_menu()
        else:
            messagebox.showerror("Error!","Card already Exists for Account No.:"+str((accid,)))
            #cust_menu((accid,))
            
    def user_show_trans():
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        cursor.execute('select cardno from card where acc_id=?', (accid,))
        conn.commit()
        cust = cursor.fetchone()
        # Close the connection
        conn.close()
        show_trans(cust[0])

    def check_bill():
        def submit():
            selected_month = month_var.get()
            selected_year = year_var.get()
            print("Selected Month:", selected_month)
            print("Selected Year:", selected_year)
            
            cardno=get_cardno(accid)
            window.destroy()
            print(cardno, selected_month, selected_year)
            show_bill(cardno, selected_month, selected_year)
            
            # You can perform further actions with the selected month and year here
        
        # Initialize Tkinter window
        window = tk.Tk()
        window.title("Month and Year Input")

        month_var = tk.IntVar()
        
        
        # Label for month
        month_label = ttk.Label(window, text="Select Month:")
        month_label.grid(row=0, column=0, padx=10, pady=5)
        
        # Combobox for month
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        year_var = tk.IntVar()
        
        month_combobox = ttk.Combobox(window, textvariable=month_var, values=months)
        #month_combobox = ttk.Combobox(window, textvariable=month_combobox,values=months)
        month_combobox.grid(row=0, column=1, padx=10, pady=5)
        #month_combobox.current(0)  # Set default value
        
        # Label for year
        year_label = ttk.Label(window, text="Select Year:")
        year_label.grid(row=1, column=0, padx=10, pady=5)
        
        # Combobox for year
        years = [year for year in range(2020, 2025)]  # Assuming range from 2000 to 2030
        
        year_combobox = ttk.Combobox(window, textvariable=year_var, values=years)
        year_combobox.grid(row=1, column=1, padx=10, pady=5)
        #year_combobox.current(0)  # Set default value
       
        
        # Submit button
        
        submit_button = ttk.Button(window, text="Submit", command=submit)
        submit_button.grid(row=2, columnspan=2, padx=10, pady=10)
        
        
        
        # Run Tkinter event loop
        window.mainloop()
        
            
    add_card_button = tk.Button(root, text="Add Card", command=add_card)
    add_card_button.pack(pady=5)

    show_card_button = tk.Button(root, text="Show Card Details", command=user.show_card_details)
    show_card_button.pack(pady=5)

    check_bill_button = tk.Button(root, text="Check Bill", command=check_bill)
    check_bill_button.pack(pady=5)

    show_trans_button = tk.Button(root, text="Show transactions", command=user_show_trans)
    show_trans_button.pack(pady=5)

    pay_dues_button = tk.Button(root, text="Pay Dues", command=pay_dues)
    pay_dues_button.pack(pady=5)

    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=5)
    root.mainloop()
    

    
def display_list_of_lists(data):
    root = tk.Tk()
    root.title("Show Card Details")
    
    # Create Treeview widget
    tree = ttk.Treeview(root)
    
    # Define columns
    tree["columns"] = tuple(f"column_{i}" for i in range(len(data[0])))

    # Configure column headings
    for i, heading in enumerate(['Card No.','PIN',"Limit",'Account No.','Date of Joining']):
        tree.heading(f"column_{i}", text=heading)

    # Add data rows
    for row in data[0:]:
        tree.insert("", "end", values=row)

    # Pack the Treeview widget
    tree.pack(expand=True, fill="both")

    root.mainloop()   


def show_trans(cardno):
    # Connect to SQLite database
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()

    # Retrieve transactions for the specified cardno from the trans table
    cursor.execute('SELECT * FROM trans WHERE cardno = ?', (cardno,))
    transactions = cursor.fetchall()
    #print(transactions)
    # Close connection
    conn.close()

    # Create a Tkinter window
    window = tk.Tk()
    window.title(f"Transactions for Card No {cardno}")

    # Create a treeview widget to display transactions
    tree = ttk.Treeview(window, columns=("Date", "Description", "Amount", "Cardno"))
    tree.heading("#0", text="ID")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")
    tree.heading("Date", text="Date")
    tree.heading("Cardno", text="Card Number")

    # Insert transactions into the treeview
    for transaction in transactions:
        tree.insert("", "end", text=transaction[0], values=(transaction[4], transaction[1], transaction[2], transaction[3]))

    tree.pack(expand=True, fill=tk.BOTH)

    # Run the Tkinter event loop
    window.mainloop()

def pay_dues():
    print("Pay Dues")

def drop():
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute("drop table IF EXISTS account")
    cursor.execute("drop table IF EXISTS card")
    cursor.execute("drop table IF EXISTS trans")
    cursor.execute("drop table IF EXISTS bill")

    conn.commit()
    conn.close()

def show():
    print("Table Account:\n")
    squeries()
    print()
    print('*'*50)
    print()
    print("Table card:\n")
    squeries("select * from card")
    print()
    print('*'*50)
    print()
    print("Table trans:\n")
    squeries("select * from trans")
    print()
    print('*'*50)
    print()
    print("Table bill:\n")
    squeries("select * from bill")

def create_bill():
    gen_bill(2329737369216735,1,2024)
    gen_bill(2329737369216735,2,2024)
    gen_bill(2329737369216735,3,2024)
    gen_bill(2329737369216735,4,2024)

    gen_bill(7797479004554915,1,2024)
    gen_bill(7797479004554915,2,2024)
    gen_bill(7797479004554915,3,2024)
    gen_bill(7797479004554915,4,2024)
    
def create():
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    
    #account table
    #1. acc_id    #2. name    #3. dob    #4. email    #5. aadhar    #6. address    #7. password    #8. role
    
    cursor.execute("CREATE TABLE IF NOT EXISTS account (acc_id INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT, dob DATE, email TEXT, aadhar TEXT, address TEXT, password TEXT,role TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card (cardno INTEGER PRIMARY KEY, pin INTEGER, cardlimit INTEGER, acc_id INTEGER, doj date)")
    
    cursor.execute("INSERT INTO account (acc_id,name,dob,email,aadhar,address,password,role) VALUES (10000, 'admin', '2002-12-23', 'admin@gmail.com', '123456789', 'home', 'pass', 'A')")
    cursor.execute("INSERT INTO account (name,dob,email,aadhar,address,password,role) VALUES('maazin', '2002-12-23', 'maazin@gmail.com', '123456789', 'home', 'pass', 'U'),('saumya', '2004-02-28', 'saumya@gmail.com', '123456789', 'house', 'sadw', 'U')")
    
    #card table
    #1. cardno 2. pin 3. cardlimit 4. acc_id
    cursor.execute("INSERT INTO card (cardno, pin, cardlimit, acc_id, doj) values (2329737369216735, 2002, 10000, 10001,'2024-01-01'),(7797479004554915, 2002, 10000, 10002,'2024-01-01')")

    #transactions table trans
    #1. trans_id 2. description 3. amount 4. cardno 5. trans_date

    cursor.execute("CREATE TABLE IF NOT EXISTS trans (trans_id INTEGER PRIMARY KEY AUTOINCREMENT ,description TEXT, amount float, cardno INTEGER, trans_date DATE)")

    cursor.execute("INSERT INTO trans VALUES (1, 'gummies', 25, 7797479004554915, '2024-01-23'),(2, 'waterbottle', 20, 7797479004554915, '2024-01-05'),(3, 'books', 400, 7797479004554915, '2024-01-19'),(4, 'bulb', 77, 7797479004554915, '2024-01-12'),(5, 'papers', 100, 7797479004554915, '2024-01-16')")

    cursor.execute("INSERT INTO trans VALUES (6, 'gola', 30, 7797479004554915, '2024-02-23'),(7, 'washing machine', 20000, 7797479004554915, '2024-02-05'),(8, 'blowdryer', 600, 7797479004554915, '2024-02-19'),(9, 'bin', 300, 7797479004554915, '2024-02-12'),(10, 'poster', 300, 7797479004554915, '2024-02-16')")

    cursor.execute("INSERT INTO trans VALUES (11, 'groceries', 2500, 7797479004554915, '2024-03-20'),(12, 'pan', 150, 7797479004554915, '2024-03-05'),(13, 'electricity', 4000, 7797479004554915, '2024-03-30'),(14, 'table', 1600, 7797479004554915, '2024-04-25'),(15, 'paints', 100, 7797479004554915, '2024-03-16')")

    cursor.execute("INSERT INTO trans VALUES (16, 'envelope', 15, 7797479004554915, '2024-04-20'),(17, 'pins', 30, 7797479004554915, '2024-04-05'),(18, 'eggs', 40, 7797479004554915, '2024-04-30'),(19, 'toaster', 700, 7797479004554915, '2024-04-13'),(20, 'medicine', 100, 7797479004554915, '2024-04-26')")

    cursor.execute("INSERT INTO trans VALUES (21, 'fish', 120, 2329737369216735, '2024-01-19'),(22, 'notebooks', 200, 2329737369216735, '2024-01-11'),(23, 'fries', 100, 2329737369216735, '2024-01-02'),(24, 'toys', 155, 2329737369216735, '2024-01-17'),(25, 'salt', 135, 2329737369216735, '2024-01-25')")

    cursor.execute("INSERT INTO trans VALUES (26, 'flowers', 1200, 2329737369216735, '2024-02-19'),(27, 'icetea', 50, 2329737369216735, '2024-02-11'),(28, 'fruits', 250, 2329737369216735, '2024-02-02'),(29, 'toileteries', 150, 2329737369216735, '2024-02-17'),(30, 'sweets', 130, 2329737369216735, '2024-02-25')")

    cursor.execute("INSERT INTO trans VALUES (31, 'charger', 120, 2329737369216735, '2024-03-19'),(32, 'floss', 5, 2329737369216735, '2024-03-11'),(33, 'tissues', 150, 2329737369216735, '2024-03-02'),(34, 'toothbrush', 55, 2329737369216735, '2024-03-17'),(35, 'glasses', 2500, 2329737369216735, '2024-03-25')")

    cursor.execute("INSERT INTO trans VALUES (36, 'gpay', 1000, 2329737369216735, '2024-04-22'),(37, 'phonepay', 150, 2329737369216735, '2024-04-02'),(38, 'food', 400, 2329737369216735, '2024-04-02'),(39, 'food', 600, 2329737369216735, '2024-04-05'),(40, 'plants', 300, 2329737369216735, '2024-04-25')")

    
    
    #bill table bill
    #1. bill_id 2. cardno 3. bill_date 4. pay_date 5. trans_tot 6. fine 7. bill_amount 8. balance 9. status
    
    cursor.execute("CREATE TABLE IF NOT EXISTS bill (bill_id integer primary key autoincrement, cardno integer, bill_date date, pay_date date, trans_tot float, fine float, bill_amount float, balance float,paid_amount float, status text)")
    
    conn.commit()
    conn.close()
def new():
    drop()
    create()
    create_bill()
    show()
    
def admin_menu():
    def logout():
        root.destroy()
        login()
    
    root = tk.Tk()
    root.title("Admin Menu")
    root.geometry("300x200")
            
    add_trans_button = tk.Button(root, text="Add Transaction", command=add_trans)
    add_trans_button.pack(pady=5)

    admin_check_bill_button = tk.Button(root, text="Check Bill", command=check_bill_admin)
    admin_check_bill_button.pack(pady=5)

    admin_show_trans_button = tk.Button(root, text="Show transactions", command=admin_show_trans)
    admin_show_trans_button.pack(pady=5)

    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=5)
    
    root.mainloop()
    
def check_bill_admin():
    print("to be added")
    
def add_trans():
    
    # Function to handle button click event and insert data into the trans table
    squeries('select * from card')
    # Function to handle button click event and insert data into the trans table
    def insert_trans():
        # Get data from entry widgets
        cardno = cardno_entry.get()
        date = date_entry.get()
        description = description_entry.get()
        amount = amount_entry.get()

        # Connect to SQLite database
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        try:
            # Insert data into trans table
            cursor.execute('INSERT INTO trans (cardno, trans_date, description, amount) VALUES (?, ?, ?, ?)', (cardno, date, description, amount))
            conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully")
            root.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Failed to add transaction: " + str(e))
        finally:
            # Close connection
            conn.close()

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Add Transaction")

    # Create and place labels and entry widgets
    tk.Label(root, text="Card No:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    cardno_entry = tk.Entry(root)
    cardno_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    date_entry = tk.Entry(root)
    date_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    description_entry = tk.Entry(root)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Amount:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    # Create a button to add transaction
    add_button = tk.Button(root, text="Add Transaction", command=insert_trans)
    add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

def admin_show_trans():
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Admin - Show Transactions")
    squeries('select * from card')
    # Function to handle button click event and show transactions
    def show_transactions():
        # Get cardno from user input
        cardno = cardno_entry.get()
        show_trans(cardno)

    # Create and place label and entry widget for cardno
    tk.Label(root, text="Enter Card No:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    cardno_entry = tk.Entry(root)
    cardno_entry.grid(row=0, column=1, padx=10, pady=5)

    # Create a button to show transactions
    show_button = tk.Button(root, text="Show Transactions", command=show_transactions)
    show_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()



    conn.commit()
    conn.close()
    
def gen_bill(cardno,month,year):
    
    #year=int(input("Year:"))
    #month=int(input("Month:"))
    bill_date=str(year)+'-'+str(month)+'-'+'25'
    
    if month==12:
        pay_date=str(year+1)+'-'+str('01')+'-'+'25'
        start_date=str(year)+'-'+str(month-1)+'-'+'26'
    elif month==1:
        pay_date=str(year)+'-0'+str(month+1)+'-'+'05'
        start_date=str(year-1)+'-'+'12'+'-'+'26'
    else:
        if month<9:
            pay_date=str(year)+'-0'+str(month+1)+'-'+'05'
            start_date=str(year)+'-0'+str(month-1)+'-'+'26'
        elif (month==9) or (month==10):
            pay_date=str(year)+'-'+str(month+1)+'-'+'05'
            start_date=str(year)+'-0'+str(month-1)+'-'+'26'
        else:
            pay_date=str(year)+'-'+str(month+1)+'-'+'05'
            start_date=str(year)+'-'+str(month-1)+'-'+'26'
            
        
        
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute("select * from trans where cardno=? and trans_date between ? and ?",(cardno,start_date,bill_date))
    transactions=cursor.fetchall()
    
    cursor.execute("select sum(amount) from trans where cardno=? and trans_date between ? and ?",(cardno,start_date,bill_date))
    trans_tot=cursor.fetchall()[0][0]

    cursor.execute("select sum(trans_tot),sum(balance) from bill where cardno = ? and status ='Unpaid'",(cardno, ))
    pay_data = cursor.fetchall()
    unpaid_trans_tot=pay_data[0][0]
    
    bal=pay_data[0][1]
    
    if trans_tot is None:
        trans_tot=0
    if unpaid_trans_tot is None:
        unpaid_trans_tot=0
    if bal is None:
        bal=0
        
    fine = unpaid_trans_tot * 0.035
    bill_amount = trans_tot + fine + bal

    val=[cardno, bill_date, pay_date, trans_tot, fine, bill_amount, bill_amount,0,'Unpaid']
    check_and_insert_element(bill_date,val)


def check_and_insert_element(bill_date,val):
        # Connect to the database
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        # Check if the element exists
        cursor.execute("SELECT * FROM bill WHERE bill_date = ?", (bill_date,))
        existing_row = cursor.fetchone()

        if existing_row is None:
            # If no rows are returned, insert the new element
            cursor.execute("INSERT INTO bill ( cardno, bill_date, pay_date, trans_tot, fine, bill_amount, balance,paid_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",val)

        # Commit changes and close connection
        conn.commit()
        conn.close()
def show_bill(cardno,month,year):
    #year=int(input("Year:"))
    #month=int(input("Month:"))
    #bill_date=str(year)+'-'+str(month)+'-'+'25'
    
    if month==12:
        bill_date=str(year)+'-'+str(month)+'-'+'25'
        pay_date=str(year+1)+'-'+str('01')+'-'+'25'
        start_date=str(year)+'-'+str(month-1)+'-'+'26'
    elif month==1:
        bill_date=str(year)+'-0'+str(month)+'-'+'25'
        pay_date=str(year)+'-0'+str(month+1)+'-'+'05'
        start_date=str(year-1)+'-'+'12'+'-'+'26'
    else:
        if month<9:
            bill_date=str(year)+'-0'+str(month)+'-'+'25'
            pay_date=str(year)+'-0'+str(month+1)+'-'+'05'
            start_date=str(year)+'-0'+str(month-1)+'-'+'26'
        elif (month==9) or (month==10):
            if month==9:
                bill_date=str(year)+'-0'+str(month)+'-'+'25'
            else:
                bill_date=str(year)+'-'+str(month)+'-'+'25'
            pay_date=str(year)+'-'+str(month+1)+'-'+'05'
            start_date=str(year)+'-0'+str(month-1)+'-'+'26'
        else:
            bill_date=str(year)+'-'+str(month)+'-'+'25'
            pay_date=str(year)+'-'+str(month+1)+'-'+'05'
            start_date=str(year)+'-'+str(month-1)+'-'+'26'
    # Connect to the database
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute("select * from trans where cardno=? and trans_date between ? and ?",(cardno,start_date,bill_date))
    #cursor.execute("select * from trans")
    transactions=cursor.fetchall()
    
    # Check if the element exists
    #cursor.execute("SELECT * FROM bill WHERE bill_date = ? and cardno= ?", (bill_date,cardno,))
    cursor.execute("SELECT * FROM bill WHERE cardno= ?", (cardno,))
    existing_row = cursor.fetchone()
    
    

    if existing_row is None:
        messagebox.showinfo("Error", "Bill does not exist!")
    else:
        
        #val=[bill_no,cardno,bill_date, pay_date, trans_tot, fine, bill_amount, bill_amount,paid_amount, status]
        pay_date=existing_row[2]
        trans_tot=existing_row[4]
        fine=existing_row[5]
        bill_amount=existing_row[6]
        balance=existing_row[7]
        paid=existing_row[8]
        status=existing_row[9]
        # Create a Tkinter window
        #print(existing_row)
        
        window = tk.Tk()
        window.title(f"Transactions for Card No {cardno}")
        labeldate = tk.Label(window, text="Bill Date: "+bill_date)
        labeldate.pack()
        label_pay_date = tk.Label(window, text="Pay Date: "+pay_date)
        label_pay_date.pack()
        # Create a treeview widget to display transactions
        tree = ttk.Treeview(window, columns=("Date", "Description", "Amount", "Cardno"))
        tree.heading("#0", text="ID")
        tree.heading("Amount", text="Amount")
        tree.heading("Description", text="Description")
        tree.heading("Date", text="Date")
        tree.heading("Cardno", text="Card Number")

        # Insert transactions into the treeview
        for transaction in transactions:
            tree.insert("", "end", text=transaction[0], values=(transaction[4], transaction[1], transaction[2], transaction[3]))

        tree.pack(expand=True, fill=tk.BOTH)
        label_trans_tot = tk.Label(window, text="Transaction Total: "+str(trans_tot))
        label_trans_tot.pack()
        label_fine = tk.Label(window, text="Fine: "+str(fine))
        label_fine.pack()
        label_bill_amount = tk.Label(window, text="Bill Amount: "+str(bill_amount))
        label_bill_amount.pack()
        label_bal = tk.Label(window, text="Balance: "+str(balance))
        label_bal.pack()
        label_paid = tk.Label(window, text="Paid: "+str(paid))
        label_paid.pack()
        
        
    # Commit changes and close connection
    conn.commit()
    conn.close()

login()
