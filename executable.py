from PyQt6.QtWidgets import QApplication
from interface.primary_window import PrimaryWindow

# ВЫЗОВ СКРИПТА ТОЛЬКО В ЭТОМ ФАЙЛЕ
if __name__ == "__main__":
    app = QApplication([])
    window = PrimaryWindow()
    window.show()
    app.exec()