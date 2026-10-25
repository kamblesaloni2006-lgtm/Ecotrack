
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
reports = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>EcoTrack - Waste Reporting</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f7f2;
            margin: 0;
            padding: 25px;
            color: #24372b;
        }
        main {
            max-width: 800px;
            margin: auto;
        }
        .card {
            background: white;
            padding: 22px;
            margin: 18px 0;
            border-radius: 14px;
            box-shadow: 0 3px 12px #00000010;
        }
        input, select, textarea, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 7px 0;
            border: 1px solid #ccd9ce;
            border-radius: 7px;
        }
        button {
            background: #21834b;
            color: white;
            border: none;
            cursor: pointer;
        }
        h1 { color: #176638; }
        .status { color: #21834b; font-weight: bold; }
    </style>
</head>
<body>
<main>
    <h1>🌱 EcoTrack</h1>
    <p>Report waste. Improve our environment.</p>

    <section class="card">
        <h2>Report a Waste Problem</h2>
        <form method="POST" action="/report">
            <input name="location" placeholder="Location" required>
            <select name="waste_type" required>
                <option value="">Select waste type</option>
                <option>Overflowing bin</option>
                <option>Plastic waste</option>
                <option>Food waste</option>
                <option>Illegal dumping</option>
                <option>Other</option>
            </select>
            <textarea name="description"
                placeholder="Describe the problem" required></textarea>
            <button type="submit">Submit Report</button>
        </form>
    </section>

    <section class="card">
        <h2>Waste Reports ({{ reports|length }})</h2>
        {% for r in reports %}
        <div class="card">
            <h3>{{ r.waste_type }}</h3>
            <p><b>Location:</b> {{ r.location }}</p>
            <p>{{ r.description }}</p>
            <p class="status">Status: {{ r.status }}</p>
        </div>
        {% else %}
        <p>No reports yet. Add your first report above!</p>
        {% endfor %}
    </section>
</main>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, reports=reports)

@app.route("/report", methods=["POST"])
def report():
    reports.append({
        "location": request.form["location"].strip(),
        "waste_type": request.form["waste_type"],
        "description": request.form["description"].strip(),
        "status": "Reported"
    })
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
