# Grading Management App

## Overview

The Grading Management App is a tool designed to help educators manage student information, assignments, and grades across multiple courses. It enables users to add students, create assignments, assign grades, and calculate overall student performance.

## Features

- **Course Management:** Create and manage multiple courses with unique passwords.
- **Student Enrollment:** Add and view students in each course.
- **Assignment Management:** Add and delete assignments for each course.
- **Grade Assignment:** Assign and modify student scores for homework and tests.
- **Automatic Grade Calculation:** Compute overall student grades based on weighted scores (30% homework, 70% tests).
- **User Authentication:** Secure login and registration for course access.
- **Graphical User Interface (GUI):** Easy-to-use interface for managing grading tasks.

## Installation

### Prerequisites

- Python (latest version recommended)
- SQLite (included with Python)
- Required Python libraries (install via `pip`)

### Steps to Install

1. **Download the source code**
2. **Install dependencies** using:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```sh
   python main.py
   ```

## Usage

### 1. Course Registration & Login

- New courses require a unique name and password.
- Users must log in with the correct credentials to access the grading system.

### 2. Managing Students and Assignments

- Add new students by entering their name and student ID.
- Create assignments, specifying whether they are Homework or Test.
- Remove students or assignments as needed.

### 3. Assigning and Modifying Grades

- Select a student and an assignment.
- Enter the corresponding score and confirm to save.
- Modify existing scores if necessary.

### 4. Viewing Grades and Overall Performance

- Check individual student scores for assignments.
- Calculate the overall grade based on weighted scores.
- View all student grades in a summarized format.

## Database Structure

The app uses an SQLite database with the following tables:

- **Users** (stores authentication credentials)
- **Students** (stores student details per course)
- **Assignments** (stores assignment details per course)
- **Scores** (stores student grades for assignments)

## Technologies Used

- **Python** for backend logic and calculations
- **Tkinter** for GUI implementation
- **SQLite** for data storage

## Troubleshooting

- If the app fails to launch, ensure all dependencies are installed correctly.
- If database errors occur, delete the existing `gradesdatabase.db` and restart the app to recreate tables.

## License

This project is open-source and available under the MIT License.

## Contact

For questions or support, please contact: tanmaynedu@gmail.com

