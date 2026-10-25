
import unittest
import os
import sqlite3
import tempfile
import app as ecotrack


class EcoTrackTests(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.test_database = self.temp_file.name

        ecotrack.DATABASE = self.test_database
        ecotrack.init_db()

        ecotrack.app.config["TESTING"] = True
        self.client = ecotrack.app.test_client()

    def tearDown(self):
        ecotrack.DATABASE = "ecotrack.db"

        if os.path.exists(self.test_database):
            try:
                os.remove(self.test_database)
            except PermissionError:
                pass

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"EcoTrack", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_submit_report(self):
        response = self.client.post("/report", data={
            "location": "College Campus",
            "waste_type": "Overflowing bin",
            "description": "Dustbin is full"
        })
        self.assertEqual(response.status_code, 302)

        page = self.client.get("/")
        self.assertIn(b"College Campus", page.data)
        self.assertIn(b"Overflowing bin", page.data)

    def test_empty_report_rejected(self):
        response = self.client.post("/report", data={
            "location": "",
            "waste_type": "Overflowing bin",
            "description": "Dustbin is full"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
