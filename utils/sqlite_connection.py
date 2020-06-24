import sqlite3


class SQLiteConnection:
    def __init__(self, filename: str):
        self.filename = filename
        self.connection = None

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.filename)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
