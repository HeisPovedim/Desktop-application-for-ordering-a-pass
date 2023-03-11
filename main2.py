from PyQt6.QtWidgets import QApplication
from interface.start import MainWindow

# ВЫЗОВ КОДА ТОЛЬКО В ЭТОМ ФАЙЛЕ ЕСЛИ ОН ЯВЛЯЕТСЯ ИСПОЛНЯЕМЫМ
if __name__ == "__main__":
  app = QApplication([])
  MainWindow().show()
  app.exec()