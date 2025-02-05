import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3

# Global Variables
userId = 0
LARGE_FONT = ("Verdana", 20)

class Student:
    def __init__(self, name, rocketid):
        self.id = rocketid
        self.name = name

    def __repr__(self):  
        return (f"Student name: {self.name}")
    
    def __str__(self):  
        return (f"Student name: {self.name}")
    
class Assignment:
    def __init__(self, assignmentId, name, type):
        self.assignmentId = assignmentId
        self.name = name
        self.type = type

    def __repr__(self):  
        return (f"Assignment name: {self.name}")
    
    def __str__(self):  
        return (f"Assignment name: {self.name}")

class Course:
    def __init__(self, name):
        self.name = name
        self.students = []
        self.assignments = []
        self.homeworks = []
        self.tests = []

    def add_student(self, student):
        self.students.append(student)
        g1.modifyRecord(f"INSERT INTO STUDENTS (COURSE, STUDENT_ID, STUDENT_NAME) VALUES ('{self.name}', '{student.id}', '{student.name}')")

    def remove_student(self, student):
        self.students.remove(student)
        g1.modifyRecord(f"DELETE FROM STUDENTS WHERE COURSE = '{self.name}' AND STUDENT_NAME = '{student.name}'")

    def add_assignment(self, assignment):
        self.assignments.append(assignment)
        g1.modifyRecord(f"INSERT INTO ASSIGNMENTS (COURSE, ASSIGNMENT_NAME, ASSIGNMENT_TYPE) VALUES ('{self.name}', '{assignment.name}', '{assignment.type}')")
        if assignment.type == "HW":
            self.homeworks.append(assignment)
        if assignment.type == "TEST":
            self.tests.append(assignment)


    def remove_assignment(self, assignment):
        self.assignments.remove(assignment)
        g1.modifyRecord(f"DELETE FROM ASSIGNMENTS WHERE COURSE = '{self.name}' AND ASSIGNMENT_NAME = '{assignment.name}'")
        g1.modifyRecord(f"DELETE FROM SCORES WHERE COURSE = '{self.name}' AND ASSIGNMENT_NAME = '{assignment.name}'")
        

    def __repr__(self):  
        return (f"Course name: {self.name}")
    
    def __str__(self):  
        return (f"Course name: {self.name}")
    
class GradeManager:
    def __init__(self):
        self.courses = []
        self.selectedCourse = Course

    # Create the Users table if it does not exist
    def createUserTable(self):
        try:
            conn.execute("CREATE TABLE USERS \
                    (ID            INTEGER     PRIMARY KEY AUTOINCREMENT, \
                    USERNAME       TEXT    NOT NULL UNIQUE, \
                    PASSWORD       TEXT    NOT NULL); ")
            print("Table created successfully")
        except:
            print("User table exists")

    # Create the Students table if it does not exist
    def createStudentsTable(self):
        try:
            conn.execute("CREATE TABLE STUDENTS \
                    (ID            INTEGER     PRIMARY KEY AUTOINCREMENT, \
                    COURSE       TEXT    NOT NULL, \
                    STUDENT_ID     TEXT    NOT NULL, \
                    STUDENT_NAME       TEXT    NOT NULL); ")
            print("Table created successfully")
        except:
            print("Students table exists")

    # Create the Assignments table if it does not exist
    def createAssignmentsTable(self):
        try:
            conn.execute("CREATE TABLE ASSIGNMENTS \
                    (ID            INTEGER     PRIMARY KEY AUTOINCREMENT, \
                    COURSE       TEXT    NOT NULL, \
                    ASSIGNMENT_NAME     TEXT    NOT NULL, \
                    ASSIGNMENT_TYPE     TEXT    NOT NULL); ")
            print("Table created successfully")
        except:
            print("Assignments table exists")

    # Create the Grades table if it does not exist
    def createScoresTable(self):
        try:
            conn.execute("CREATE TABLE SCORES \
                        (USER_ID INTEGER, \
                        RECORD_ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                        COURSE TEXT, \
                        STUDENT_ID TEXT, \
                        STUDENT_NAME TEXT, \
                        ASSIGNMENT_NAME TEXT, \
                        ASSIGNMENT_TYPE TEXT, \
                        SCORE INTEGER, \
                        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, \
                        FOREIGN KEY (USER_ID) REFERENCES USERS(ID)); ")
            print("Table created successfully")
        except:
            print("Grades table exists")
    
    # Initialization
    def initialize(self):
        # Scans grades table, adds courses, students, and assignments found.
        courses = g1.getRecords(
            f"Select username from users")
        print(courses)
        for crs in courses:
            g1.courses.append(Course(crs[0].upper()))

        students = g1.getRecords(
            f"Select * from students")
        print(students)
        for st in students:
            cr = g1.get_objects(st[1], "", "")
            sto = Student(st[3], st[2])
            cr[0].students.append(sto)

        assignments = g1.getRecords(
            f"Select * from assignments")
        print(assignments)
        for assi in assignments:
            cr = g1.get_objects(assi[1], "", "")
            assign = Assignment("", assi[2], assi[3])
            cr[0].assignments.append(assign)


    # Database Functions
    def modifyRecord(self, inpStr):
        conn.execute(f"{inpStr}")
        conn.commit()

    def getRecords(self, inpStr):
        cur = conn.cursor()
        cur.execute(f"{inpStr}")

        rows = cur.fetchall()
        print(rows)
        return rows

    def getFirstRecord(self, inpStr):
        cur = conn.cursor()
        cur.execute(f"{inpStr}")

        rows = cur.fetchall()
        print(rows)
        for row in rows:
            return row[0]
        
    def get_objects(self, course_name, student_name, assignment_name):
        course_name, student_name, assignment_name = course_name.upper(), student_name.upper(), assignment_name.upper()
        g1.selectedCourse = next((course for course in g1.courses if course.name == course_name), None)

        student = next((student for student in g1.selectedCourse.students if student.name == student_name), None)
        assignment = next((assignment for assignment in g1.selectedCourse.assignments if assignment.name == assignment_name), None)
        print(g1.selectedCourse, student, assignment)
        return [g1.selectedCourse, student, assignment]

    def grade_assignment(self, course_name, student_name, assignment_name, score):
        course, student, assignment = g1.get_objects(course_name, student_name, assignment_name)
        print(course.name, student.id ,student.name, assignment.name, assignment.type, score)
                        
        g1.modifyRecord(f"INSERT INTO SCORES (COURSE, STUDENT_ID, STUDENT_NAME, ASSIGNMENT_NAME, ASSIGNMENT_TYPE, SCORE ) VALUES ('{course.name}', '{student.id}', '{student.name}', '{assignment.name}', '{assignment.type}', {score})")


    def calculate_grade(self, course_name, student_name):
        objs = g1.get_objects(course_name, student_name, "")
        course = objs[0]
        print(course.homeworks, course.tests)
        hw_total = 0
        
        test_total = 0
        
        overall_grade_percentage = 0

        hw_scores = g1.getRecords(f"SELECT SCORE FROM SCORES WHERE COURSE = '{course_name}' AND STUDENT_NAME = '{student_name}' AND ASSIGNMENT_TYPE = 'HW'")
        total_hws = len(hw_scores) * 100
        test_scores = g1.getRecords(f"SELECT SCORE FROM SCORES WHERE COURSE = '{course_name}' AND STUDENT_NAME = '{student_name}' AND ASSIGNMENT_TYPE = 'TEST'")
        total_tests = len(test_scores) * 100
        hw_per = 0
        test_per = 0

        for hwscore in hw_scores:
            hw_total += hwscore[0]
        for tscore in test_scores:
            test_total += tscore[0]
        print(hw_total, test_total)

        if len(hw_scores) == 0 and len(test_scores) == 0:
            hw_per = None
            test_per = None
            overall_grade_percentage = 0
        elif len(hw_scores) == 0:
            hw_per = None
            test_per = (test_total / total_tests) * 100
            overall_grade_percentage = (test_total / total_tests)
        elif len(test_scores) == 0:
            hw_per = hw_total / total_hws * 100
            test_per = None
            overall_grade_percentage = (hw_total / total_hws) * 100
        else:
            overall_grade_percentage = ((hw_total / total_hws) * 0.3 + (test_total / total_tests) * 0.7) * 100
            hw_per = hw_total / total_hws * 100
            test_per = test_total / total_tests * 100
            print((hw_total / total_hws), (test_total / total_tests))
            


        if overall_grade_percentage >= 90:
            letter_grade = "A"
        elif overall_grade_percentage >= 80:
            letter_grade = "B"
        elif overall_grade_percentage >= 70:
            letter_grade = "C"
        elif overall_grade_percentage >= 60:
            letter_grade = "D"
        else:
            letter_grade = "F"

        print ("Grades", student_name, hw_per, test_per, overall_grade_percentage, letter_grade)
        return student_name, hw_per, test_per, overall_grade_percentage, letter_grade
        
            


    def calculate_overall_grade(self, course):
        courseGrades = []
        for student in course.students:
            courseGrades.append(g1.calculate_grade(course.name, student.name))
        return courseGrades



# Create the main class and define show frame functions
class MyGrades(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, MainPage, RegistrationPage, GradesPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


# Login Page
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Checks whether username and password are correct
        def checkPassword():
            # Check if user exists in database
            username = usernameEntry.get().upper()
            password = passwordEntry.get()
            print(username, password)

            if g1.getFirstRecord(f"SELECT ID FROM USERS WHERE USERNAME = '{username}' AND PASSWORD = '{password}'"):
                return True
            else:
                return False

        # Prints whether login is successful or not to the app
        def sucUnsuc():
            if checkPassword():
                # If authenticated
                username = usernameEntry.get()
                global userId
                userId = g1.getFirstRecord(f"Select id from users where username = '{username}'")
                g1.selectedCourse = g1.get_objects(username, "","")[0]
                print(g1.selectedCourse)
                usernameEntry.delete(0, 'end')
                passwordEntry.delete(0, 'end')
                label1 = tk.Label(self, text=" ", width=30)
                canvas1.create_window(200, 250, window=label1)
                View()
                controller.show_frame(MainPage)
            else:
                # If authentication fails
                label1 = tk.Label(self, text="Invalid credentials!")
                canvas1.create_window(200, 250, window=label1)

        # Login Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=400)
        canvas1.pack()

        # Username
        usernameLabel = tk.Label(self, text="Course Name")
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

# Registration Page
class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def alertMsg(inpStr):
            messagebox.showerror("Error", inpStr)
            # label2 = tk.Label(self, text=inpStr)
            # canvas1.create_window(200, 300, window=label2)

        # Checks whether username exists and passwords match
        def regCheckPassword():
            username = usernameEntry.get()
            password = passwordEntry.get()
            conPassword = passwordConEntry.get()
            print(username, password, conPassword)

            if not username or not password or not conPassword:
                alertMsg("All fields are mandatory!")
                return 1
            elif not username.isalnum():
                alertMsg("Course Name must be Alphanumeric")
                return 2
            elif g1.getFirstRecord(f"SELECT ID FROM USERS WHERE USERNAME = '{username.upper()}'"):
                alertMsg("Course Name is taken!")
                return 2
            elif password != conPassword:
                alertMsg("Password and Confirm Password do not match!")
                return 3
            else:
                return 0

        # Prints whether registration is successful or not to the app
        def regSucUnsuc():
            username = usernameEntry.get().upper()
            password = passwordEntry.get()
            if regCheckPassword() == 0:
                # Initialize records in both tables
                g1.modifyRecord(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('{username}', '{password}')")
                newId = g1.getFirstRecord(f"Select id from users where username = '{username}'")
                # g1.modifyRecord(
                #     f"INSERT INTO SCORES(USER_ID, COURSE) VALUES({newId}, '{username}')")
                
                # Add course to courses
                g1.courses.append(Course(username))
                print(g1.courses)

                # Clear the form
                usernameEntry.delete(0, 'end')
                passwordEntry.delete(0, 'end')
                passwordConEntry.delete(0, 'end')

                # Go back to login Page
                controller.show_frame(LoginPage)

        # Registration Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=300)
        canvas1.pack()

        # Username
        usernameLabel = tk.Label(self, text="Course Name")
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

# Main Page
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        
        # Table
        global View
        def View():
            print("Building Tree...")
            print(g1.selectedCourse)

            for row in student_tree.get_children():
                student_tree.delete(row)

            for student in g1.selectedCourse.students:
                student_tree.insert(parent = '', index='end', values= student.name)

            for row in assignment_tree.get_children():
                assignment_tree.delete(row)

            for assignment in g1.selectedCourse.assignments:
                assignment_tree.insert(parent = '', index='end', values= (assignment.name, assignment.type))
        
        def clearView():
            for row in student_tree.get_children():
                student_tree.delete(row)
            for row in assignment_tree.get_children():
                assignment_tree.delete(row) 
            scoreEntry.delete(0, 'end')

        def alertMsg(myString):
            messagebox.showerror("Alert", myString) 
            print(myString)

        # Check whether all entries in the form are valid
        def checkForm():
            selected_student = student_tree.item(student_tree.focus(), 'values')
            selected_assignment = assignment_tree.item(assignment_tree.focus(), 'values')
            score = scoreEntry.get()
            if not selected_student:
                alertMsg("Please select a student")
                return 1
            elif not selected_assignment:
                alertMsg("Please select an Assignment")
                return 1

            try:
                score = int(score)
                if score < 0 or score > 100:
                    alertMsg("Invalid Score!")
                    return 1
                else: 
                    print(selected_student, selected_assignment, score)
                    return 0
            except:
                alertMsg("Invalid Score!")
                return 1
   
                
        def submitForm():
            if checkForm() == 0:
                student_name = student_tree.item(student_tree.focus(), 'values')[0]
                assignment_name = assignment_tree.item(assignment_tree.focus(), 'values')[0]
                score = scoreEntry.get()
                print(student_name, assignment_name, score)
                print("Submitted successfully")

                existing = g1.getFirstRecord(
                    f"Select record_id from scores where course = '{g1.selectedCourse.name}' AND STUDENT_NAME = '{student_name}'AND ASSIGNMENT_NAME = '{assignment_name}'")
                print(existing)
                
                if not existing:
                    g1.grade_assignment(g1.selectedCourse.name, student_name, assignment_name, score)
                    select_item(0)
                else:
                    print("Record exists")
                    res = messagebox.askyesno("Modify?", "Record Exists. Do you wish to modify it?")
                    print(res)
                    if res:
                        g1.modifyRecord(f"UPDATE SCORES SET SCORE = {score} WHERE COURSE = '{g1.selectedCourse.name}' AND STUDENT_NAME = '{student_name}' AND ASSIGNMENT_NAME = '{assignment_name}'")
                        View()
                

        def logMeOut():
            # Clear all displayed data and go to Login Page
            clearView()
            controller.show_frame(LoginPage)

        def delScore():
            selected_student = student_tree.item(student_tree.focus(), 'values')
            selected_assignment = assignment_tree.item(assignment_tree.focus(), 'values')

            if not selected_student:
                alertMsg("Please select a student")
                return 1
            elif not selected_assignment:
                alertMsg("Please select an Assignment")
                return 1
            else:
                print(selected_student, selected_assignment)
                if selected_assignment[2] == 'None':
                    print("Record does not exist")
                    return 1
                else:                
                    g1.modifyRecord(f"DELETE FROM SCORES WHERE COURSE = '{g1.selectedCourse.name}' AND STUDENT_NAME = '{selected_student[0]}' AND ASSIGNMENT_NAME = '{selected_assignment[0]}'")
                    select_item(0)

        def calcGrade():
            # Clear all displayed data and go to Login Page
            dispGrades()
            controller.show_frame(GradesPage)

        


        def get_student_info():
            student_window = tk.Toplevel(self)
            student_window.title("Student Information")
            student_window.geometry("400x200")

            canvas = tk.Canvas(student_window, width=200, height=150)
            canvas.pack()

            label_id = tk.Label(student_window, text="Student ID:")
            canvas.create_window(25, 30, window=label_id)
            entry_id = tk.Entry(student_window)
            canvas.create_window(150, 30, window=entry_id)

            label_name = tk.Label(student_window, text="Student Name:")
            canvas.create_window(25, 60, window=label_name)
            entry_name = tk.Entry(student_window)
            canvas.create_window(150, 60, window=entry_name)

            def submitstu():
                try:
                    student_id = entry_id.get()
                    student_name = entry_name.get().upper()
                    if student_id.isalnum() and student_name.isalpha():
                        print("Student ID:", student_id)
                        print("Student Name:", student_name)
                        existing_students = []
                        for st_name in g1.selectedCourse.students:
                            existing_students.append(st_name.name)
                        print(existing_students)

                        if student_name not in existing_students:
                            st = Student (student_name, student_id)
                            course = g1.get_objects(g1.selectedCourse.name, "", "")
                            course[0].add_student(st)
                            student_window.destroy()
                            View()
                        else:
                            error_label = tk.Label(student_window, text="Student Already Exists", fg="red")
                            canvas.create_window(100, 150, window=error_label)
                    else:
                        error_label = tk.Label(student_window, text="                  Invalid Entries                 ", fg="red")
                        canvas.create_window(100, 150, window=error_label)
                except:
                    print("Invalid entries exception")
                    error_label = tk.Label(student_window, text="Invalid Entries", fg="red")
                    canvas.create_window(100, 150, window=error_label)

            submit_button = tk.Button(student_window, text="Submit", command=submitstu)
            canvas.create_window(100, 100, window=submit_button)


        def get_assignment_info():
            student_window = tk.Toplevel(self)
            student_window.title("Assignment Information")
            student_window.geometry("400x200")

            canvas = tk.Canvas(student_window, width=200, height=300)
            canvas.pack()

            label_name = tk.Label(student_window, text="Assignment Name:")
            canvas.create_window(25, 30, window=label_name)
            entry_name = tk.Entry(student_window)
            canvas.create_window(150, 30, window=entry_name)

            # Radio buttons
            var = tk.StringVar()
   
            radio_hw = tk.Radiobutton(student_window, text="HW", variable=var, value="HW")
            canvas.create_window(50, 90,  window=radio_hw)
            radio_test = tk.Radiobutton(student_window, text="TEST", variable=var, value="TEST")
            canvas.create_window(200, 90, window=radio_test)



            def submitassi():
                try:
                    assignment_name = entry_name.get().upper()
                    assign_type = "HW"
                    if assignment_name.isalnum() and var.get():
                        print("Assign Name:", assignment_name)
                        assign_type = var.get()
                        existing_assignments = []
                        for as_name in g1.selectedCourse.assignments:
                            existing_assignments.append(as_name.name)
                        print(existing_assignments)

                        if assignment_name not in existing_assignments:
                            assi = Assignment ("", assignment_name, assign_type)
                            course = g1.get_objects(g1.selectedCourse.name, "", "")
                            course[0].add_assignment(assi)
                            student_window.destroy()
                            View()
                        else:
                            error_label = tk.Label(student_window, text="Assignment Already Exists", fg="red")
                            canvas.create_window(100, 170, window=error_label)
                    else:
                        error_label = tk.Label(student_window, text="                  Invalid Entries                 ", fg="red")
                        canvas.create_window(100, 170, window=error_label)
                except:
                    print("Invalid entries exception")
                    error_label = tk.Label(student_window, text="             Invalid Entries ex         ", fg="red")
                    canvas.create_window(100, 170, window=error_label)

            submit_button = tk.Button(student_window, text="Submit", command=submitassi)
            canvas.create_window(100, 140, window=submit_button)




        def delAssignment():
            selected_assignment = assignment_tree.item(assignment_tree.focus(), 'values')
            if not selected_assignment:
                alertMsg("Select an assignment")
                return 1
            print(selected_assignment)
            objs = g1.get_objects(g1.selectedCourse.name, "", selected_assignment[0])
            objs[0].remove_assignment(objs[2])
            View()

        def select_item(a):
            course_name = g1.selectedCourse.name
            student_name = student_tree.item(student_tree.focus(), 'values')[0]
            for row in assignment_tree.get_children():
                assignment_tree.delete(row)

            for assignment in g1.selectedCourse.assignments:
                score = g1.getFirstRecord(f"SELECT SCORE FROM SCORES WHERE COURSE = '{course_name}' AND STUDENT_NAME = '{student_name}' AND ASSIGNMENT_NAME = '{assignment.name}'")
                assignment_tree.insert(parent = '', index='end', values= (assignment.name, assignment.type, score))

        tk.Frame.__init__(self, parent)
        # Main Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=700)
        canvas1.pack()

        # Student tree
        student_tree = ttk.Treeview(self, column=("c1"), show='headings')
        student_tree.column("#1", anchor=tk.W, width=200)
        student_tree.heading("#1", text="Student")
        student_tree.bind('<ButtonRelease-1>', select_item)
        student_tree.pack()
        canvas1.create_window(0, 150, window=student_tree)
        
        # Assignment tree
        assignment_tree = ttk.Treeview(self, column=("c1", "c2", "c3"), show='headings')
        assignment_tree.column("#1", anchor=tk.W, width=100)
        assignment_tree.heading("#1", text="Name")
        assignment_tree.column("#2", anchor=tk.W, width=100)
        assignment_tree.heading("#2", text="Type")
        assignment_tree.column("#3", anchor=tk.W, width=100)
        assignment_tree.heading("#3", text="Student Score")
        assignment_tree.pack()
        canvas1.create_window(350, 150, window=assignment_tree)

        # addStudent button
        addStudent = tk.Button(self, width=20, text="Add student", command=get_student_info)
        canvas1.create_window(0, 300, window=addStudent)

        # # editAssignments button
        # editAssignments = tk.Button(self, width=20, text="Edit Assignments", command=editAssignments)
        # canvas1.create_window(350, 300, window=editAssignments)

        # addAssignment button
        addAssignment = tk.Button(self, width=20, text="Add Assignment", command=get_assignment_info)
        canvas1.create_window(270, 300, window=addAssignment)

        # delAssignment button
        delAssignment = tk.Button(self, width=20, text="Delete Assignment", command=delAssignment)
        canvas1.create_window(430, 300, window=delAssignment)

        # Score
        scoreLabel = tk.Label(self, text="Score (100)", width=20)
        canvas1.create_window(-60, 400, window=scoreLabel)
        scoreEntry = tk.Entry(self, width=24)
        canvas1.create_window(50, 400, window=scoreEntry)

        # Confirm button
        confirmButton = tk.Button(self, width=20, text="Confirm Score", command=submitForm)
        canvas1.create_window(270, 400, window=confirmButton)

        # Delete Score button
        delScoreButton = tk.Button(self, width=20, text="Delete Score", command=delScore)
        canvas1.create_window(430, 400, window=delScoreButton)

        # Logout button
        logoutButton = tk.Button(self, width=20, text="Back", command=logMeOut)
        canvas1.create_window(0, 550, window=logoutButton)

        # Calcuate Class Grade button
        calcButton = tk.Button(self, width=30, text="Calculate Class Grades", command=calcGrade)
        canvas1.create_window(350, 550, window=calcButton)



# Login Page
class GradesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global dispGrades
        def dispGrades():
            for row in grades_tree.get_children():
                grades_tree.delete(row)
            
            course_grades = g1.calculate_overall_grade(g1.selectedCourse)

            for grade in course_grades:
                print(grade)
                grades_tree.insert(parent = '', index='end', values= (grade[0], grade[1],grade[2],grade[3],grade[4]))

        # Main Page Layout:
        canvas1 = tk.Canvas(self, width=400, height=700)
        canvas1.pack()

        # Assignment tree
        grades_tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        grades_tree.column("#1", anchor=tk.W, width=150)
        grades_tree.heading("#1", text="Student Name")
        grades_tree.column("#2", anchor=tk.W, width=150)
        grades_tree.heading("#2", text="HW %")
        grades_tree.column("#3", anchor=tk.W, width=150)
        grades_tree.heading("#3", text="TEST %")
        grades_tree.column("#4", anchor=tk.W, width=150)
        grades_tree.heading("#4", text="Overall %")
        grades_tree.column("#5", anchor=tk.W, width=150)
        grades_tree.heading("#5", text="Overall Grade")
        grades_tree.pack()
        canvas1.create_window(200, 200, window=grades_tree)

        # Back button
        backButton = tk.Button(self, width=15, text="Back", command=lambda: controller.show_frame(MainPage))
        canvas1.create_window(200, 400, window=backButton)

# Connect to or create Database
conn = sqlite3.connect('gradesdatabase.db')
if conn:
    print("Opened database successfully")
else:
    print("Error creating database")

# Create grademanager
g1 = GradeManager()
g1.createUserTable()
g1.createStudentsTable()
g1.createAssignmentsTable()
g1.createScoresTable()
g1.initialize()

print(g1.courses)

# Create Window and display
app = MyGrades()
app.title("Student Grading")
app.geometry("800x600")
app.mainloop()


