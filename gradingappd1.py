import tkinter as tk
from tkinter import ttk
import sqlite3

# Global Variables
userId = 0

# Connect to or create Database
conn = sqlite3.connect('gradesdatabase.db')
if conn:
    print("Opened database successfully")


# Create the Users table if it does not exist
def createUserTable():
    try:
        conn.execute("CREATE TABLE USERS \
                 (ID            INTEGER     PRIMARY KEY AUTOINCREMENT, \
                 USERNAME       TEXT    NOT NULL UNIQUE, \
                 PASSWORD       TEXT    NOT NULL); ")
        print("Table created successfully")
    except:
        print("User table exists")


# Create the Transactions table if it does not exist
def createTransTable():
    try:
        conn.execute("CREATE TABLE TRANSACTIONS \
                    (USER_ID INTEGER, \
                    TRANS_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    AMOUNT DECIMAL, \
                    CATEGORY TEXT, \
                    TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    FOREIGN KEY (USER_ID) REFERENCES USERS(ID)); ")
        print("Table created successfully")
    except:
        print("Transaction table exists")

# Create the Transactions table if it does not exist
def createTransTable():
    try:
        conn.execute("CREATE TABLE TRANSACTIONS \
                    (USER_ID INTEGER, \
                    TRANS_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    AMOUNT DECIMAL, \
                    CATEGORY TEXT, \
                    TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    FOREIGN KEY (USER_ID) REFERENCES USERS(ID)); ")
        print("Table created successfully")
    except:
        print("Transaction table exists")

# Create the Grades table if it does not exist
def createGradesTable():
    try:
        conn.execute("CREATE TABLE GRADES \
                    (USER_ID INTEGER, \
                    RECORD_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    STUDENT TEXT, \
                    GRADE INTEGER, \
                    COURSE TEXT, \
                    TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    FOREIGN KEY (USER_ID) REFERENCES USERS(ID)); ")
        print("Table created successfully")
    except:
        print("Grades table exists")


# Try to create tables
createUserTable()
createTransTable()
createGradesTable()


# Database Functions
def insertRecord(inpStr):
    conn.execute(f"{inpStr}")
    conn.commit()


def deleteRecord(inpStr):
    conn.execute(f"{inpStr}")
    conn.commit()


def updateRecord(inpStr):
    conn.execute(f"{inpStr}")
    conn.commit()


def getRecords(inpStr):
    cur = conn.cursor()
    cur.execute(f"{inpStr}")

    rows = cur.fetchall()
    print(rows)
    return rows


def getFirstRecord(inpStr):
    cur = conn.cursor()
    cur.execute(f"{inpStr}")

    rows = cur.fetchall()
    print(rows)
    for row in rows:
        return row[0]


LARGE_FONT = ("Verdana", 20)


# Create the main class and define show frame functions
class MyExpenses(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, MainPage, RegistrationPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login Page
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Checks whether username and password are correct
        def checkPassword():
            # Check if user exists in database
            username = usernameEntry.get()
            password = passwordEntry.get()
            print(username, password)

            if getFirstRecord(f"SELECT ID FROM USERS WHERE USERNAME = '{username}' AND PASSWORD = '{password}'"):
                return True
            else:
                return False

        # Prints whether login is successful or not to the app
        def sucUnsuc():
            if checkPassword():
                # If authenticated
                username = usernameEntry.get()
                global userId
                userId = getFirstRecord(f"Select id from users where username = '{username}'")
                usernameEntry.delete(0, 'end')
                passwordEntry.delete(0, 'end')
                label1 = tk.Label(self, text=" ", width=30)
                canvas1.create_window(200, 250, window=label1)
                controller.show_frame(MainPage)
            else:
                # If authentication fails
                label1 = tk.Label(self, text="Invalid credentials!")
                canvas1.create_window(200, 250, window=label1)

        # Login Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=400)
        canvas1.pack()

        # Username
        usernameLabel = tk.Label(self, text="Username")
        canvas1.create_window(100, 100, window=usernameLabel)
        usernameEntry = tk.Entry(self)
        canvas1.create_window(250, 100, window=usernameEntry)

        # Password
        passwordLabel = tk.Label(self, text="Password")
        canvas1.create_window(100, 150, window=passwordLabel)
        passwordEntry = tk.Entry(self, show="*")
        canvas1.create_window(250, 150, window=passwordEntry)

        # Login button
        loginButton = tk.Button(self, width=15, text="Login", command=sucUnsuc)
        canvas1.create_window(260, 200, window=loginButton)

        # Register button
        registerButton = tk.Button(self, width=15, text="Register", command=lambda: controller.show_frame(RegistrationPage))
        canvas1.create_window(100, 200, window=registerButton)


class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def displayMsg(inpStr):
            label2 = tk.Label(self, text=inpStr)
            canvas1.create_window(200, 300, window=label2)

        # Checks whether username exists and passwords match
        def regCheckPassword():
            username = usernameEntry.get()
            password = passwordEntry.get()
            conPassword = passwordConEntry.get()
            print(username, password, conPassword)

            if not username or not password or not conPassword:
                displayMsg("All fields are mandatory!")
                return 1
            elif getFirstRecord(f"SELECT ID FROM USERS WHERE USERNAME = '{username}'"):
                displayMsg("Username is taken!")
                return 2
            elif password != conPassword:
                displayMsg("Password and Confirm Password do not match!")
                return 3
            else:
                return 0

        # Prints whether registration is successful or not to the app
        def regSucUnsuc():
            username = usernameEntry.get()
            password = passwordEntry.get()
            if regCheckPassword() == 0:
                # Initialize records in both tables
                insertRecord(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('{username}', '{password}')")
                newId = getFirstRecord(f"Select id from users where username = '{username}'")
                insertRecord(
                    f"INSERT INTO TRANSACTIONS(USER_ID, AMOUNT, CATEGORY) VALUES({newId}, 0, 'Other')")

                # Clear the form
                usernameEntry.delete(0, 'end')
                passwordEntry.delete(0, 'end')
                passwordConEntry.delete(0, 'end')
                displayMsg(" ")
                # label1 = tk.Label(self, text=" ", width=50)
                # canvas1.create_window(200, 300, window=label1)

                # Go back to login Page
                controller.show_frame(LoginPage)

        # Registration Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=300)
        canvas1.pack()

        # Username
        usernameLabel = tk.Label(self, text="Username")
        canvas1.create_window(100, 100, window=usernameLabel)
        usernameEntry = tk.Entry(self)
        canvas1.create_window(250, 100, window=usernameEntry)

        # Password
        passwordLabel = tk.Label(self, text="Password")
        canvas1.create_window(100, 150, window=passwordLabel)
        passwordEntry = tk.Entry(self, show="*")
        canvas1.create_window(250, 150, window=passwordEntry)

        # Confirm Password
        passwordConLabel = tk.Label(self, text="Confirm Password")
        canvas1.create_window(100, 200, window=passwordConLabel)
        passwordConEntry = tk.Entry(self, show="*")
        canvas1.create_window(250, 200, window=passwordConEntry)

        # Register button
        registerButton = tk.Button(self, width=15, text="Register", command=regSucUnsuc)
        canvas1.create_window(260, 250, window=registerButton)

        # Back button
        backButton = tk.Button(self, width=15, text="Back", command=lambda: controller.show_frame(LoginPage))
        canvas1.create_window(100, 250, window=backButton)


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def displayMsg(inpStr):
            label2 = tk.Label(self, text=" ", width=20)
            canvas1.create_window(200, 200, window=label2)
            label2 = tk.Label(self, text=inpStr)
            canvas1.create_window(200, 200, window=label2)

        # Check whether all entries in the form are valid
        def checkForm():
            amount = amountEntry.get()
            category = menu.get()
            plusOrMinus = hwOrTest.get()
            print(amount, category, plusOrMinus)

            try:
                amount = float(amount)
            except:
                displayMsg("Invalid Amount!")
                return 2

            if not plusOrMinus or amount == 0 or category == "Select a Category":
                displayMsg("A required field is empty!")
                return 1
            else:
                return 0

        def submitForm():
            if checkForm() == 0:
                # Get all the required variables
                amount = float(amountEntry.get())
                category = menu.get()
                plusOrMinus = hwOrTest.get()
                print(userId, amount, category, plusOrMinus)
                print("Recording transaction to wallet...")
                if plusOrMinus == 1:
                    # Adding
                    print(userId, amount, category, plusOrMinus)
                    foo = f"INSERT INTO TRANSACTIONS (USER_ID, AMOUNT, CATEGORY) VALUES ({userId}, {amount}, '{category}')"
                else:
                    # Subtracting
                    print(userId, amount, category, plusOrMinus)
                    foo = f"INSERT INTO TRANSACTIONS (USER_ID, AMOUNT, CATEGORY) VALUES ({userId}, -{amount}, '{category}')"
                print(foo)
                insertRecord(foo)
                displayMsg("Recorded Successfully")
                updateBalance()
                View()

        def updateIt():
            try:
                selected = tree.focus()
                values = tree.item(selected, 'values')
                print(values[0])
                tId = values[0]
                if checkForm() == 0:
                    # Get all the required variables
                    amount = float(amountEntry.get())
                    category = menu.get()
                    plusOrMinus = hwOrTest.get()
                    print(userId, amount, category, plusOrMinus)

                    print("Updating transaction...")
                    if plusOrMinus == 1:
                        # Adding
                        print(userId, amount, category, plusOrMinus)
                        # foo = f"INSERT INTO TRANSACTIONS (USER_ID, AMOUNT, CATEGORY) VALUES ({userId}, {amount}, '{category}')"
                        foo = f"UPDATE TRANSACTIONS SET AMOUNT = {amount}, CATEGORY = '{category}' WHERE TRANS_ID = {tId}"
                    else:
                        # Subtracting
                        print(userId, amount, category, plusOrMinus)
                        # foo = f"INSERT INTO TRANSACTIONS (USER_ID, AMOUNT, CATEGORY) VALUES ({userId}, -{amount}, '{category}')"
                        foo = f"UPDATE TRANSACTIONS SET AMOUNT = -{amount}, CATEGORY = '{category}' WHERE TRANS_ID = {tId}"
                    print(foo)
                    updateRecord(foo)
                    displayMsg("Updated Successfully")
                    updateBalance()
                    View()
            except:
                displayMsg("Please select a row")

        def updateBalance():
            balance = round(getFirstRecord(f"SELECT SUM(AMOUNT) FROM TRANSACTIONS WHERE USER_ID = {userId}"), 2)
            balanceLabel = tk.Label(self, text=f"Balance:\n$ {balance}", width=20, font=LARGE_FONT)
            canvas1.create_window(450, 100, window=balanceLabel)

        def logMeOut():
            # Clear all displayed data and go to Login Page
            global userId
            userId = 0
            for row in tree.get_children():
                tree.delete(row)
            amountEntry.delete(0, 'end')
            displayMsg(" ")
            clearBalanceLabel = tk.Label(self, text=" ", width=20, height=4)
            canvas1.create_window(450, 100, window=clearBalanceLabel)
            controller.show_frame(LoginPage)

        # Main Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=300)
        canvas1.pack()

        # Amount
        amountLabel = tk.Label(self, text="Grade", width=20)
        canvas1.create_window(50, 100, window=amountLabel)
        amountEntry = tk.Entry(self, width=24)
        canvas1.create_window(200, 100, window=amountEntry)

        # Add or spend money
        hwOrTest = tk.IntVar()
        addButton = tk.Radiobutton(self, text="Homework", variable=hwOrTest, value=1)
        canvas1.create_window(125, 50, window=addButton)
        addButton = tk.Radiobutton(self, text="Test", variable=hwOrTest, value=2)
        canvas1.create_window(250, 50, window=addButton)


        # Category
        # Set the Menu initially
        menu = tk.StringVar()
        menu.set("Select a Category")

        # Create a dropdown Menu

        drop = tk.OptionMenu(self, menu, "Personal", "Travel", "Food", "Other")
        drop.configure(width=20)
        canvas1.create_window(200, 150, window=drop)

        # Confirm button
        confirmButton = tk.Button(self, width=20, text="Confirm", command=submitForm)
        canvas1.create_window(0, 200, window=confirmButton)

        # Logout button
        logoutButton = tk.Button(self, width=20, text="Logout", command=logMeOut)
        canvas1.create_window(400, 200, window=logoutButton)

        # Table
        def View():
            updateBalance()

            for row in tree.get_children():
                tree.delete(row)

            for row in reversed(getRecords(
                    f"Select TRANS_ID, amount, category, timestamp from transactions where user_Id = {userId}")):
                tree.insert("", tk.END, values=row)

        def delIt():
            try:
                selected = tree.focus()
                values = tree.item(selected, 'values')
                print(values[0])
                tId = values[0]
                deleteRecord(f"DELETE FROM TRANSACTIONS WHERE TRANS_ID = {tId}")
                updateBalance()
                View()
                displayMsg("Deleted Successfully")
            except:
                displayMsg("Please select a row")

        dispData = tk.Button(self, width=20, text="Display data", command=View)
        canvas1.create_window(200, 250, window=dispData)

        deleteButton = tk.Button(self, width=20, text="Delete entry", command=delIt)
        canvas1.create_window(400, 250, window=deleteButton)

        updateButton = tk.Button(self, width=20, text="Update entry", command=updateIt)
        canvas1.create_window(0, 250, window=updateButton)

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings')

        tree.column("#1", anchor=tk.CENTER, width=150)
        tree.heading("#1", text="ID")

        tree.column("#2", anchor=tk.CENTER, width=150)
        tree.heading("#2", text="Amount")

        tree.column("#3", anchor=tk.CENTER, width=150)
        tree.heading("#3", text="Category")

        tree.column("#4", anchor=tk.CENTER, width=200)
        tree.heading("#4", text="Timestamp")
        tree.pack()


# Create Window and display
app = MyExpenses()
app.title("Digital Wallet")
app.geometry("800x600")
app.mainloop()