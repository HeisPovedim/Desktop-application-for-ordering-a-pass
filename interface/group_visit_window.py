import sys
from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import (
  QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget,
  QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from helpers.helpers import *


class GroupVisit(QMainWindow):
  def __init__(self,start_window):
    super().__init__()
    
    new_window = QMainWindow(self)
    new_window.setFixedSize(600, 400)
    
    self.start_window = start_window
  
    # создаем кнопку назад и привязываем к ней событие нажатия
    self.back_button = QPushButton("Назад", new_window)
    self.back_button.move(260, 200)
    self.back_button.clicked.connect(lambda: self.show_main_window(new_window))

    # привязываем к новому окну событие закрытия окна
    new_window.closeEvent = lambda: self.show_main_window(new_window)

    # показываем новое окно
    new_window.show()
    self.hide()
    
  def show_main_window(self, new_window):
    # показываем главное окно и закрываем новое окно
    new_window.hide()
    self.start_window.show()