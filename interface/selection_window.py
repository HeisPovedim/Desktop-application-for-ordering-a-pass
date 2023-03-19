from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton

from interface.widgets.photo_and_signature import PhotoAndSignature
from interface.individual_visit_window import PersonalWindow
from interface.group_visit_window import GroupVisit

from data.user import user

class SelectionWindow(QMainWindow):
  def __init__(self, primary_window):
    super().__init__()

    # Создаем новое окно и задаем ему фиксированный размер с заголовком
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(600, 400)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.photo_and_signature = PhotoAndSignature()
    self.primary_window = primary_window
    self.group_signature = None
    self.group_photo = None
    self.individual_signature = None
    self.individual_photo = None

    self.initGUI()

  def initGUI(self):
    grid = QGridLayout()

    grid.addLayout(self.photo_and_signature, 0, 0)
    self.photo_and_signature.individual_photo.mousePressEvent = lambda event: self.individual_visit_window()
    self.photo_and_signature.group_photo.mousePressEvent = lambda event: self.group_visit_window()

    button = QPushButton("Назад"); button.setFixedHeight(30)
    button.clicked.connect(lambda: self.return_back())
    grid.addWidget(button, 1, 0)

    self.centralWidget().setLayout(grid)

  def individual_visit_window(self):
    self.close()
    PersonalWindow(self).show()

  def group_visit_window(self):
    self.close()
    GroupVisit(self).show()

  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    user["username"] = ""
    self.primary_window.show()