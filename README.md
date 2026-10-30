# Student API

A backend-only REST API for adding, listing, looking up, and deleting students. Student records are stored in a local SQLite database.

## Requirements

- Python 3.10 or newer
- Packages listed in `requirements.txt`

## Setup

Run these commands from the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents virtual environment activation, run the commands using `.\.venv\Scripts\python.exe` instead.

## Run the application

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`; alternative ReDoc documentation is at `http://127.0.0.1:8000/redoc`.

The SQLite database is created at `data/students.db` on first run. To use a different file, set `STUDENT_DB_PATH` before starting the application:

```powershell
$env:STUDENT_DB_PATH = "D:\path\to\students.db"
uvicorn main:app --reload
```

## API endpoints

| Method | URL | Description |
| --- | --- | --- |
| `POST` | `http://127.0.0.1:8000/students` | Add a student |
| `GET` | `http://127.0.0.1:8000/students` | View all students |
| `GET` | `http://127.0.0.1:8000/students/{student_id}` | View one student by ID |
| `DELETE` | `http://127.0.0.1:8000/students/{student_id}` | Delete a student |

You can open the `GET` URLs directly in a browser. Use Postman or the interactive `/docs` page for `POST` and `DELETE`.

### Add a student

In Postman, choose **POST**, enter `http://127.0.0.1:8000/students`, select **Body > raw > JSON**, and send:

```json
{
  "name": "Alex Morgan",
  "age": 20,
  "email": "alex@example.com"
}
```

`email` is optional and may be omitted or set to `null`. Names must contain 1–100 non-whitespace characters, ages must be between 1 and 150, and a supplied email must be valid.

Successful creation returns `201 Created`, including the generated `id`:

```json
{
  "id": 1,
  "name": "Alex Morgan",
  "age": 20,
  "email": "alex@example.com"
}
```

### View students

- Open `http://127.0.0.1:8000/students` in a browser or send a **GET** request in Postman to list all students.
- Replace `{student_id}` in `http://127.0.0.1:8000/students/{student_id}` with the ID returned when creating a student, then open it in a browser or send a **GET** request.

### Delete a student

Send a **DELETE** request in Postman to `http://127.0.0.1:8000/students/{student_id}`. A successful deletion returns `204 No Content`; an unknown ID returns `404 Not Found`.

## Run tests

```powershell
python -m pytest
```
