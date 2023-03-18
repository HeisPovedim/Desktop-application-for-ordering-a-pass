# ВИДЖЕТ - АВТОРИЗАЦИЯ
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

from interface.selection_window import SelectionWindow

# HELPERS
from helpers.regulars import *

# DATABASE
from MySQL.connect_db import DB
from data.user import User

# LIBRARIES
import hashlib

class Authorization(QMainWindow):
  def __init__(self, receiving_party):
    super().__init__()

    # Настройки окна
    self.setWindowTitle("Авторизация")
    self.setFixedSize(300, 110)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.receiving_party = receiving_party # класс "Первичное окно"
    self.input_login = None
    self.input_password = None

    # Настройка базы данных
    self.db = DB()
    self.connect = self.db.connect
    self.cursor = self.db.cursor

    self.initGUI()

  def initGUI(self):
    grid = QGridLayout(); grid.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    self.input_login = QLineEdit()
    self.input_login.textEdited.connect(
      lambda: self.input_login.setText(
        re_login(self.input_login.text())
      )
    )

    self.input_password = QLineEdit()
    self.input_password.textEdited.connect(
      lambda: self.input_password.setText(
        re_password(self.input_password.text())
      )
    )

    btn_back = QPushButton("Назад"); btn_back.clicked.connect(lambda: self.return_back())
    btn_next = QPushButton("Далее"); btn_next.clicked.connect(lambda: self.authorization())

    grid.addWidget(QLabel("Логин:"), 0, 0)
    grid.addWidget(self.input_login, 0, 1)
    grid.addWidget(QLabel("Пароль:"), 1, 0)
    grid.addWidget(self.input_password, 1, 1)
    grid.addWidget(btn_back, 2, 0)
    grid.addWidget(btn_next, 2, 1)

    self.centralWidget().setLayout(grid)

  # АВТОРИЗАЦИЯ
  def authorization(self):
    login = self.input_login.text()
    password = self.input_password.text()

    if(login and password) != "":
        hashed_password = hashlib.sha256((login + password).encode()).hexdigest()  # хеширование пароля

        # выполняем запрос к базе данных для проверки логина и пароля
        query = f"SELECT * FROM users WHERE login='{login}' AND password='{hashed_password}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result:
          QMessageBox.information(self, "Успех", "Вы вошли.")
          self.open_selection_window()
        else:
          QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
    else:
      QMessageBox.warning(self, "Ошибка", "Заполните пустые поля!")

  # ОЧИСТКА ПОЛЕЙ
  def reset_fields(self):
    self.input_login.clear()
    self.input_password.clear()

  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.db.close()
    self.reset_fields()
    self.receiving_party.show()

  # СОБЫТИЕ НА ЗАКРЫТИЕ ОКНА
  def closeEvent(self, event):
    self.close()
    self.db.close()
    self.reset_fields()
    self.receiving_party.show()

  # ПЕРЕХОД К ОКНУ ВЫБОРА
  def open_selection_window(self):
    User(self.input_login.text(), self.input_password.text())
    self.close()
    self.db.close()
    self.reset_fields()
    self.receiving_party.close()
    SelectionWindow().show()