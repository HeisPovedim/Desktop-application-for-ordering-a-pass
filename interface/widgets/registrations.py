# ВИДЖЕТ - РЕГИСТРАЦИЯ
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QRegularExpression

# HELPERS
from helpers.regulars import *

# DATABASE
from database.connect import DB

# LIBRARIES
import dns.resolver
import hashlib

class Registrations(QMainWindow):
  def __init__(self, receiving_party):
    super().__init__()

    # Настройки окна
    self.setWindowTitle("Регистрация")
    self.setFixedSize(300, 160)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.receiving_party = receiving_party  # класс "Первичное окно"
    self.input_login = None
    self.input_email = None
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

    self.input_email = QLineEdit()
    self.input_email.setValidator(QRegularExpressionValidator(
      QRegularExpression(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    ))

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
    grid.addWidget(QLabel("Email:"), 1, 0)
    grid.addWidget(self.input_email, 1, 1)
    grid.addWidget(QLabel("Пароль:"), 2, 0)
    grid.addWidget(self.input_password, 2, 1)
    grid.addWidget(QLabel("Повторите пароль:"), 3, 0)
    grid.addWidget(self.input_repeat_password, 3, 1)
    grid.addWidget(btn_back, 4, 0)
    grid.addWidget(btn_next, 4, 1)

    self.centralWidget().setLayout(grid)

  # АВТОРИЗАЦИЯ
  def registrations(self):
    login = self.input_login.text()
    email = self.input_email.text()
    password = self.input_password.text()
    repeat_password = self.input_repeat_password.text()

    if (login and email and password and repeat_password) != "":
      if (len(password) and len(repeat_password)) >= 8:
        if password == repeat_password:
    
          # Проверка email на существования домена
          domain = email.split('@')[-1]
          if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email) is None:
            QMessageBox.warning(self, 'Email', 'Неправильный формат!')
            return
          else:
            try:
              answers = dns.resolver.resolve(domain, 'MX')  # получаем MX записи домена
            except dns.resolver.NXDOMAIN:
              QMessageBox.warning(self, 'Email', 'Такой домен не найден!')
              answers = 0
              return
            
            # проверяем, есть ли хотя бы один адрес сервера в ответе
            if answers and len(answers) <= 0:
              QMessageBox.warning(self, 'Email', 'Такой домен не найден!')
              return
          
          hashed_password = hashlib.sha256((login + password).encode()).hexdigest() # хеширование пароля
  
          # проверяем, что пользователь с таким логином еще не зарегистрирован
          check_query = f"SELECT * FROM users WHERE login='{login}'"
          self.cursor.execute(check_query)
          result = self.cursor.fetchone()
  
          if result:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже зарегистрирован!")
          else:
            # если пользователь не зарегистрирован, добавляем его в базу данных
            register_query = f"INSERT INTO users (email, login, password) VALUES ('{email}', '{login}', '{hashed_password}')"
            self.cursor.execute(register_query)
            self.db.commit()
  
            self.return_back()
            QMessageBox.information(self, "Успех", "Вы зарегистрировались.")
        else:
          QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
      else:
        QMessageBox.warning(self, "Ошибка", "Не менее 8 символов в пароле!")
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