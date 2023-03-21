from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt6.QtGui import QIcon

# WIDGETS
from interface.widgets.photo_and_signature import PhotoAndSignature

# WINDOW
from interface.personal_visit import PersonalVisit
from interface.personal_account import PersonalAccount
from interface.group_visit import GroupVisit

# DATA
from data.user import user

class SelectionWindow(QMainWindow):
  def __init__(self, primary_window):
    super().__init__()

    # Настройки окна
    self.setWindowTitle("IDVisitor")
    self.setWindowIcon(QIcon('./assets/img/icon.png'))
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

    grid.addLayout(self.photo_and_signature, 0, 0, 1, 2)
    self.photo_and_signature.individual_photo.mousePressEvent = lambda event: self.personal_visit_window()
    self.photo_and_signature.group_photo.mousePressEvent = lambda event: self.group_visit_window()

    button_back = QPushButton("Назад"); button_back.setFixedHeight(30)
    button_back.clicked.connect(lambda: self.return_back())
    grid.addWidget(button_back, 1, 0)
    
    button_personal_account = QPushButton("Личный кабинет"); button_personal_account.setFixedHeight(30)
    button_personal_account.clicked.connect(lambda: self.personal_account_show())
    grid.addWidget(button_personal_account, 1, 1)

    self.centralWidget().setLayout(grid)

  def personal_visit_window(self):
    self.close()
    PersonalVisit(self).show()

  def group_visit_window(self):
    self.close()
    GroupVisit(self).show()

  def personal_account_show(self):
    self.close()
    PersonalAccount(self).show()

  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    user["username"] = ""
    self.primary_window.show()