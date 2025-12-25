# Project Overview
# A Student Management System is used to store, manage, update, and retrieve student
# information from a database using Object-Oriented Programming (OOP) principles.

# ✔ Features
# Add new student
# View student details
# Update student records
# Delete student
# Store data in database (DBMS)

# | OOP Concept        | Usage                               |
# | ------------------ | ----------------------------------- |
# | Class & Object     | Student, Database classes           |
# | Encapsulation      | Private variables + getters/setters |
# | Abstraction        | Database operations hidden          |
# | Inheritance        | Base `Person` → `Student`           |
# | Polymorphism       | Method overriding (optional)        |


import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password@123",  # put your MySQL password
            database="student_db",
        )
        self.cursor = self.conn.cursor()


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    def __init__(self, name, age, course, email, phone):
        super().__init__(name, age)
        self.course = course
        self.email = email
        self.phone = phone


class StudentManager(Database):

    def add_student(self, student):

        # 🔍 Check if student already exists
        check_query = """
        SELECT student_id FROM students
        WHERE email = %s OR phone = %s
        """
        self.cursor.execute(check_query, (student.email, student.phone))
        result = self.cursor.fetchone()

        if result:
            print("⚠ Student already exists in the system!")
            return None

        # ✅ Insert new student
        insert_query = """
        INSERT INTO students (name, age, course, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            student.name,
            student.age,
            student.course,
            student.email,
            student.phone,
        )

        self.cursor.execute(insert_query, values)
        self.conn.commit()

        student_id = self.cursor.lastrowid
        print(f"✅ Student added successfully. Student ID is: {student_id}")
        return student_id

    def view_students(self):
        self.cursor.execute("SELECT * FROM students")
        records = self.cursor.fetchall()

        if not records:
            print("⚠ No student records found.")
            return

        print("\n---------------- STUDENT RECORDS ----------------")
        print(
            "{:<5} {:<20} {:<5} {:<15} {:<15} {:<25}".format(
                "ID", "Name", "Age", "Phone", "Course", "Email"
            )
        )
        print("-" * 90)

        for row in records:
            print(
                "{:<5} {:<20} {:<5} {:<15} {:<15} {:<25}".format(
                    row[0], row[1], row[2], row[3], row[4], row[5]
                )
            )

    def update_student(self, student_id, course):
        query = "UPDATE students SET course = %s WHERE student_id = %s"
        self.cursor.execute(query, (course, student_id))
        self.conn.commit()
        print("✅ Student updated successfully")

    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE student_id = %s"
        self.cursor.execute(query, (student_id,))
        self.conn.commit()
        print("❌ Student deleted successfully")


def main():
    manager = StudentManager()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            course = input("Enter course: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")

            student = Student(name, age, course, email, phone)
            manager.add_student(student)

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            student_id = int(input("Enter student ID: "))
            course = input("Enter new course: ")
            manager.update_student(student_id, course)

        elif choice == "4":
            student_id = int(input("Enter student ID: "))
            manager.delete_student(student_id)

        elif choice == "5":
            print("👋 Exiting system...")
            break

        else:
            print("⚠ Invalid choice, try again")


if __name__ == "__main__":
    main()
