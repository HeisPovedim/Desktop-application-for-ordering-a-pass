from PyQt6.QtWidgets import QApplication
from interface.start import MainWindow

from interface.individual_visit_window import PersonalWindow

# ВЫЗОВ СКРИПТА ТОЛЬКО В ЭТОМ ФАЙЛЕ
if __name__ == "__main__":
    app = QApplication([])
    MainWindow().show()
    app.exec()