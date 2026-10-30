import sqlite3
from pathlib import Path

from student_api.schemas import StudentCreate, StudentRead


class StudentRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT
                )
                """
            )

    @staticmethod
    def _to_student(row: sqlite3.Row) -> StudentRead:
        return StudentRead(
            id=row["id"],
            name=row["name"],
            age=row["age"],
            email=row["email"],
        )

    def create(self, student: StudentCreate) -> StudentRead:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO students (name, age, email) VALUES (?, ?, ?)",
                (student.name, student.age, student.email),
            )
            row = connection.execute(
                "SELECT id, name, age, email FROM students WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        if row is None:
            raise RuntimeError("The newly created student could not be retrieved.")
        return self._to_student(row)

    def get_all(self) -> list[StudentRead]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, name, age, email FROM students ORDER BY id"
            ).fetchall()
        return [self._to_student(row) for row in rows]

    def get_by_id(self, student_id: int) -> StudentRead | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, age, email FROM students WHERE id = ?",
                (student_id,),
            ).fetchone()
        return self._to_student(row) if row is not None else None

    def delete(self, student_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM students WHERE id = ?", (student_id,)
            )
        return cursor.rowcount > 0
