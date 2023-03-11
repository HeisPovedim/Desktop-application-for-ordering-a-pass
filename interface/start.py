from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import (
  QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget,
  QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from helpers.capitalize_text import capitalize_text

from interface.individual_visit_window import PersonalWindow
from interface.group_visit_window import GroupVisit

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
  # задаем фиксированный размер главного окна и его заголовок
    self.setWindowTitle("IDVisitor")
    self.setWindowIcon(QIcon("./img/icon.png"))
    self.setFixedSize(600, 400)

    # создаем виджет, на котором будут расположены картинки и подписи
    widget = QWidget(self)
    self.setCentralWidget(widget)

    # создаем лейблы для каждой картинки и подписи
    self.label1 = QLabel(widget)
    self.label1.setPixmap(QPixmap("./img/one.jpg").scaled(250, 250, transformMode= Qt.TransformationMode.SmoothTransformation))
    self.label1.move(25, 50)
    self.caption1 = QLabel("Личное посещение", widget)
    self.caption1.move(105, 315)

    self.label2 = QLabel(widget)
    self.label2.setPixmap(QPixmap("./img/group.jpg").scaled(250, 250, transformMode = Qt.TransformationMode.SmoothTransformation))
    self.label2.move(325, 50)
    self.caption2 = QLabel("Групповое посещение", widget)
    self.caption2.move(405, 315)

    # привязываем к лейблам события нажатия на них
    self.label1.mousePressEvent = lambda event: self.individual_visit_window()
    self.label2.mousePressEvent = lambda event: self.group_visit_window()
  
  def individual_visit_window(self):
    self.hide()
    personal_page = PersonalWindow(self)
    
  def group_visit_window(self):
    self.hide()
    group_page = GroupVisit(self)
    
