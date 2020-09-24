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


class SQLiteCursor:
    def __init__(self, filename: str):
        self.filename = filename
        self.cursor = None
        self.connection = None
    
    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()