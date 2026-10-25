
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = "ecotrack.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                waste_type TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Reported'
            )
        """)


@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as conn:
        reports = conn.execute(
            "SELECT id, location, waste_type, description, status "
            "FROM reports ORDER BY id DESC"
        ).fetchall()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EcoTrack</title>
        <style>
            body {
                font-family: Arial;
                max-width: 850px;
                margin: 35px auto;
                padding: 20px;
                background: #f0f7f2;
            }
            h1 { color: #176b45; }
            input, textarea, button {
                display: block;
                width: 100%;
                box-sizing: border-box;
                margin: 10px 0;
                padding: 12px;
            }
            button {
                background: #176b45;
                color: white;
                border: 0;
                cursor: pointer;
            }
            .report {
                background: white;
                padding: 12px;
                margin: 12px 0;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <h1>🌱 EcoTrack</h1>
        <p>Report waste problems in your community.</p>

        <form action="/report" method="post">
            <input name="location" placeholder="Location" required>
            <input name="waste_type" placeholder="Waste type" required>
            <textarea name="description"
                placeholder="Describe the problem" required></textarea>
            <button type="submit">Submit Report</button>
        </form>

        <h2>Submitted Reports</h2>
        {% for r in reports %}
        <div class="report">
            <strong>Report #{{ r[0] }} — {{ r[4] }}</strong>
            <p><b>Location:</b> {{ r[1] }}</p>
            <p><b>Waste type:</b> {{ r[2] }}</p>
            <p>{{ r[3] }}</p>
        </div>
        {% else %}
        <p>No reports submitted yet.</p>
        {% endfor %}
    </body>
    </html>
    """, reports=reports)


@app.route("/report", methods=["POST"])
def report():
    location = request.form.get("location", "").strip()
    waste_type = request.form.get("waste_type", "").strip()
    description = request.form.get("description", "").strip()

    if not location or not waste_type or not description:
        return "All fields are required.", 400

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO reports (location, waste_type, description) "
            "VALUES (?, ?, ?)",
            (location, waste_type, description)
        )

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "healthy"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
