# EcoTrack - Smart Waste Reporting System

## Project Overview
EcoTrack is a Flask-based web application that allows users to report waste by entering a location, waste type, and description.

## Features
- Submit waste reports
- Store reports using SQLite
- View submitted reports
- Health-check endpoint
- Automated application tests
- Docker containerization

## Technologies Used
- Python
- Flask
- SQLite
- unittest
- Docker

## Run Locally
1. Install Python.
2. Install dependencies:

   pip install -r requirements.txt

3. Start the application:

   python -m flask --app app run --debug

4. Open http://127.0.0.1:5000

## Health Check
Visit http://127.0.0.1:5000/health

## Run Tests
python -m unittest test_app.py

## Build Docker Image
docker build -t ecotrack:1.0 .

## Run Docker Container
docker run -d --name ecotrack-app -p 5000:5000 ecotrack:1.0

Open http://localhost:5000 to access the application.
