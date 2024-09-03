import sqlite3

class Database:
    def __init__(self, db_name='routine.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Routine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            activity TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_routine(self, day, time, activity):
        self.cursor.execute('''
        INSERT INTO Routine (day, time, activity)
        VALUES (?, ?, ?)
        ''', (day, time, activity))
        self.conn.commit()

    def get_routine_by_day(self, day):
        self.cursor.execute('SELECT time, activity FROM Routine WHERE day = ?', (day,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
      
