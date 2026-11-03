import json
import os

grade_records = []

subjects = ["GEN 001", "GEN 002", "NST 021", "ITE 260",
            "ITE 366", "GEN 006", "MAT 152", "PED 030"]

periods = ["P1", "P2", "P3"]


# LOAD SAVED GRADES
def load_records():
    global grade_records

    grade_records = []

    if os.path.exists("grades.json"):
        try:
            with open("grades.json", "r") as file:
                saved_records = json.load(file)

            if isinstance(saved_records, list):
                for record in saved_records:
                    if (isinstance(record, list)
                            and len(record) == 9
                            and all(isinstance(record[i], (int, float))
                                    for i in [4, 5, 6, 7])):
                        grade_records.append(record)

        except (ValueError, OSError):
            grade_records = []
            print("Unable to load saved grades.")


# SAVE GRADES
def save_records():
    try:
        with open("grades.json", "w") as file:
            json.dump(grade_records, file, indent=4)

        return True

    except OSError:
        print("Error saving grades.")
        return False


# CHECK GRADE STATUS
def check_grade(grade):
    if grade >= 90:
        return "Excellent"
    elif grade >= 75:
        return "Passed"
    else:
        return "Needs Improvement"


# DISPLAY TABLE
def display_table(headers, rows):
    widths = []

    for i, header in enumerate(headers):
        longest = len(header)

        for row in rows:
            longest = max(longest, len(str(row[i])))

        widths.append(longest + 2)

    border = "+"
    for width in widths:
        border += "-" * width + "+"

    print(border)

    header_line = "|"
    for i, header in enumerate(headers):
        header_line += " " + header.ljust(widths[i] - 1) + "|"

    print(header_line)
    print(border)

    for row in rows:
        row_line = "|"

        for i, value in enumerate(row):
            row_line += " " + str(value).ljust(widths[i] - 1) + "|"

        print(row_line)

    print(border)


# RECORD STUDENT GRADES
def add_grade(period):
    print("\n=== RECORD STUDENT GRADES ===")
    print("Selected Period:", period)

    student_id = input("Student ID: ").strip()
    student_name = input("Student Name: ").strip()
    section = input("Student Section: ").strip()

    if not student_id or not student_name or not section:
        print("Please complete all student information.")
        return

    print("\n=== SUBJECTS ===")

    for i, subject_name in enumerate(subjects, start=1):
        print(i, subject_name)

    try:
        choice = int(input("Choose subject number: "))

        if choice < 1 or choice > len(subjects):
            print("Invalid subject number.")
            return

        subject = subjects[choice - 1]

        quiz = float(input("Quiz Score (0-100): "))
        attendance = float(input("Attendance Score (0-100): "))
        task = float(input("Performance Task Score (0-100): "))

        if not all(0 <= score <= 100
                   for score in [quiz, attendance, task]):
            print("Scores must be between 0 and 100.")
            return

        # CALCULATE PERIOD GRADE
        grade = (quiz + attendance + task) / 3

        # UPDATE STUDENT NAME AND SECTION
        for record in grade_records:
            if record[0] == student_id:
                record[1] = student_name
                record[8] = section

        # CHECK IF RECORD ALREADY EXISTS
        found = False

        for record in grade_records:
            if (record[0] == student_id
                    and record[2] == subject
                    and record[3] == period):

                record[1] = student_name
                record[4] = quiz
                record[5] = attendance
                record[6] = task
                record[7] = grade
                record[8] = section

                found = True
                break

        if found:
            message = "Student grades updated!"
        else:
            record = [
                student_id, student_name, subject, period,
                quiz, attendance, task, grade, section
            ]

            grade_records.append(record)
            message = "Student grades recorded!"

        if save_records():
            print(message)
        else:
            print("Grades changed, but could not be saved.")

        print("Period Grade:", round(grade, 2))
        print("Status:", check_grade(grade))

    except ValueError:
        print("Please enter valid numbers.")


# VIEW ALL GRADES SEPARATED BY P1, P2, P3
def view_grades():
    if not grade_records:
        print("\nNo grades recorded yet.")
        return

    headers = [
        "Student ID", "Student Name", "Section",
        "Subject", "Quiz", "Attendance",
        "Task", "Grade", "Status"
    ]

    print("\n" + "=" * 45)
    print("       COLLEGE GRADE MONITORING SYSTEM")
    print("              ALL STUDENT GRADES")
    print("=" * 45)

    total_records = 0

    for period in periods:
        rows = []

        for record in grade_records:
            if record[3] == period:
                rows.append([
                    record[0],
                    record[1],
                    record[8],
                    record[2],
                    f"{record[4]:.2f}",
                    f"{record[5]:.2f}",
                    f"{record[6]:.2f}",
                    f"{record[7]:.2f}",
                    check_grade(record[7])
                ])

        print(f"\n========== {period} GRADES ==========")

        if rows:
            display_table(headers, rows)
            print("Total", period, "Records:", len(rows))
            total_records += len(rows)
        else:
            print("No grades recorded for", period)

    print("\nTotal Records:", total_records)


# STUDENT CHECK GRADES SEPARATED BY P1, P2, P3
def student_check_grades():
    student_id = input("Enter your Student ID: ").strip()

    student_records = [
        record for record in grade_records
        if record[0] == student_id
    ]

    if not student_records:
        print("No grades found for this Student ID.")
        return

    print("\n" + "=" * 45)
    print("                MY GRADE REPORT")
    print("=" * 45)
    print("Student ID:", student_id)
    print("Name:", student_records[0][1])
    print("Section:", student_records[0][8])

    headers = [
        "Subject", "Quiz", "Attendance",
        "Task", "Grade", "Status"
    ]

    total = 0
    count = 0

    for period in periods:
        rows = []

        for record in student_records:
            if record[3] == period:
                rows.append([
                    record[2],
                    f"{record[4]:.2f}",
                    f"{record[5]:.2f}",
                    f"{record[6]:.2f}",
                    f"{record[7]:.2f}",
                    check_grade(record[7])
                ])

                # AREAS THAT NEED IMPROVEMENT
                if record[4] < 75:
                    print(
                        f"\n{period} - {record[2]}: "
                        "Improve your quiz score."
                    )

                if record[5] < 75:
                    print(
                        f"\n{period} - {record[2]}: "
                        "Improve your attendance score."
                    )

                if record[6] < 75:
                    print(
                        f"\n{period} - {record[2]}: "
                        "Improve your performance task score."
                    )

                total += record[7]
                count += 1

        print(f"\n========== {period} GRADES ==========")

        if rows:
            display_table(headers, rows)
        else:
            print("No grades recorded for", period)

    # GRADE SUMMARY
    if count > 0:
        average = total / count

        print("\n========== GRADE SUMMARY ==========")
        print("Total Recorded Grades:", count)
        print("Average of Recorded Period Grades:",
              round(average, 2))
        print("Overall Status:", check_grade(average))


# MAIN PROGRAM
load_records()

while True:
    print("\n=== COLLEGE GRADE MONITORING SYSTEM ===")
    print("1. Record P1 Grades")
    print("2. Record P2 Grades")
    print("3. Record P3 Grades")
    print("4. View All Grades")
    print("5. Student Check Grades")
    print("6. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_grade("P1")

    elif choice == "2":
        add_grade("P2")

    elif choice == "3":
        add_grade("P3")

    elif choice == "4":
        view_grades()

    elif choice == "5":
        student_check_grades()

    elif choice == "6":
        if save_records():
            print("Grades saved. Program ended.")
        else:
            print("Warning: Grades could not be saved.")

        break

    else:
        print("Invalid choice. Try again.")