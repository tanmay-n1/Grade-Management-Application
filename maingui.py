import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name):
        self.name = name
        self.assignments = {"Homework": {}, "Test": {}}

    def add_assignment_grade(self, assignment_type, assignment_name, grade):
        if assignment_type not in self.assignments:
            raise ValueError("Invalid assignment type")

        if not 0 <= grade <= 100:
            raise ValueError("Invalid grade")

        self.assignments[assignment_type][assignment_name] = grade

    def delete_assignment(self, assignment_type, assignment_name):
        if assignment_type not in self.assignments:
            raise ValueError("Invalid assignment type")

        if assignment_name not in self.assignments[assignment_type]:
            raise ValueError("Assignment not found")

        del self.assignments[assignment_type][assignment_name]

    def edit_assignment_grade(self, assignment_type, assignment_name, grade):
        self.delete_assignment(assignment_type, assignment_name)
        self.add_assignment_grade(assignment_type, assignment_name, grade)

    def calculate_overall_grade(self):
        total_points = 0
        total_possible_points = 0

        for assignments in self.assignments.values():
            for grade in assignments.values():
                total_points += grade
                total_possible_points += 100

        overall_grade_percentage = (total_points / total_possible_points) * 100

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

        return overall_grade_percentage, letter_grade

class Course:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)

def add_student_window():
    # Create a new window for adding a student
    add_student_window = tk.Toplevel(root)
    add_student_window.title("Add Student")

    # Labels and Entry fields
    tk.Label(add_student_window, text="Student Name:").grid(row=0, column=0)
    student_name_entry = tk.Entry(add_student_window)
    student_name_entry.grid(row=0, column=1)

    # Add Student Button
    add_student_btn = tk.Button(add_student_window, text="Add Student", command=lambda: add_student(student_name_entry.get(), add_student_window))
    add_student_btn.grid(row=1, column=0, columnspan=2)

def add_student(name, window):
    new_student = Student(name)
    math_class.add_student(new_student)
    window.destroy()
    update_student_listbox()

def update_student_listbox():
    student_listbox.delete(0, tk.END)
    for student in math_class.students:
        student_listbox.insert(tk.END, student.name)

def display_student_grades():
    selected_index = student_listbox.curselection()
    if selected_index:
        selected_student = math_class.students[selected_index[0]]
        overall_percentage, letter_grade = selected_student.calculate_overall_grade()
        messagebox.showinfo("Overall Grade", f"Overall Percentage: {overall_percentage:.2f}%, Letter Grade: {letter_grade}")
    else:
        messagebox.showwarning("No Student Selected", "Please select a student.")

root = tk.Tk()
root.title("Grade Tracker")

# Create a class
math_class = Course("Math")

# Main Frame
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Student Listbox
student_listbox = tk.Listbox(main_frame)
student_listbox.pack(side=tk.LEFT, padx=10)

# Add Student Button
add_student_btn = tk.Button(main_frame, text="Add Student", command=add_student_window)
add_student_btn.pack(pady=5)

# Display Grades Button
display_grades_btn = tk.Button(main_frame, text="Display Grades", command=display_student_grades)
display_grades_btn.pack(pady=5)

root.mainloop()

