# Importing necessary modules
import os
import json
import datetime

# Defining a Person class (parent class for Student and Teacher)
class Person:
    def __init__(self, name, age, person_id):
        self.name = name
        self.age = age
        self.person_id = person_id

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, ID: {self.person_id}")

# Defining a Student class (inherits from Person)
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age, student_id)
        self.attendance = {}
        self.grades = {}

    def add_grade(self, subject, grade):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(grade)
        print(f"Added grade {grade} in {subject} for {self.name}")

    def add_attendance(self, date, status):
        self.attendance[date] = status
        print(f"Attendance for {self.name} on {date}: {status}")

    def calculate_average(self):
        total, count = 0, 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count > 0 else 0

    def display_report_card(self):
        print(f"\nReport Card for {self.name}:")
        for subject, grades in self.grades.items():
            average_grade = sum(grades) / len(grades)
            print(f"Subject: {subject}, Grades: {grades}, Average: {average_grade:.2f}")
        attendance_count = sum(1 for status in self.attendance.values() if status == "Present")
        print(f"Total Attendance: {attendance_count}/{len(self.attendance)}")
        print(f"Overall Average Grade: {self.calculate_average():.2f}")

# Defining a Teacher class (inherits from Person)
class Teacher(Person):
    def __init__(self, name, age, teacher_id):
        super().__init__(name, age, teacher_id)
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)
        print(f"{self.name} is now assigned to teach {subject}")

    def display_subjects(self):
        print(f"{self.name} teaches: {', '.join(self.subjects)}")

# Defining a ClassRoom class
class ClassRoom:
    def __init__(self, class_id):
        self.class_id = class_id
        self.students = []
        self.teachers = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Added {student.name} to class {self.class_id}")

    def add_teacher(self, teacher):
        self.teachers.append(teacher)
        print(f"Added {teacher.name} to class {self.class_id}")

    def display_class_info(self):
        print(f"\nClass {self.class_id} Information:")
        print("Students:")
        for student in self.students:
            student.display_info()
        print("Teachers:")
        for teacher in self.teachers:
            teacher.display_subjects()

# Defining a School class to manage students, teachers, and classrooms
class School:
    def __init__(self, name):
        self.name = name
        self.students = {}
        self.teachers = {}
        self.classrooms = {}
        self.load_data()

    # Register a student
    def register_student(self, name, age):
        student_id = len(self.students) + 1
        new_student = Student(name, age, student_id)
        self.students[student_id] = new_student
        print(f"Student {name} registered successfully with ID: {student_id}")
        return new_student

    # Register a teacher
    def register_teacher(self, name, age):
        teacher_id = len(self.teachers) + 1
        new_teacher = Teacher(name, age, teacher_id)
        self.teachers[teacher_id] = new_teacher
        print(f"Teacher {name} registered successfully with ID: {teacher_id}")
        return new_teacher

    # Create a classroom
    def create_classroom(self, class_id):
        if class_id not in self.classrooms:
            self.classrooms[class_id] = ClassRoom(class_id)
            print(f"Classroom {class_id} created successfully.")
        else:
            print(f"Classroom {class_id} already exists.")
        return self.classrooms[class_id]

    # Assign a student to a class
    def assign_student_to_class(self, student_id, class_id):
        if student_id in self.students and class_id in self.classrooms:
            student = self.students[student_id]
            classroom = self.classrooms[class_id]
            classroom.add_student(student)
        else:
            print(f"Student ID {student_id} or Class ID {class_id} not found.")

    # Assign a teacher to a class
    def assign_teacher_to_class(self, teacher_id, class_id, subject):
        if teacher_id in self.teachers and class_id in self.classrooms:
            teacher = self.teachers[teacher_id]
            classroom = self.classrooms[class_id]
            teacher.add_subject(subject)
            classroom.add_teacher(teacher)
        else:
            print(f"Teacher ID {teacher_id} or Class ID {class_id} not found.")

    # Record attendance for a student
    def record_attendance(self, student_id, date, status):
        if student_id in self.students:
            student = self.students[student_id]
            student.add_attendance(date, status)
        else:
            print(f"Student ID {student_id} not found.")

    # Record grades for a student
    def record_grade(self, student_id, subject, grade):
        if student_id in self.students:
            student = self.students[student_id]
            student.add_grade(subject, grade)
        else:
            print(f"Student ID {student_id} not found.")

    # Display class information
    def display_class(self, class_id):
        if class_id in self.classrooms:
            classroom = self.classrooms[class_id]
            classroom.display_class_info()
        else:
            print(f"Class ID {class_id} not found.")

    # Save data to a file
    def save_data(self):
        data = {
            "students": {student_id: {"name": student.name, "age": student.age, "attendance": student.attendance, "grades": student.grades} for student_id, student in self.students.items()},
            "teachers": {teacher_id: {"name": teacher.name, "age": teacher.age, "subjects": teacher.subjects} for teacher_id, teacher in self.teachers.items()},
            "classrooms": {class_id: {"students": [student.person_id for student in classroom.students], "teachers": [teacher.person_id for teacher in classroom.teachers]} for class_id, classroom in self.classrooms.items()}
        }
        with open('school_data.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("School data saved successfully.")

    # Load data from a file
    def load_data(self):
        if os.path.exists('school_data.json'):
            with open('school_data.json', 'r') as file:
                data = json.load(file)
                for student_id, info in data["students"].items():
                    student = Student(info["name"], info["age"], student_id)
                    student.attendance = info["attendance"]
                    student.grades = info["grades"]
                    self.students[student_id] = student
                for teacher_id, info in data["teachers"].items():
                    teacher = Teacher(info["name"], info["age"], teacher_id)
                    teacher.subjects = info["subjects"]
                    self.teachers[teacher_id] = teacher
                for class_id, class_info in data["classrooms"].items():
                    classroom = self.create_classroom(class_id)
                    for student_id in class_info["students"]:
                        classroom.add_student(self.students[student_id])
                    for teacher_id in class_info["teachers"]:
                        classroom.add_teacher(self.teachers[teacher_id])
            print("School data loaded successfully.")
        else:
            print("No previous data found.")

# Main program to manage the school system
def main():
    school = School("Green Valley High School")

    # Registering students
    student1 = school.register_student("John Doe", 15)
    student2 = school.register_student("Jane Smith", 16)
    student3 = school.register_student("Sam Brown", 14)

    # Registering teachers
    teacher1 = school.register_teacher("Mrs. Robinson", 35)
    teacher2 = school.register_teacher("Mr. Anderson", 40)

    # Creating classrooms
    class10 = school.create_classroom("10A")
    class11 = school.create_classroom("11B")

    # Assign students to classes
    school.assign_student_to_class(1, "10A")
    school.assign_student_to_class(2, "11B")
    school.assign_student_to_class(3, "10A")

    # Assign teachers to classes and subjects
    school.assign_teacher_to_class(1, "10A", "Math")
    school.assign_teacher_to_class(2, "11B", "Science")

    # Recording attendance
    school.record_attendance(1, "2024-09-29", "Present")
    school.record_attendance(2, "2024-09-29", "Absent")
    school.record_attendance(3, "2024-09-29", "Present")

    # Recording grades
    school.record_grade(1, "Math", 85)
    school.record_grade(1, "Science", 78)
    school.record_grade(2, "Math", 92)
    school.record_grade(3, "Science", 88)

    # Display class information
    school.display_class("10A")

    # Generate report cards for students
    student1.display_report_card()
    student2.display_report_card()

    # Saving data
    school.save_data()

if __name__ == "__main__":
    main()
