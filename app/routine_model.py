from app.database import Database

class RoutineModel:
    def __init__(self):
        self.db = Database()

    def get_routine_for_day(self, day):
        return self.db.get_routine_by_day(day)

    def close(self):
        self.db.close()
