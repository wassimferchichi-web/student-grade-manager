# ============================================================
#  Student Grade Manager
#  A beginner-friendly console app to track student grades
# ============================================================

# ---------- Data Storage ----------
# We use a list of dictionaries to store students.
# Each student looks like:
#   { "name": "Alice", "grades": [85, 90, 78] }

students = []

PASS_MARK = 50          # Minimum average to pass
MAX_GRADE = 100         # Grades must be between 0 and MAX_GRADE


# ──────────────────────────────────────────────
#  Helper / utility functions
# ──────────────────────────────────────────────

def calculate_average(grades):
    """Return the average of a list of grades, or 0 if empty."""
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def get_status(average):
    """Return 'PASS' or 'FAIL' based on the average."""
    return "PASS" if average >= PASS_MARK else "FAIL"


def find_student(name):
    """Find a student by name (case-insensitive). Returns the dict or None."""
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None


def get_letter_grade(average):
    """Convert a numeric average to a letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


# ──────────────────────────────────────────────
#  Input validation helpers
# ──────────────────────────────────────────────

def input_non_empty(prompt):
    """Ask for a non-empty string; keep asking until one is given."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ⚠  This field cannot be empty. Please try again.")


def input_grade(prompt):
    """Ask for a valid grade (0–100). Returns a float."""
    while True:
        raw = input(prompt).strip()
        try:
            grade = float(raw)
            if 0 <= grade <= MAX_GRADE:
                return grade
            else:
                print(f"  ⚠  Grade must be between 0 and {MAX_GRADE}.")
        except ValueError:
            print("  ⚠  Please enter a number (e.g. 85 or 91.5).")


def input_positive_int(prompt):
    """Ask for a positive integer. Returns an int."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value > 0:
                return value
            else:
                print("  ⚠  Please enter a number greater than 0.")
        except ValueError:
            print("  ⚠  Please enter a whole number (e.g. 3).")


# ──────────────────────────────────────────────
#  Core feature functions
# ──────────────────────────────────────────────

def add_student():
    """Add a new student (with optional grades)."""
    print("\n── Add New Student ──────────────────────────")
    name = input_non_empty("  Student name : ")

    # Check for duplicates
    if find_student(name):
        print(f"  ⚠  '{name}' already exists. Use 'Add Grades' to update.")
        return

    # Optionally add grades right away
    grades = []
    add_now = input("  Add grades now? (y/n) : ").strip().lower()
    if add_now == "y":
        count = input_positive_int("  How many grades? : ")
        for i in range(count):
            grade = input_grade(f"    Grade {i + 1}: ")
            grades.append(grade)

    students.append({"name": name, "grades": grades})
    print(f"\n  ✔  '{name}' added successfully!")


def add_grades():
    """Add more grades to an existing student."""
    print("\n── Add Grades ───────────────────────────────")
    if not students:
        print("  ⚠  No students yet. Add a student first.")
        return

    name = input_non_empty("  Student name : ")
    student = find_student(name)
    if not student:
        print(f"  ⚠  No student named '{name}' found.")
        return

    count = input_positive_int("  How many grades to add? : ")
    for i in range(count):
        grade = input_grade(f"    Grade {i + 1}: ")
        student["grades"].append(grade)

    print(f"\n  ✔  Added {count} grade(s) to '{student['name']}'.")


def view_student():
    """Display full details for one student."""
    print("\n── View Student ─────────────────────────────")
    if not students:
        print("  ⚠  No students yet.")
        return

    name = input_non_empty("  Student name : ")
    student = find_student(name)
    if not student:
        print(f"  ⚠  No student named '{name}' found.")
        return

    avg    = calculate_average(student["grades"])
    status = get_status(avg)
    letter = get_letter_grade(avg)

    print(f"\n  Name    : {student['name']}")
    if student["grades"]:
        print(f"  Grades  : {', '.join(str(g) for g in student['grades'])}")
        print(f"  Average : {avg:.2f}  ({letter})")
        print(f"  Status  : {status}")
    else:
        print("  Grades  : (none yet)")


def display_all_students():
    """Show all students sorted by average (highest first)."""
    print("\n── All Students ─────────────────────────────")
    if not students:
        print("  ⚠  No students yet.")
        return

    # Sort a copy so the original list order is preserved
    sorted_students = sorted(
        students,
        key=lambda s: calculate_average(s["grades"]),
        reverse=True
    )

    # Table header
    print(f"\n  {'#':<4} {'Name':<20} {'Grades':^30} {'Avg':>6}  {'Ltr':>3}  {'Status'}")
    print("  " + "-" * 72)

    for rank, student in enumerate(sorted_students, start=1):
        avg    = calculate_average(student["grades"])
        letter = get_letter_grade(avg)
        status = get_status(avg)

        if student["grades"]:
            grades_str = ", ".join(str(int(g) if g == int(g) else g) for g in student["grades"])
            # Truncate if too long for display
            if len(grades_str) > 28:
                grades_str = grades_str[:25] + "..."
            avg_str = f"{avg:.1f}"
        else:
            grades_str = "(no grades)"
            avg_str    = "—"
            letter     = "—"
            status     = "—"

        print(f"  {rank:<4} {student['name']:<20} {grades_str:<30} {avg_str:>6}  {letter:>3}  {status}")

    print()


def remove_student():
    """Remove a student from the list."""
    print("\n── Remove Student ───────────────────────────")
    if not students:
        print("  ⚠  No students yet.")
        return

    name = input_non_empty("  Student name to remove : ")
    student = find_student(name)
    if not student:
        print(f"  ⚠  No student named '{name}' found.")
        return

    confirm = input(f"  Are you sure you want to remove '{student['name']}'? (y/n) : ").strip().lower()
    if confirm == "y":
        students.remove(student)
        print(f"\n  ✔  '{name}' removed.")
    else:
        print("  Cancelled.")


def show_summary():
    """Show class-wide statistics."""
    print("\n── Class Summary ────────────────────────────")
    if not students:
        print("  ⚠  No students yet.")
        return

    students_with_grades = [s for s in students if s["grades"]]
    if not students_with_grades:
        print("  ⚠  No grades recorded yet.")
        return

    averages = [calculate_average(s["grades"]) for s in students_with_grades]
    passing  = sum(1 for a in averages if a >= PASS_MARK)
    failing  = len(averages) - passing

    top_student = students_with_grades[averages.index(max(averages))]
    low_student = students_with_grades[averages.index(min(averages))]

    print(f"\n  Total students     : {len(students)}")
    print(f"  With grades        : {len(students_with_grades)}")
    print(f"  Class average      : {sum(averages) / len(averages):.2f}")
    print(f"  Highest average    : {max(averages):.2f}  ({top_student['name']})")
    print(f"  Lowest average     : {min(averages):.2f}  ({low_student['name']})")
    print(f"  Passing            : {passing} student(s)")
    print(f"  Failing            : {failing} student(s)")
    print()


# ──────────────────────────────────────────────
#  Menu system
# ──────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════╗
║       STUDENT GRADE MANAGER         ║
╠══════════════════════════════════════╣
║  1. Add a new student               ║
║  2. Add grades to a student         ║
║  3. View a student's details        ║
║  4. Display all students (sorted)   ║
║  5. Class summary / statistics      ║
║  6. Remove a student                ║
║  7. Exit                            ║
╚══════════════════════════════════════╝
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
    print("\n  Welcome to the Student Grade Manager!")
    print(f"  Pass mark is set to {PASS_MARK}/100.\n")

    while True:
        print(MENU)
        choice = input("  Enter your choice (1-7): ").strip()

        if choice == "7":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print("  ⚠  Invalid choice. Please enter a number from 1 to 7.")


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()