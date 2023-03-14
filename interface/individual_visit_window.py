import os

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QPixmap, QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import (
  QLabel, QMainWindow, QPushButton, QGridLayout, QGroupBox, QFormLayout, QWidget,
  QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QVBoxLayout, QMessageBox
)

# HELPERS
from helpers.helpers import *

# Database
from MySQL.connect_db import DB

# БИБЛИОТЕКИ
import dns.resolver
import re

class PersonalWindow(QMainWindow):
  def __init__(self, start_window):
    super().__init__()

    self.file_names = None
    self.visitorInformation_birthdate = None
    self.visitorInformation_phone = None
    self.receivingParty_comboBox = None
    self.infoPass_comboBox = None
    self.visitorInformation_number = None
    self.visitorInformation_patronymic = None
    self.visitorInformation_note = None
    self.visitorInformation_organization = None
    self.visitorInformation_series = None
    self.visitorInformation_name = None
    self.visitorInformation_surname = None
    self.receivingParty_fio = None
    self.visitorInformation_email = None
    self.attachedDocuments_selectedAilesLbl = None
    self.attachedPhoto_photo = None
    self.infoPass_dateAbout = None
    self.infoPass_dateWith = None
    
    self.start_window = start_window
    self.db = DB()
    self.connect = self.db.connect
    self.cursor = self.db.cursor

    print(self.cursor.execute("SELECT LAST_INSERT_ID()"))

    # ?: создаем новое окно и задаем ему фиксированный размер с заголовком
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(1000, 700)
    self.setCentralWidget(QWidget())
    
    self.initGUI()
    
  def initGUI(self):
    
    # @: создаем форму => Информация для пропуска
    infoPass_groupBox = QGroupBox("Информация для пропуск")  # создание группового блока
    infoPass_grid = QGridLayout()                            # создание сетки
    infoPass_grid.setAlignment(                              # выравнивание сетки
      Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
    )
    infoPass_groupBox.setLayout(infoPass_grid)               # добавление формы в групповой блок
    
    self.infoPass_dateWith = create_date_edit_with()  # создание поля с датой "с*"
    self.infoPass_dateAbout = create_date_edit_with() # создание поля с датой "по*"
    self.infoPass_dateWith.dateChanged.connect(self.update_max_date) # обновление даты после её выбора
    
    infoPass_groupDate = QHBoxLayout() # создание группового горизонтального блока с полями даты
    add_widgets_to_layout(
      infoPass_groupDate,
      [QLabel("c"), self.infoPass_dateWith, QLabel("по"), self.infoPass_dateAbout]
    )

    self.infoPass_comboBox = QComboBox() # строка выбора "Цель посещения"
    self.infoPass_comboBox.addItems(     # добавление списка из состоящего из массива
      ["Ознакомление", "Экскурсия", "Мне просто спросить"]
    )
    
    infoPass_grid.addWidget(QLabel("Срок действия заявки*:"), 0, 0) # 1-я строка
    infoPass_grid.addLayout(infoPass_groupDate, 1, 0)               # 2-я строка
    infoPass_grid.addWidget(QLabel("Цель посещения*:"), 2, 0)       # 3-я строка
    infoPass_grid.addWidget(self.infoPass_comboBox, 3, 0)                # 4-я строка
    
    # @: создаем форму => Принимающая сторона
    receivingParty_groupBox = QGroupBox("Принимающая сторона")  # создаем групповой блок
    receivingParty_grid = QGridLayout()                         # создание сетки
    receivingParty_grid.setAlignment(Qt.AlignmentFlag.AlignTop) # выравнивание по верху группового блока
    receivingParty_groupBox.setLayout(receivingParty_grid)      # добавление сетки в групповой блок
    
    self.receivingParty_comboBox = QComboBox()                      # строка выбора "Подразделение"
    self.receivingParty_comboBox.addItems(["ТКМП", "ЮФУ", "ГИБДД"]) # добавление списка из состоящего из массива
    
    self.receivingParty_fio = QLineEdit() # строка ввода фамилии
    self.receivingParty_fio.textChanged.connect(self.validate_input)
    self.receivingParty_fio.textChanged.connect(
      lambda: self.receivingParty_fio.setText(
        re.sub(r'[^а-яА-Я\\s ]', '', self.receivingParty_fio.text().title())
      )
    )
    self.receivingParty_fio.setMaxLength(50)
    
    receivingParty_grid.addWidget(QLabel("Подразделение*:"), 0, 0)  # 1-я строка
    receivingParty_grid.addWidget(self.receivingParty_comboBox, 1, 0) # 2-я строка
    receivingParty_grid.addWidget(QLabel("ФИО*:"), 2, 0)            # 3-я строка
    receivingParty_grid.addWidget(self.receivingParty_fio, 3, 0)    # 4-я строка
    
    # @: создаем форму => Информация о посетителе
    visitorInformation_groupBox = QGroupBox("Информация о посетителе") # создаем групповой блок
    visitorInformation_grid = QGridLayout()                             # создание сетки
    visitorInformation_grid.setAlignment(Qt.AlignmentFlag.AlignTop)     # выравнивание по верху группового блока
    visitorInformation_groupBox.setLayout(visitorInformation_grid)   # добавление сетки в групповой блок
    
    # ?: окно с картинкой и полем загрузить фотографию
    attachedPhoto_qvboxLayout = QVBoxLayout()
    
    self.attachedPhoto_photo = QLabel() # добавление области для отображения фотографии
    self.attachedPhoto_photo.setFixedSize(200, 200)
    self.attachedPhoto_photo.setPixmap(QPixmap("./img/one.jpg"))
    self.attachedPhoto_photo.setScaledContents(True)

    attachedPhoto_button = QPushButton("Загрузить фото") # создание кнопки для загрузки фотографии
    attachedPhoto_button.setFixedWidth(100)
    attachedPhoto_button.clicked.connect(self.load_image)
    
    attachedPhoto_qvboxLayout.addWidget(self.attachedPhoto_photo) # добавление в блок
    attachedPhoto_qvboxLayout.setAlignment(                       # выравнивание по центру
      self.attachedPhoto_photo, Qt.AlignmentFlag.AlignHCenter
    )
    attachedPhoto_qvboxLayout.addWidget(attachedPhoto_button) # добавление в блок
    attachedPhoto_qvboxLayout.setAlignment(                   # выравнивание по центру
      attachedPhoto_button, Qt.AlignmentFlag.AlignHCenter
    )
    
    visitorInformation_grid.addLayout(attachedPhoto_qvboxLayout, 0, 4, 6, 1)

    INPUT_LENGTH = 50
    
    # 1-я строка | Фамилия && Организация
    visitorInformation_grid.addWidget(QLabel("Фамилия*:"), 0, 0)
    self.visitorInformation_surname = QLineEdit() ; self.visitorInformation_surname.setMaxLength(INPUT_LENGTH)
    self.visitorInformation_surname.textEdited.connect(
      lambda: self.visitorInformation_surname.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.visitorInformation_surname.text().title())
      )
    )
    visitorInformation_grid.addWidget(self.visitorInformation_surname, 0, 1)
    
    visitorInformation_grid.addWidget(QLabel("Организация:"), 0, 2)
    self.visitorInformation_organization = QLineEdit() ; self.visitorInformation_organization.setMaxLength(INPUT_LENGTH)
    visitorInformation_grid.addWidget(self.visitorInformation_organization, 0, 3)
    # 2-я строка
    visitorInformation_grid.addWidget(QLabel("Имя*:"), 1, 0)
    self.visitorInformation_name = QLineEdit() ; self.visitorInformation_name.setMaxLength(INPUT_LENGTH)
    self.visitorInformation_name.textEdited.connect(
      lambda: self.visitorInformation_name.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.visitorInformation_name.text().title())
      )
    )
    visitorInformation_grid.addWidget(self.visitorInformation_name, 1, 1)
    
    visitorInformation_grid.addWidget(QLabel("Примечание*:"), 1, 2)
    self.visitorInformation_note = QLineEdit() ; self.visitorInformation_note.setMaxLength(INPUT_LENGTH)
    visitorInformation_grid.addWidget(self.visitorInformation_note, 1, 3)
    # 3-я строка
    visitorInformation_grid.addWidget(QLabel("Отчество*:"), 2, 0)
    self.visitorInformation_patronymic = QLineEdit() ; self.visitorInformation_patronymic.setMaxLength(25)
    self.visitorInformation_patronymic.textEdited.connect(
      lambda: self.visitorInformation_patronymic.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.visitorInformation_patronymic.text().title())
      )
    )
    visitorInformation_grid.addWidget(self.visitorInformation_patronymic , 2, 1)
    
    visitorInformation_grid.addWidget(QLabel("Дата рождения:"), 2, 2)
    self.visitorInformation_birthdate = QDateEdit() ; self.visitorInformation_birthdate.setCalendarPopup(True)
    self.visitorInformation_birthdate.setMaximumDate(QDate.currentDate().addYears(-16))
    visitorInformation_grid.addWidget(self.visitorInformation_birthdate, 2, 3)
    # 4-я строка
    visitorInformation_grid.addWidget(QLabel("Телефон:"), 3, 0)
    self.visitorInformation_phone = QLineEdit() ; self.visitorInformation_phone.setInputMask('+7 (999) 999-99-99')
    
    visitorInformation_grid.addWidget(self.visitorInformation_phone, 3, 1)
    visitorInformation_grid.addWidget(QLabel("Серия паспорта*:"), 3, 2)
    self.visitorInformation_series = QLineEdit() ; self.visitorInformation_series.setMaxLength(4)
    self.visitorInformation_series.setValidator(QIntValidator())
    visitorInformation_grid.addWidget(self.visitorInformation_series, 3, 3)
    # 5-я строка
    visitorInformation_grid.addWidget(QLabel("E-mail*:"), 4, 0)
    self.visitorInformation_email = QLineEdit()
    self.visitorInformation_email.setValidator(QRegularExpressionValidator(
      QRegularExpression(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    ))
    visitorInformation_grid.addWidget(self.visitorInformation_email, 4, 1)
    
    visitorInformation_grid.addWidget(QLabel("Номер паспорта*:"), 4, 2)
    self.visitorInformation_number = QLineEdit() ; self.visitorInformation_number.setMaxLength(6)
    self.visitorInformation_number.setValidator(QIntValidator())
    visitorInformation_grid.addWidget(self.visitorInformation_number, 4, 3)
    
    # @: создаем форму => Прикрепляемые документы
    attachedDocuments_groupBox = QGroupBox("Прикрепляемые документы")   # создаем групповой блок
    attachedDocuments_formLayout = QFormLayout()                        # создаем форму
    attachedDocuments_groupBox.setFixedWidth(700)
    attachedDocuments_groupBox.setLayout(attachedDocuments_formLayout) # добавление формы в групповой блок
    
    attachedDocuments_chooseFileBtn = QPushButton("Выбрать файлы") # cоздание кнопки для вызова диалога выбора файлов
    attachedDocuments_chooseFileBtn.clicked.connect(self.show_file_dialog)
    self.attachedDocuments_selectedAilesLbl = QLabel() # метка для отображения выбранных файлов
    attachedDocuments_formLayout.addRow(attachedDocuments_chooseFileBtn)
    attachedDocuments_formLayout.addRow(self.attachedDocuments_selectedAilesLbl)
    
    # @: блок кнопок
    buttons = QHBoxLayout()

    back_button = QPushButton("Назад") # кнопка "Назад"
    back_button.setFixedWidth(80)
    back_button.clicked.connect(lambda: self.show_main_window)

    further_button = QPushButton("Оформить заявку") # кнопка "Оформить заявку"
    further_button.setFixedWidth(120)
    further_button.clicked.connect(lambda: self.make_application())
    
    buttons.addWidget(back_button)
    buttons.addWidget(further_button)

    # конфигурация QGridLayout
    grid = QGridLayout()                                    # grid - для размещения элементов по сетке
    grid.addWidget(infoPass_groupBox, 0, 0)                 # информация для пропуска
    grid.addWidget(receivingParty_groupBox, 0, 1)           # принимающая сторона
    grid.addWidget(visitorInformation_groupBox, 1, 0, 1, 2) # информация о посетителе
    grid.addWidget(attachedDocuments_groupBox, 2, 0)        # прикрепляемые документы
    grid.addLayout(buttons, 2, 1)
    
    grid.setSpacing(5)
    self.centralWidget().setLayout(grid)
    
  # ОБНОВЛЕНИЕ ДАТЫ
  def update_max_date(self):
    self.infoPass_dateAbout.setMinimumDate(self.infoPass_dateWith.date())
    self.infoPass_dateAbout.setMaximumDate(self.infoPass_dateWith.date().addDays(15))
  
  # ЗАГРУЗКА ИЗОБРАЖЕНИЯ
  def load_image(self):
    file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")
    if file_name: # загрузка выбранного изображения
      self.attachedPhoto_photo.setPixmap(QPixmap(file_name))
      self.attachedPhoto_photo.setScaledContents(True)
    
  # ОТОБРАЖЕНИЕ ДИАЛОГОВОГО ОКНА ВЫБОРА ФАЙЛОВ
  def show_file_dialog(self):
    self.file_names, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "*.pdf")
    print(self.file_names)
    self.attachedDocuments_selectedAilesLbl.setText("Выбранные файлы: " + ", ".join(self.file_names)) # отображение выбранных файлов в метке

    # Добавляем сохранение файлов на компьютер
    if self.file_names:
      file_path = os.path.join("D:/GitHub/Web-service-for-ordering-a-pass/files/individual_visit_window/pdf_files", "лох.pdf",)
      for file_name in self.file_names:
        with open(file_name, 'rb') as file:
          data = file.read()
        with open(file_path, 'ab') as file:
          file.write(data)
      print("Файлы успешно сохранены.")
    
  # ВОЗВРАЩЕНИЕ В ГЛАВНОЕ МЕНЮ
  def show_main_window(self):
    self.hide()
    self.start_window.show()
    
  # ОБРАБОТКИ ФОРМЫ
  def make_application(self):
    print("Работает")
    print(self.file_names)
    
    blank_fields = [] # массив, куда мы будем записывать наши не записанные поля
    form_valid = True # формат проверки
    
    # ФИО валидация
    if self.receivingParty_fio.text() == "":
      blank_fields.append("ФИО")
      form_valid = False
      
    # Фамилия | валидация
    if self.visitorInformation_surname.text() == "":
      blank_fields.append("Фамилия")
      form_valid = False
    
    # Имя | валидация
    if self.visitorInformation_name.text() == "":
      blank_fields.append("Имя")
      form_valid = False
    
    # Отчество | валидация
    if self.visitorInformation_patronymic.text() == "":
      blank_fields.append("Отчество")
      form_valid = False
    
    # E-mail | валидация
    email = self.visitorInformation_email.text()
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
      
    # Примечание | валидация
    if self.visitorInformation_note.text() == "":
      blank_fields.append("Примечание")
      form_valid = False
    
    # Серия паспорта | валидация
    if self.visitorInformation_series.text() == "":
      blank_fields.append("Серия паспорта")
      form_valid = False
      
    # Номер паспорта | валидация
    if self.visitorInformation_number.text() == "":
      blank_fields.append("Номер паспорта")
      form_valid = False
      
    # Прикрепляемые документы | валидация
    if self.file_names is None:
      blank_fields.append("Прикрепите документы")
      form_valid = False
    
    if not form_valid:
      message = "\n".join(blank_fields)
      QMessageBox.warning(self, "Заполните поля", message)
    elif form_valid:
      
      
      
      sql = "INSERT INTO personal_visit(validity_period_from ,validity_period_for,purpose_of_the_visit,division,FIO,surname,name,patronymic,phone,email,organization,note,birthdate,passport_series,passport_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (
        self.infoPass_dateWith.date().toString("yyyy-MM-dd"),
        self.infoPass_dateAbout.date().toString("yyyy-MM-dd"),
        self.infoPass_comboBox.currentText(),
        self.receivingParty_comboBox.currentText(),
        self.receivingParty_fio.text(),
        self.visitorInformation_surname.text(),
        self.visitorInformation_name.text(),
        self.visitorInformation_patronymic.text(),
        re.sub(r'[^\d+]', '', self.visitorInformation_phone.text()),
        self.visitorInformation_email.text(),
        self.visitorInformation_organization.text(),
        self.visitorInformation_note.text(),
        self.visitorInformation_birthdate.date().toString("yyyy-MM-dd"),
        self.visitorInformation_series.text(),
        self.visitorInformation_number.text()
      )
      self.cursor.execute(sql,val)
      self.connect.commit()
      QMessageBox.warning(self, "Успех", "Валидация прошла успешно")
      
  # СОБЫТИЕ НА ЗАКРЫТИЕ ОКНА
  def closeEvent(self, event):
    self.start_window.show()
    self.hide()

  def validate_input(self):
    text = self.receivingParty_fio.text().strip()
    words = text.split()
    if len(words) > 3:
      cursor_pos = self.receivingParty_fio.cursorPosition()
      self.receivingParty_fio.setText(" ".join(words[:3]))
      self.receivingParty_fio.setCursorPosition(cursor_pos - 1)

  def keyPressEvent(self, event):
    # запрещаем ввод пробелов, если слов уже три
    if event.key() == Qt.Key and len(self.receivingParty_fio.text().split()) >= 3:
      event.ignore()
    else:
      super().keyPressEvent(event)