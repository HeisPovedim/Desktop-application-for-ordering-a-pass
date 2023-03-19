# ВИДЖЕТ - РЕГИСТРАЦИЯ
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

# HELPERS
from helpers.regulars import *

# DATABASE
from MySQL.connect_db import DB

# LIBRARIES
import hashlib

class Registrations(QMainWindow):
  def __init__(self, receiving_party):
    super().__init__()

    # Настройки окна
    self.setWindowTitle("Регистрация")
    self.setFixedSize(300, 130)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.receiving_party = receiving_party  # класс "Первичное окно"
    self.input_login = None
    self.input_password = None
    self.input_repeat_password = None

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

    self.input_repeat_password = QLineEdit()
    self.input_repeat_password.textEdited.connect(
      lambda: self.input_repeat_password.setText(
        re_password(self.input_repeat_password.text())
      )
    )

    btn_back = QPushButton("Назад"); btn_back.clicked.connect(lambda: self.return_back())
    btn_next = QPushButton("Далее"); btn_next.clicked.connect(lambda: self.registrations())

    grid.addWidget(QLabel("Логин:"), 0, 0)
    grid.addWidget(self.input_login, 0, 1)
    grid.addWidget(QLabel("Пароль:"), 1, 0)
    grid.addWidget(self.input_password, 1, 1)
    grid.addWidget(QLabel("Повторите пароль:"), 2, 0)
    grid.addWidget(self.input_repeat_password, 2, 1)
    grid.addWidget(btn_back, 3, 0)
    grid.addWidget(btn_next, 3, 1)

    self.centralWidget().setLayout(grid)

  # АВТОРИЗАЦИЯ
  def registrations(self):
    login = self.input_login.text()
    password = self.input_password.text()
    repeat_password = self.input_repeat_password.text()

    if (login and password and repeat_password) != "":
      if password == repeat_password:
        hashed_password = hashlib.sha256((login + password).encode()).hexdigest()  # хеширование пароля

        # запрос на регистрацию нового пользователя
        query = f"INSERT INTO users (login, password) VALUES ('{login}', '{hashed_password}')"

        # проверяем, что пользователь с таким логином еще не зарегистрирован
        check_query = f"SELECT * FROM users WHERE login='{login}'"
        self.cursor.execute(check_query)
        result = self.cursor.fetchone()

        if result:
          QMessageBox.warning(self, "Ошибка", "Пользователь уже зарегистрирован!")
        else:
          # если пользователь не зарегистрирован, добавляем его в базу данных
          register_query = f"INSERT INTO users (login, password) VALUES ('{login}', '{hashed_password}')"
          self.cursor.execute(register_query)
          self.db.commit()

          QMessageBox.information(self, "Успех", "Вы зарегистрировались.")
          self.db.close()
      else:
        QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
    else:
      QMessageBox.warning(self, "Ошибка", "Заполните пустые поля!")

  # ОЧИСТКА ПОЛЕЙ
  def reset_fields(self):
    self.input_login.clear()
    self.input_password.clear()
    self.input_repeat_password.clear()

  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.db.close()
    self.reset_fields()
    self.receiving_party.show()