"""Run with: py app.py, then visit http://127.0.0.1:5000."""

import json
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("students.json")
SUBJECTS = ("maths", "english", "science")
# Classroom practice boundaries, not official exam-board boundaries.
GRADE_BOUNDARIES = [(grade * 10, str(grade)) for grade in range(9, 0, -1)]


@app.template_filter("grade")
def grade(score):
    for minimum, result in GRADE_BOUNDARIES:
        if score >= minimum:
            return result
    return "U"


def read_scores(values):
    scores = {}
    for subject in SUBJECTS:
        try:
            score = int(values.get(subject, ""))
        except ValueError:
            raise ValueError(f"Enter a whole number for {subject.title()}.") from None
        if not 0 <= score <= 100:
            raise ValueError(f"{subject.title()} must be between 0 and 100.")
        scores[subject] = score
    return scores


def load_students():
    if DATA_FILE.exists():
        students = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        # Give older records an ID so sorting never changes who is removed.
        changed = False
        for student in students:
            if "id" not in student:
                student["id"] = uuid4().hex
                changed = True
        if changed:
            save_students(students)
        return students
    return []


def save_students(students):
    temporary_file = DATA_FILE.with_suffix(".tmp")
    temporary_file.write_text(json.dumps(students, indent=2), encoding="utf-8")
    temporary_file.replace(DATA_FILE)


def average(students):
    # Same calculation as the terminal version: total divided by class size.
    if not students:
        return {subject: None for subject in SUBJECTS}
    totals = {subject: 0 for subject in SUBJECTS}
    for student in students:
        for subject in SUBJECTS:
            totals[subject] += student[subject]
    return {subject: totals[subject] / len(students) for subject in SUBJECTS}


@app.route("/", methods=["GET", "POST"])
def index():
    students = load_students()
    error = None
    values = {}

    if request.method == "POST":
        # A webpage form supplies the values instead of input().
        values = request.form
        name = values.get("name", "").strip()
        try:
            if not name or len(name) > 100:
                raise ValueError("Enter a student name between 1 and 100 characters.")
            scores = read_scores(values)
            students.append({"id": uuid4().hex, "name": name, **scores})
            save_students(students)
            # Redirect so refreshing the page does not submit a second student.
            return redirect(url_for("index", added="1"))
        except ValueError as exc:
            error = str(exc)

    students.sort(key=lambda student: sum(student[subject] for subject in SUBJECTS) / len(SUBJECTS), reverse=True)
    query = request.args.get("q", "").strip()
    matches = [student for student in students if query.casefold() in student["name"].casefold()]
    combined = sum(sum(student[subject] for subject in SUBJECTS) for student in students) / len(students) if students else None
    return render_template(
        "index.html", students=students, averages=average(students),
        matches=matches, query=query, combined=combined,
        subjects=SUBJECTS, error=error, values=values,
        added=request.args.get("added") == "1",
        removed=request.args.get("removed") == "1",
    ), 400 if error else 200


@app.route("/students/<student_id>", methods=["GET", "POST"])
def profile(student_id):
    students = load_students()
    student = next((item for item in students if item["id"] == student_id), None)
    if student is None:
        abort(404)
    error = None
    values = student
    if request.method == "POST":
        values = request.form
        try:
            scores = read_scores(values)
            student.update(scores)
            save_students(students)
            return redirect(url_for("profile", student_id=student_id, updated="1"))
        except ValueError as exc:
            error = str(exc)
    total = sum(student[subject] for subject in SUBJECTS)
    return render_template(
        "profile.html", student=student, subjects=SUBJECTS, values=values,
        error=error, total=total, mean=total / len(SUBJECTS),
        boundaries=GRADE_BOUNDARIES, updated=request.args.get("updated") == "1",
    ), 400 if error else 200

@app.post("/students/<student_id>/remove")
def remove_student(student_id):
    students = load_students()
    remaining = [student for student in students if student["id"] != student_id]
    if len(remaining) == len(students):
        return "Student not found. Return to the tracker and refresh the page.", 404
    save_students(remaining)
    return redirect(url_for("index", removed="1"))



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
