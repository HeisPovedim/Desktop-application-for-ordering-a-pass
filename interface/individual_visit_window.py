from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QPixmap, QRegularExpressionValidator
from PyQt6.QtWidgets import (
  QLabel, QMainWindow, QPushButton, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget,
  QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QVBoxLayout, QMessageBox
)
from helpers.capitalize_text import capitalize_text
import dns.resolver


class PersonalWindow(QMainWindow):
  def __init__(self, start_window):
    super().__init__()
    self.receiving_party_fio = None
    self.visitor_information__email = None
    self.attached_documents_selected_ailes_lbl = None
    self.attached_photo__photo = None
    self.info_passDate_editAbout = None
    self.info_passDate_editWith = None
    self.start_window = start_window
    
    self.initGUI()
    
    
  def initGUI(self):
    # ?: создаем новое окно и задаем ему фиксированный размер с заголовком
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(1000, 700)
    self.setCentralWidget(QWidget())
    
    # @: создаем форму => Информация для пропуска
    info_pass__group_box = QGroupBox("Информация для пропуск") # создание группового блока
    info_pass__grid = QGridLayout() # создание сетки
    info_pass__grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) # выравнивание сетки
    info_pass__group_box.setLayout(info_pass__grid) # добавление формы в групповой блок
    
    self.info_passDate_editWith = QDateEdit(info_pass__group_box) # создание поля с датой "с*"
    self.info_passDate_editWith.setFixedWidth(150) # фиксация ширины поля
    self.info_passDate_editWith.setCalendarPopup(True) # включение календаря
    self.info_passDate_editWith.setMinimumDate(QDate.currentDate()) # выбор даты не меньше текущей
    self.info_passDate_editWith.setMaximumDate(QDate.currentDate().addDays(15)) # макс можно выбрать на 15 вперед от текущей даты
    
    self.info_passDate_editAbout = QDateEdit(info_pass__group_box) # создание поля с датой "по"
    self.info_passDate_editAbout.setFixedWidth(150) # фиксация ширины поля
    self.info_passDate_editAbout.setCalendarPopup(True) # включение календаря
    self.info_passDate_editAbout.setMinimumDate(self.info_passDate_editWith.date()) # зависит от даты с полем "с"
    self.info_passDate_editAbout.setMaximumDate(self.info_passDate_editWith.date().addDays(15)) # зависит от даты с полем "с"
    
    self.info_passDate_editWith.dateChanged.connect(self.update_max_date) # обновление даты после её выбора
    
    info_pass__combo_box = QComboBox() # строка выбора "Цель посещения"
    info_pass__combo_box.addItems(["Ознакомление", "Экскурсия", "Мне просто спросить"]) # добавление списка из состоящего из массива
    
    info_pass__qhbox_layout = QHBoxLayout()                              # создание группового горизонтального блока с полями даты
    info_pass__qhbox_layout.addWidget(QLabel("c"))                       # добавление в блок
    info_pass__qhbox_layout.addWidget(self.info_passDate_editWith)       # добавление в блок
    info_pass__qhbox_layout.addWidget(QLabel("по"))                      # добавление в блок
    info_pass__qhbox_layout.addWidget(self.info_passDate_editAbout)      # добавление в блок
    
    info_pass__grid.addWidget(QLabel("Срок действия заявки*:"), 0, 0) # 1-я строка
    info_pass__grid.addLayout(info_pass__qhbox_layout, 1, 0)          # 2-я строка
    info_pass__grid.addWidget(QLabel("Цель посещения*:"), 2, 0)       # 3-я строка
    info_pass__grid.addWidget(info_pass__combo_box, 3, 0)             # 4-я строка
    
    # @: создаем форму => Принимающая сторона
    receiving_party__group_box = QGroupBox("Принимающая сторона") # создаем групповой блок
    receiving_party__grid = QGridLayout()                         # создание сетки
    receiving_party__grid.setAlignment(Qt.AlignmentFlag.AlignTop) # выравнивание по верху группового блока
    receiving_party__group_box.setLayout(receiving_party__grid)   # добавление сетки в групповой блок
    
    receiving_party__combo_box = QComboBox()                      # строка выбора "Подразделение"
    receiving_party__combo_box.addItems(["ТКМП", "ЮФУ", "ГИБДД"]) # добавление списка из состоящего из массива
    
    self.receiving_party_fio = QLineEdit() # строка ввода фамилии
    self.receiving_party_fio.setValidator(QRegularExpressionValidator(QRegularExpression("^[а-яА-Я\\s]*$")))
    self.receiving_party_fio.setMaxLength(50)
    
    receiving_party__grid.addWidget(QLabel("Подразделение*:"), 0, 0)  # 1-я строка
    receiving_party__grid.addWidget(receiving_party__combo_box, 1, 0) # 2-я строка
    receiving_party__grid.addWidget(QLabel("ФИО*:"), 2, 0)            # 3-я строка
    receiving_party__grid.addWidget(self.receiving_party_fio, 3, 0)        # 4-я строка
    
    self.receiving_party_fio.textEdited.connect(
      lambda: self.receiving_party_fio.setText(capitalize_text("FIO", self.receiving_party_fio.text()))
    )
    
    # @: создаем форму => Информация о посетителе
    visitor_information__group_box = QGroupBox("Информация о посетителе") # создаем групповой блок
    visitor_information__grid = QGridLayout()                             # создание сетки
    visitor_information__grid.setAlignment(Qt.AlignmentFlag.AlignTop)     # выравнивание по верху группового блока
    visitor_information__group_box.setLayout(visitor_information__grid)   # добавление сетки в групповой блок
    
    # ?: окно с картинкой и полем загрузить фотографию
    attached_photo__qvbox_layout = QVBoxLayout() # создание вертикального блока
    attached_photo__button = QPushButton("Загрузить фото")
    attached_photo__button.setFixedWidth(100)
    attached_photo__button.clicked.connect(self.load_image)
    
    self.attached_photo__photo = QLabel()                          # добавление области для отображения фотографии
    self.attached_photo__photo.setFixedSize(200, 200)              # фиксация размера для фото
    self.attached_photo__photo.setPixmap(QPixmap("./img/one.jpg")) # загрузка фотографии по умолчанию
    self.attached_photo__photo.setScaledContents(True)             # скеил фотографии
    
    attached_photo__qvbox_layout.addWidget(self.attached_photo__photo) # добавление в блок
    attached_photo__qvbox_layout.addWidget(attached_photo__button)     # добавление в блок
    attached_photo__qvbox_layout.setAlignment(self.attached_photo__photo, Qt.AlignmentFlag.AlignHCenter) # выравнивание по центру
    attached_photo__qvbox_layout.setAlignment(attached_photo__button, Qt.AlignmentFlag.AlignHCenter)     # выравнивание по центру
    
    # 1-я строка
    visitor_information__grid.addWidget(QLabel("Фамилия*:"), 0, 0)
    visitor_information__surname = QLineEdit()
    visitor_information__surname.setMaxLength(25)
    visitor_information__surname.textEdited.connect(
      lambda: visitor_information__surname.setText(capitalize_text("Surname", visitor_information__surname.text()))
    )
    visitor_information__grid.addWidget(visitor_information__surname, 0, 1)
    visitor_information__grid.addWidget(QLabel("Организация:"), 0, 2)
    visitor_information__organization = QLineEdit()
    visitor_information__grid.addWidget(visitor_information__organization, 0, 3)
    # 2-я строка
    visitor_information__grid.addWidget(QLabel("Имя*:"), 1, 0)
    visitor_information__name = QLineEdit()
    visitor_information__name.setMaxLength(25)
    visitor_information__name.textEdited.connect(
      lambda: visitor_information__name.setText(capitalize_text("Other", visitor_information__name.text()))
    )
    visitor_information__grid.addWidget(visitor_information__name, 1, 1)
    visitor_information__grid.addWidget(QLabel("Примечание*:"), 1, 2)
    visitor_information__note = QLineEdit()
    visitor_information__grid.addWidget(visitor_information__note, 1, 3)
    # 3-я строка
    visitor_information__grid.addWidget(QLabel("Отчество*:"), 2, 0)
    visitor_information__patronymic = QLineEdit()
    visitor_information__patronymic.setMaxLength(25)
    visitor_information__patronymic.textEdited.connect(
      lambda: visitor_information__patronymic.setText(capitalize_text("Other", visitor_information__patronymic.text()))
    )
    visitor_information__grid.addWidget(visitor_information__patronymic , 2, 1)
    visitor_information__grid.addWidget(QLabel("Дата рождения:"), 2, 2)
    visitor_information_edit_with = QDateEdit(visitor_information__group_box) # создание поля с датой рождения
    visitor_information_edit_with.setCalendarPopup(True) # включение календаря
    visitor_information__grid.addWidget(visitor_information_edit_with, 2, 3)
    # 4-я строка
    visitor_information__grid.addWidget(QLabel("Телефон:"), 3, 0)
    visitor_information__phone = QLineEdit()
    visitor_information__phone.setInputMask('+7 (999) 999-99-99')
    visitor_information__grid.addWidget(visitor_information__phone, 3, 1)
    visitor_information__grid.addWidget(QLabel("Серия*:"), 3, 2)
    visitor_information__series = QLineEdit()
    visitor_information__grid.addWidget(visitor_information__series, 3, 3)
    # 5-я строка
    visitor_information__grid.addWidget(QLabel("E-mail*:"), 4, 0)
    self.visitor_information__email = QLineEdit()
    visitor_information__grid.addWidget(self.visitor_information__email, 4, 1)
    visitor_information__grid.addWidget(QLabel("Номер*:"), 4, 2)
    visitor_information__number = QLineEdit()
    visitor_information__grid.addWidget(visitor_information__number, 4, 3)
    # блок с фотографией
    visitor_information__grid.addLayout(attached_photo__qvbox_layout, 0, 4, 6, 1)
    
    # @: создаем форму => Прикрепляемые документы
    attached_documents__group_box = QGroupBox("Прикрепляемые документы")   # создаем групповой блок
    attached_documents__form_layout = QFormLayout()                        # создаем форму
    attached_documents__group_box.setFixedWidth(700)
    attached_documents__group_box.setLayout(attached_documents__form_layout) # добавление формы в групповой блок
    
    attached_documents_choose_file_btn = QPushButton("Выбрать файлы") # cоздание кнопки для вызова диалога выбора файлов
    attached_documents_choose_file_btn.clicked.connect(self.show_file_dialog)
    self.attached_documents_selected_ailes_lbl = QLabel() # метка для отображения выбранных файлов
    attached_documents__form_layout.addRow(attached_documents_choose_file_btn)
    attached_documents__form_layout.addRow(self.attached_documents_selected_ailes_lbl)


    # создаем кнопку назад и привязываем к ней событие нажатия
    back_button = QPushButton("Назад")
    back_button.setFixedWidth(80)
    back_button.clicked.connect(lambda: self.show_main_window)


    # создаем кнопку далее и привязываем к ней событие нажатия
    further_button = QPushButton("Оформить заявку")
    further_button.setFixedWidth(120)
    further_button.clicked.connect(lambda: self.make_application())
    
    # объединение кнопок в один горизонтальный блок
    buttons = QHBoxLayout()
    buttons.addWidget(back_button)
    buttons.addWidget(further_button)

    # конфигурация QGridLayout
    grid = QGridLayout()                                       # grid - для размещения элементов по сетке
    grid.addWidget(info_pass__group_box, 0, 0)                 # информация для пропуска
    grid.addWidget(receiving_party__group_box, 0, 1)           # принимающая сторона
    grid.addWidget(visitor_information__group_box, 1, 0, 1, 2) # информация о посетителе
    grid.addWidget(attached_documents__group_box, 2, 0)        # прикрепляемые документы
    grid.addLayout(buttons, 2, 1)
    
    grid.setSpacing(5)
    self.centralWidget().setLayout(grid)
    
  # ОБНОВЛЕНИЕ ДАТЫ
  def update_max_date(self):
    self.info_passDate_editAbout.setMinimumDate(self.info_passDate_editWith.date())
    self.info_passDate_editAbout.setMaximumDate(self.info_passDate_editWith.date().addDays(15))
  
  # ЗАГРУЗКА ИЗОБРАЖЕНИЯ
  def load_image(self):
    file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")
    if file_name: # загрузка выбранного изображения
      self.attached_photo__photo.setPixmap(QPixmap(file_name))
      self.attached_photo__photo.setScaledContents(True)
    
  # ОТОБРАЖЕНИЕ ДИАЛОГОВОГО ОКНА ВЫБОРА ФАЙЛОВ
  def show_file_dialog(self):
    file_names, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "All Files (*);;Text Files (*.txt)")
    self.attached_documents_selected_ailes_lbl.setText("Выбранные файлы: " + ", ".join(file_names)) # отображение выбранных файлов в метке
    
  # ЗАКРЫТИЕ НОВОГО ОКНА И ОТКРЫТИЕ ГЛАВНОГО
  def show_main_window(self):
    self.hide()
    self.start_window.show()
    
  # ОБРАБОТКИ ФОРМЫ
  def make_application(self):
    print("Работает")
    # фио валидация
    fio = self.receiving_party_fio.text()
    if fio != "":
      print("Ok")
    else:
      QMessageBox.warning(self, "Пиздец", "Ну ты и еблан, напиши ФИО")
      
    # email валидация
    email = self.visitor_information__email.text().strip()
    domain = email.split('@')[-1]
    
    if email != "":
      # получаем MX записи домена
      try:
        answers = dns.resolver.resolve(domain, 'MX')
      except dns.resolver.NXDOMAIN:
        QMessageBox.warning(self, 'Validation', 'No MX records found for domain')
        return
  
      # проверяем, есть ли хотя бы один адрес сервера в ответе
      if len(answers) > 0:
        QMessageBox.information(self, 'Validation', 'Email is valid')
      else:
        QMessageBox.warning(self, 'Validation', 'No valid MX records found for domain')
    else:
      QMessageBox.warning(self, "ПОЧТА!!", "Ты забыл почту олень!")
      
  def closeEvent(self, event):
    self.start_window.show()
    self.hide()
