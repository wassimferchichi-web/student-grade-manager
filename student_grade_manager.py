students = []

PASS_MARK = 10
MAX_GRADE = 20


def calculate_average(grades):
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def get_status(average):
    return "PASS" if average >= PASS_MARK else "FAIL"


def get_mention(average):
    if average >= 16:
        return "Tres Bien"
    elif average >= 14:
        return "Bien"
    elif average >= 12:
        return "Assez Bien"
    elif average >= 10:
        return "Passable"
    else:
        return "Insuffisant"


def find_student(name):
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def input_grade(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            grade = float(raw)
            if 0 <= grade <= MAX_GRADE:
                return grade
            else:
                print(f"Grade must be between 0 and {MAX_GRADE}.")
        except ValueError:
            print("Please enter a valid number.")


def input_positive_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value > 0:
                return value
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a whole number.")


def add_student():
    print("\n-- Add New Student --")
    name = input_non_empty("Name: ")

    if find_student(name):
        print(f"'{name}' already exists.")
        return

    grades = []
    if input("Add grades now? (y/n): ").strip().lower() == "y":
        count = input_positive_int("How many grades? ")
        for i in range(count):
            grades.append(input_grade(f"  Grade {i + 1}: "))

    students.append({"name": name, "grades": grades})
    print(f"'{name}' added.")


def add_grades():
    print("\n-- Add Grades --")
    if not students:
        print("No students found.")
        return

    student = find_student(input_non_empty("Name: "))
    if not student:
        print("Student not found.")
        return

    count = input_positive_int("How many grades to add? ")
    for i in range(count):
        student["grades"].append(input_grade(f"  Grade {i + 1}: "))

    print(f"Grades added to '{student['name']}'.")


def view_student():
    print("\n-- View Student --")
    if not students:
        print("No students found.")
        return

    student = find_student(input_non_empty("Name: "))
    if not student:
        print("Student not found.")
        return

    avg = calculate_average(student["grades"])
    print(f"\nName    : {student['name']}")
    if student["grades"]:
        print(f"Grades  : {', '.join(str(g) for g in student['grades'])}")
        print(f"Average : {avg:.2f} / 20")
        print(f"Mention : {get_mention(avg)}")
        print(f"Status  : {get_status(avg)}")
    else:
        print("Grades  : none")


def display_all_students():
    print("\n-- All Students (sorted by average) --")
    if not students:
        print("No students found.")
        return

    sorted_students = sorted(students, key=lambda s: calculate_average(s["grades"]), reverse=True)

    print(f"\n  {'#':<4} {'Name':<20} {'Average':>8}  {'Mention':<14}  {'Status'}")
    print("  " + "-" * 58)

    for rank, student in enumerate(sorted_students, start=1):
        avg = calculate_average(student["grades"])
        if student["grades"]:
            print(f"  {rank:<4} {student['name']:<20} {avg:.2f}/20  {get_mention(avg):<14}  {get_status(avg)}")
        else:
            print(f"  {rank:<4} {student['name']:<20} {'--':>8}  {'--':<14}  --")

    print()


def remove_student():
    print("\n-- Remove Student --")
    if not students:
        print("No students found.")
        return

    student = find_student(input_non_empty("Name: "))
    if not student:
        print("Student not found.")
        return

    if input(f"Remove '{student['name']}'? (y/n): ").strip().lower() == "y":
        students.remove(student)
        print("Student removed.")
    else:
        print("Cancelled.")


def show_summary():
    print("\n-- Class Summary --")
    if not students:
        print("No students found.")
        return

    graded = [s for s in students if s["grades"]]
    if not graded:
        print("No grades recorded yet.")
        return

    averages = [calculate_average(s["grades"]) for s in graded]
    top = graded[averages.index(max(averages))]
    low = graded[averages.index(min(averages))]

    print(f"\n  Total students  : {len(students)}")
    print(f"  With grades     : {len(graded)}")
    print(f"  Class average   : {sum(averages) / len(averages):.2f} / 20")
    print(f"  Highest average : {max(averages):.2f} / 20  ({top['name']})")
    print(f"  Lowest average  : {min(averages):.2f} / 20  ({low['name']})")
    print(f"  Passing         : {sum(1 for a in averages if a >= PASS_MARK)}")
    print(f"  Failing         : {sum(1 for a in averages if a < PASS_MARK)}")
    print()


MENU = """
Student Grade Manager
---------------------
1. Add a new student
2. Add grades to a student
3. View a student
4. Display all students
5. Class summary
6. Remove a student
7. Exit
"""

ACTIONS = {
    "1": add_student,
    "2": add_grades,
    "3": view_student,
    "4": display_all_students,
    "5": show_summary,
    "6": remove_student,
}


def main():
    print("Student Grade Manager | Scale: 0-20 | Pass mark: 10/20")

    while True:
        print(MENU)
        choice = input("Choice: ").strip()

        if choice == "7":
            print("Goodbye.")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()