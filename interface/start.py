from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow, QWidget

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

    # создаем картинки и подписи
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

    # привязываем к картинкам события
    self.label1.mousePressEvent = lambda event: self.individual_visit_window()
    self.label2.mousePressEvent = lambda event: self.group_visit_window()
  
  def individual_visit_window(self):
    self.hide()
    PersonalWindow(self).show()
    
  def group_visit_window(self):
    self.hide()
    group_page = GroupVisit(self)