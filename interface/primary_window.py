from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout

# WIDGETS
from interface.widgets.authorization import Authorization
from interface.widgets.registrations import Registrations

class PrimaryWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Настройки окна
    self.setWindowTitle("Первичное окно")
    self.setFixedSize(300, 300)
    self.setCentralWidget(QWidget())
    # Инициализация переменных
    self.buttons = None

    self.initGUI()

  def initGUI(self):
    self.buttons = QGridLayout(); self.buttons.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    auth_btn = QPushButton("Авторизация"); auth_btn.setFixedSize(150, 100)
    reg_btn = QPushButton("Регистрация"); reg_btn.setFixedSize(150, 100)

    auth_btn.clicked.connect(lambda: self.authorization())
    reg_btn.clicked.connect(lambda: self.registration())

    self.buttons.addWidget(auth_btn)
    self.buttons.addWidget(reg_btn)

    self.centralWidget().setLayout(self.buttons)

  # ОТКРЫТИЕ ОКНА АВТОРИЗАЦИИ
  def authorization(self):
    self.hide()
    Authorization(self).show()

  # ОТКРЫТИЕ ОКНА РЕГИСТРАЦИИ
  def registration(self):
    self.hide()
    Registrations(self).show()