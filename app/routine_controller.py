from qtpy.QtWidgets import QApplication
from app.routine_model import RoutineModel
from app.routine_view import RoutineView

class RoutineController:
    def __init__(self):
        self.model = RoutineModel()
        self.view = RoutineView()

        self.view.show_button.clicked.connect(self.show_routine)

    def show_routine(self):
        day = self.view.day_selector.currentText()
        routine = self.model.get_routine_for_day(day)
        self.view.update_routine(routine)

    def run(self):
        self.view.show()
