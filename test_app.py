"""Flask integration checks that never use real student records."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as tracker


class GradeTrackerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        data_patch = patch.object(tracker, "DATA_FILE", Path(self.directory.name) / "students.json")
        data_patch.start()
        self.addCleanup(data_patch.stop)
        config_patch = patch.dict(tracker.app.config, TESTING=True)
        config_patch.start()
        self.addCleanup(config_patch.stop)
        self.client = tracker.app.test_client()

    def add_student(self, name="Harry", maths=60, english=70, science=80):
        return self.client.post("/", data=dict(name=name, maths=maths, english=english, science=science))

    def test_empty_class_and_stylesheet(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        response = self.client.get("/static/style.css")
        self.assertEqual(response.status_code, 200)
        response.close()
        self.assertTrue(all(value is None for value in tracker.average([]).values()))

    def test_add_persistence_and_averages(self):
        self.assertEqual(self.add_student().status_code, 302)
        self.add_student("Alex", 80, 90, 100)
        self.assertEqual(len(tracker.load_students()), 2)
        self.assertEqual(tracker.average(tracker.load_students()), dict(maths=70, english=80, science=90))
        self.assertIn("240.00", self.client.get("/").get_data(as_text=True))

    def test_ranking_and_search_keep_class_averages(self):
        self.add_student("Low", 10, 10, 10)
        self.add_student("High", 90, 90, 90)
        page = self.client.get("/").get_data(as_text=True)
        self.assertLess(page.index("High</a>"), page.index("Low</a>"))
        results = self.client.get("/?q=HI").get_data(as_text=True)
        self.assertIn("High</a>", results)
        self.assertNotIn("Low</a>", results)
        self.assertIn("150.00", results)
        self.assertIn("No matching students", self.client.get("/?q=absent").get_data(as_text=True))

    def test_profile_edit_updates_saved_scores_and_ranking(self):
        self.add_student("Harry", 20, 20, 20)
        self.add_student("Alex", 50, 50, 50)
        student = tracker.load_students()[0]
        path = f"/students/{student['id']}"
        self.assertEqual(self.client.get(path).status_code, 200)
        result = self.client.post(path, data=dict(maths=90, english=80, science=70), follow_redirects=True)
        self.assertIn("Practice grade 9", result.get_data(as_text=True))
        self.assertEqual(tracker.load_students()[0]["maths"], 90)
        page = self.client.get("/").get_data(as_text=True)
        self.assertLess(page.index("Harry</a>"), page.index("Alex</a>"))
        self.assertEqual(self.client.get("/students/missing").status_code, 404)

    def test_invalid_scores_are_rejected_without_partial_edits(self):
        self.add_student()
        path = f"/students/{tracker.load_students()[0]['id']}"
        for value in ("101", "-1", "3.5", "abc", ""):
            with self.subTest(value=value):
                self.assertEqual(self.add_student(maths=value).status_code, 400)
                self.assertEqual(self.client.post(path, data=dict(maths=value, english=99, science=99)).status_code, 400)
        self.assertEqual(len(tracker.load_students()), 1)
        self.assertEqual(tracker.load_students()[0]["english"], 70)
        self.assertEqual(self.add_student(name=" ").status_code, 400)

    def test_removal_uses_identity_with_duplicate_names(self):
        self.add_student("Same", 20, 20, 20)
        self.add_student("Same", 80, 80, 80)
        target = tracker.load_students()[1]
        path = f"/students/{target['id']}/remove"
        self.assertEqual(self.client.get(path).status_code, 405)
        self.assertEqual(self.client.post(path).status_code, 302)
        self.assertEqual([student["maths"] for student in tracker.load_students()], [20])
        self.assertEqual(self.client.post(path).status_code, 404)

    def test_legacy_records_keep_their_assigned_ids(self):
        tracker.save_students([dict(name="Legacy", maths=50, english=60, science=70)])
        first = tracker.load_students()[0]["id"]
        self.assertEqual(tracker.load_students()[0]["id"], first)

    def test_grade_boundaries(self):
        for score in range(101):
            with self.subTest(score=score):
                expected = str(min(score // 10, 9)) if score >= 10 else "U"
                self.assertEqual(tracker.grade(score), expected)

    def test_names_are_escaped_in_html(self):
        self.add_student("<script>alert(1)</script>")
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>alert(1)</script>", page)


if __name__ == "__main__":
    unittest.main()
