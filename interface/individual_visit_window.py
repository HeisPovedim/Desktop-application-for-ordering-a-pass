# PYQT6
from PyQt6.QtWidgets import (
  QMainWindow, QPushButton, QGridLayout, QWidget,
  QHBoxLayout, QMessageBox
)

# WIDGETS
from interface.widgets.information_for_the_pass import InformationPass
from interface.widgets.receiving_party import ReceivingParty
from interface.widgets.visitor_information import VisitorInformation
from interface.widgets.attaching_documents import AttachingDocuments

# HELPERS
from helpers.helpers import *

# DATABASE
from MySQL.connect_db import DB

# LIBRARIES
from datetime import datetime
import dns.resolver
import re
import os

class PersonalWindow(QMainWindow):
  def __init__(self, start_window):
    super().__init__()
    
    # Создаем новое окно и задаем ему фиксированный размер с заголовком
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(1000, 700)
    self.setCentralWidget(QWidget())
    
    # Инициализация окон и виджетов
    self.start_window = start_window
    self.information_for_the_pass = InformationPass()
    self.receiving_party = ReceivingParty()
    self.visitor_information = VisitorInformation()
    self.attaching_documents = AttachingDocuments()
    
    # Настройка базы данных
    self.db = DB()
    self.connect = self.db.connect
    self.cursor = self.db.cursor
    
    self.initGUI()
    
  def initGUI(self):
    # @: блок кнопок
    buttons = QHBoxLayout()
  
    back_button = QPushButton("Назад")  # кнопка "Назад"
    back_button.setFixedWidth(80)
    back_button.clicked.connect(lambda: self.show_main_window())
  
    further_button = QPushButton("Оформить заявку")  # кнопка "Оформить заявку"
    further_button.setFixedWidth(120)
    further_button.clicked.connect(lambda: self.make_application())
  
    buttons.addWidget(back_button)
    buttons.addWidget(further_button)
    
    # конфигурация QGridLayout
    grid = QGridLayout()
    grid.addWidget(self.information_for_the_pass, 0, 0)  # информация для пропуска
    grid.addWidget(self.receiving_party, 0, 1)           # принимающая сторона
    grid.addWidget(self.visitor_information, 1, 0, 1, 2) # информация о посетителе
    grid.addWidget(self.attaching_documents, 2, 0)       # прикрепляемые документы
    grid.addLayout(buttons, 2, 1)
    
    grid.setSpacing(5)
    self.centralWidget().setLayout(grid)
    
  # ОБРАБОТКИ ФОРМЫ
  def make_application(self):
    blank_fields = [] # массив, куда мы будем записывать наши не заполненные поля
    form_valid = True # формат проверки

    # ФИО | валидация
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
    
    # E-mail | валидация
    email = self.visitor_information.email.text()
    domain = email.split('@')[-1]
    if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email) is None:
      blank_fields.append("Email")
      form_valid = False
    else:
      # получаем MX записи домена
      try:
        answers = dns.resolver.resolve(domain, 'MX')
      except dns.resolver.NXDOMAIN:
        blank_fields.append("Email")
        form_valid = False
        answers = 0

      # проверяем, есть ли хотя бы один адрес сервера в ответе
      if answers and len(answers) <= 0:
        blank_fields.append("Email")
        form_valid = False
    
    # Прикрепление фото | валидация
    if self.visitor_information.file_photo is None or self.visitor_information.file_photo == "":
      self.visitor_information.file_photo = None
    
    # Прикрепление документа | валидация
    if self.attaching_documents.file_document is None or self.attaching_documents.file_document == "":
      blank_fields.append("Прикрепите документы")
      self.attaching_documents.file_document=None
      form_valid = False
    
    # Валидация формы
    if not form_valid:
      message = "\n".join(blank_fields)
      QMessageBox.warning(self, "Заполните поля", message)
    elif form_valid:
      # Cохранение документов на компьютере
      if self.attaching_documents.file_document:
        file_path = os.path.join(
          "D:/GitHub/Web-service-for-ordering-a-pass/files/individual_visit_window/pdf_files",
          f'{datetime.now():%Y-%m-%d %H-%M-%S%z}.pdf'
        )
        try:
          with open( self.attaching_documents.file_document, 'rb') as file:
            data = file.read()
          with open(file_path, 'ab') as file:
            file.write(data)
          print("Файлы успешно сохранены.")
        except Exception as error:
          QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файлы: {error}")
      
      # Номер | валидация
      phone_valid = ""
      if len(re.sub(r'[^\d+]', '', self.visitor_information.phone.text())) == 12:
        phone_valid = re.sub(r'[^\d+]', '', self.visitor_information.phone.text())
      
      # Сохранение в базу данных
      sql = "INSERT INTO personal_visit(" \
            "validity_period_from," \
            "validity_period_for," \
            "purpose_of_the_visit," \
            "division," \
            "FIO," \
            "surname," \
            "name," \
            "patronymic," \
            "phone," \
            "email," \
            "organization," \
            "note,birthdate," \
            "passport_series," \
            "passport_number," \
            "document_name," \
            "document_unique_name," \
            "photo" \
            ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (
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
        self.attaching_documents.file_document_name,
        f'{datetime.now():%Y-%m-%d %H-%M-%S%z}',
        self.visitor_information.file_photo
      )
      self.cursor.execute(sql,val)
      self.connect.commit()
      QMessageBox.warning(self, "Успех", "Валидация прошла успешно")

  # ВОЗВРАЩЕНИЕ В ГЛАВНОЕ МЕНЮ
  def show_main_window(self):
    self.start_window.show()
    self.hide()

  # СОБЫТИЕ НА ЗАКРЫТИЕ ОКНА
  def closeEvent(self, event):
    self.start_window.show()
    self.hide()