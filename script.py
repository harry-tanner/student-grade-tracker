def addstudent():
    student=input("What is the students name")
    maths = int(input("Enter the student's Maths score (0-100): "))
    english = int(input("Enter the student's English score (0-100): "))
    science = int(input("Enter the student's Science score (0-100): "))

    return {
        "name": student,
        "maths": maths,
        "english": english,
        "science": science
    }
def average(students):
    if len(students) == 0:
        print("No students have been added yet.")
        return

    maths_total = 0
    english_total = 0
    science_total = 0

    for student in students:
        maths_total += student["maths"]
        english_total += student["english"]
        science_total += student["science"]

    number_of_students = len(students)
    print(f"Maths average: {maths_total / number_of_students:.2f}")
    print(f"English average: {english_total / number_of_students:.2f}")
    print(f"Science average: {science_total / number_of_students:.2f}")


students = []

while True:
    print("\n===== STUDENT GRADE TRACKER =====")
    print("1. Add a new student")
    print("2. See class averages")
    print("3. Stop")
    choice = input("Would you like to add a new student, see averages, or stop? Enter 1, 2 or 3: ")

    if choice == "1":
        new_student = addstudent()
        students.append(new_student)
        print("Student added.")
    elif choice == "2":
        average(students)
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Please enter 1, 2 or 3.")
