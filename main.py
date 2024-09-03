import sys
from qtpy.QtWidgets import QApplication
from app.routine_controller import RoutineController

def main():
    app = QApplication(sys.argv)
    controller = RoutineController()
    controller.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
