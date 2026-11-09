# Student Grade Tracker

A Python and Flask learning project that turns a terminal-based grade tracker into a styled webpage.

## AI disclosure and purpose

**This is an AI-generated project, developed through an iterative conversation with OpenAI's Codex.** I supplied the requirements and requested changes while the AI generated the implementation, styling, and automated checks. It should not be presented as independently written software.

I am interested in a future in software development. This project is an experiment in how AI can help build software, how it responds to feedback, and where its limitations become visible. It is also a starting point for learning how Python, HTML, and CSS work together.

The experiment explores:

- Turning a basic programming task into a working local web application.
- Adding features incrementally through natural-language requests.
- Checking generated behaviour rather than assuming generated code is correct.
- Distinguishing a working prototype from software ready for real users.

## Features

- Add students with Maths, English, and Science scores out of 100.
- List students from highest average to lowest.
- Search by all or part of a student's name.
- Open student profiles and edit their scores.
- Show illustrative GCSE-style grades from 9 to 1, or U.
- Calculate subject averages and an overall class average.
- Remove students and update the averages automatically.
- Save webpage records locally between runs.
- Use a responsive HTML and CSS interface.

## Run locally

Requires Python 3.10 or newer. In a terminal, open the folder containing `app.py`.

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

On macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open **http://127.0.0.1:5000** in your browser. Keep the terminal running and press **Ctrl+C** to stop. Run the Python server rather than opening the HTML file directly.

For the original terminal version, run `py script.py` on Windows or `python3 script.py` on macOS/Linux. Its records are stored only in memory and are separate from the webpage's records.

## How the project works

| File | Purpose |
| --- | --- |
| `app.py` | Flask routes, score validation, calculations, and local saving |
| `templates/index.html` | Dashboard, search, student table, and add form |
| `templates/profile.html` | Individual results, practice grades, and score editing |
| `static/style.css` | Colours, layout, and responsive styling |
| `script.py` | Original terminal exercise |
| `requirements.txt` | Webpage dependencies |
| `test_app.py` | Automated checks using temporary student records |

`students.json` is created when you add your first student. It is excluded from GitHub so locally entered student details are not published. No student records are included in this repository.

## Calculations and practice grades

A student's average is their three scores added together, divided by three. Each subject's class average is its total divided by the number of students. The overall class average is the mean student total out of 300; dividing it by three gives the displayed percentage. Searching does not change the class averages.

The practice boundaries are:

| Score out of 100 | Practice grade |
| --- | --- |
| 90-100 | 9 |
| 80-89 | 8 |
| 70-79 | 7 |
| 60-69 | 6 |
| 50-59 | 5 |
| 40-49 | 4 |
| 30-39 | 3 |
| 20-29 | 2 |
| 10-19 | 1 |
| 0-9 | U |

These are illustrative classroom thresholds, **not official GCSE boundaries or predictions**. Actual boundaries vary by subject, tier, board, and exam series. See [AQA's grade boundary guidance](https://www.aqa.org.uk/exams-administration/results-days/grade-boundaries). The practice thresholds are defined in `GRADE_BOUNDARIES` in `app.py`.

## Testing

After installing the dependencies, run:

```powershell
.venv\Scripts\python.exe -m unittest -v
```

On macOS/Linux use `.venv/bin/python -m unittest -v`. Tests use temporary files, leaving actual records alone. They cover adding and removing students, searching, profiles, editing, sorting, averages, input validation, grade boundaries, and escaping HTML in names.

## Limitations and lessons from the experiment

- AI-generated code still needs human understanding, review, and testing. Passing these tests does not prove the application is free of bugs or secure.
- The checks exercise Flask responses and calculations. The interface has not been visually verified in a browser, and there is no full browser accessibility test suite.
- This is a local prototype with no login, access permissions, or CSRF protection. It is not suitable for publishing as an internet-facing service or using for real school records.
- JSON file storage has no multi-user locking, backups, or recovery interface. Simultaneous writes could overwrite changes, and malformed stored data can cause errors.
- Removal has no undo, and editing replaces current scores without retaining a history.
- The terminal version has simpler input handling and can fail on invalid numeric input.
- Web fonts load from Google Fonts; system fonts are used when they are unavailable.
- This repository publishes the source code, not a hosted working website. The Flask development server is for local use.

Possible future work includes a database, score history, configurable exam-specific boundaries, stronger security, and browser-based tests. These features are not implemented.
