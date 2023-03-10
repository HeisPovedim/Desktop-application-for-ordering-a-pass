from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import (
  QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget,
  QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from helpers.capitalize_text import capitalize_text
from interface.start import MainWindow

# #: ВЫЗОВ КОДА ТОЛЬКО В ЭТОМ ФАЙЛЕ ЕСЛИ ОН ЯВЛЯЕТСЯ ИСПОЛНЯЕМЫМ
if __name__ == "__main__":
  app = QApplication([])
  MainWindow().show()
  app.exec()