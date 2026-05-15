# AI Request Tracker

A simple web application to track AI project requests from team members. Built with Python, Flask, SQLite, and Bootstrap.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Chart.js
- **Backend:** Python + Flask
- **Database:** SQLite

## Setup Instructions

1. Make sure Python 3 is installed on your machine
2. Clone or download this repository
3. Navigate to the project folder in your terminal
4. Install dependencies: pip3 install flask flask-cors flask-sqlalchemy
5. Run the application: python3 app.py
6. Open your browser and go to: `http://127.0.0.1:5000`

## How to Use

- **Submit a request:** Fill out the form at the main page and click Submit
- **View dashboard:** Go to `/dashboard` to see all requests, filter by department or status, and update request statuses
- **View details:** Click any row in the dashboard table to see full request details

## Known Limitations
- No authentication — everyone has committee access
- No pagination — works best for under 100 requests
- Local deployment only unless hosted on a server