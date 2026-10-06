# Attendance Tracker

Mini REST application for ASDD Practical 10.

## Required endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/items` | View attendance records |
| POST | `/items` | Add an attendance record |
| GET | `/health` | Check application health |

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

- http://127.0.0.1:5000/items
- http://127.0.0.1:5000/health

## Run tests

```bash
pytest
```

Expected result: all tests pass.

## Attendance JSON format

```json
{
  "student_id": 101,
  "student_name": "Rohit",
  "date": "2026-10-06",
  "status": "Present"
}
```

## Jira

Replace the example Jira issue keys in Git commit messages with the actual keys created by R1.
