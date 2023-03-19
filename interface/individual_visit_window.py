from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget , QMessageBox

# WIDGETS
from interface.widgets.information_for_the_pass import InformationPass
from interface.widgets.receiving_party import ReceivingParty
from interface.widgets.visitor_information import VisitorInformation
from interface.widgets.attaching_documents import AttachingDocuments
from interface.widgets.buttons import Buttons

# HELPERS
from helpers.helpers import *

# DATABASE
from database.requests import *
from data.user import user

# LIBRARIES
from datetime import datetime
import dns.resolver
import hashlib
import re
import os

class IndividualVisit(QMainWindow):
  def __init__(self, selection_window):
    super().__init__()

    # Настройка окна
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(1000, 700)
    self.setCentralWidget(QWidget())

    # Инициализация окон и виджетов
    self.selection_window = selection_window
    self.information_for_the_pass = InformationPass()
    self.receiving_party = ReceivingParty()
    self.visitor_information = VisitorInformation(True)
    self.attaching_documents = AttachingDocuments()
    self.buttons = Buttons()

    # Настройка базы данных
    self.db = DB()
    self.connect = self.db.connect
    self.cursor = self.db.cursor

    # Получение текущего ID пользователя
    self.username = user['username']
    query = f"SELECT id FROM users WHERE login='{self.username}'"
    self.cursor.execute(query)
    self.userId = self.cursor.fetchone()

    self.initGUI()

  def initGUI(self):

    # Конфигурация Grid
    grid = QGridLayout()
    grid.addWidget(self.information_for_the_pass, 0, 0)
    grid.addWidget(self.receiving_party, 0, 1)
    grid.addWidget(self.visitor_information, 1, 0, 1, 2)
    grid.addWidget(self.attaching_documents, 2, 0)
    grid.addLayout(self.buttons, 2, 1)

    self.buttons.back_button.clicked.connect(lambda: self.show_main_window())
    self.buttons.further_button.clicked.connect(lambda: self.make_application())

    grid.setSpacing(5)
    self.centralWidget().setLayout(grid)

  # ОБРАБОТКИ ФОРМЫ
  def make_application(self):
  
    blank_fields = []  # массив, куда мы будем записывать наши не заполненные поля
    form_valid = True  # формат проверки

    # ФИО - длина макс. 3 и пустое поле
    if not check_three_words(self.receiving_party.fio.text()) or self.receiving_party.fio.text() == "":
      blank_fields.append("ФИО")
      form_valid = False

    # Быстрая валидация одинарных полей на пустоту
    array_valid = [
      [
        self.visitor_information.surname.text(),
        self.visitor_information.name.text(),
        self.visitor_information.patronymic.text(),
        self.visitor_information.note.text(),
        self.visitor_information.series.text(),
        self.visitor_information.number.text(),
      ],
      [
        "Фамилия",
        "Имя",
        "Отчество",
        "Примечание",
        "Серия паспорта",
        "Номер паспорта"
      ]
    ]
    for i in range(len(array_valid)):
      for j in range(len(array_valid[i])):
        if array_valid[i][j] == "":
          blank_fields.append(array_valid[1][j])
          form_valid = False

    # E-mail - регулярное выражение и существование доменов
    email = self.visitor_information.email.text()
    domain = email.split('@')[-1]
    if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email) is None:
      blank_fields.append("Email")
      form_valid = False
    else:
      try:
        answers = dns.resolver.resolve(domain, 'MX') # получаем MX записи домена
      except dns.resolver.NXDOMAIN:
        blank_fields.append("Email")
        form_valid = False
        answers = 0

      # проверяем, есть ли хотя бы один адрес сервера в ответе
      if answers and len(answers) <= 0:
        blank_fields.append("Email")
        form_valid = False

    # Прикрепление фото - пустая строка и ничего не выбрано
    if self.visitor_information.file_photo is None or self.visitor_information.file_photo == "":
      self.visitor_information.file_photo = None

    # Прикрепление документа - пустая строка и ничего не выбрано
    if self.attaching_documents.file_document is None or self.attaching_documents.file_document == "":
      blank_fields.append("Прикрепите документы")
      self.attaching_documents.file_document = None
      form_valid = False

    # Основная валидация с последующей записью в БД
    if not form_valid:
      message = "\n".join(blank_fields)
      QMessageBox.warning(self, "Заполните поля", message)
    elif form_valid:
      # Cохранение документов на компьютере
      if self.attaching_documents.file_document:
        file_path = os.path.join(
          "D:/Project/GitHub/Desktop-application-for-ordering-a-pass/assets/files/individual_visit_window/pdf",
          hashlib.sha256((self.username + f'{datetime.now():%Y-%m-%d %H-%M-%S%z}').encode()).hexdigest() + ".pdf"
        )
        try:
          with open(self.attaching_documents.file_document, 'rb') as file:
            data = file.read()
          with open(file_path, 'ab') as file:
            file.write(data)
          print("Файлы успешно сохранены.")
        except Exception as error:
          QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файлы: {error}")

      # Номер - убираем лишние символы и проверяем длину номера
      phone_valid = ""
      if len(re.sub(r'[^\d+]', '', self.visitor_information.phone.text())) == 12:
        phone_valid = re.sub(r'[^\d+]', '', self.visitor_information.phone.text())

      # Последовательное добавление данных в БД
      addIndividualVisits(
        self.information_for_the_pass.dateWith.date().toString("yyyy-MM-dd"),
        self.information_for_the_pass.dateAbout.date().toString("yyyy-MM-dd"),
        self.information_for_the_pass.comboBox.currentText(),
        self.receiving_party.comboBox.currentText(),
        self.receiving_party.fio.text(),
        self.visitor_information.surname.text(),
        self.visitor_information.name.text(),
        self.visitor_information.patronymic.text(),
        phone_valid,
        self.visitor_information.email.text(),
        self.visitor_information.organization.text(),
        self.visitor_information.note.text(),
        self.visitor_information.birthdate.date().toString("yyyy-MM-dd"),
        self.visitor_information.series.text(),
        self.visitor_information.number.text(),
        hashlib.sha256((self.username + f'{datetime.now():%Y-%m-%d %H-%M-%S%z}').encode()).hexdigest(),
        self.visitor_information.file_photo,
        f'{datetime.now():%Y-%m-%d %H-%M-%S%z}'
      )
      
      QMessageBox.warning(self, "Успех", "Валидация прошла успешно")

  # ВОЗВРАЩЕНИЕ В ГЛАВНОЕ МЕНЮ
  def show_main_window(self):
    self.close()
    self.selection_window.show()
