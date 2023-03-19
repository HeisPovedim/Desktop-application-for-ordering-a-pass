# ВИДЖЕТ - ИНФОРМАЦИЯ О ПОСЕТИТЕЛИ
from PyQt6.QtWidgets import (
  QGroupBox, QGridLayout, QVBoxLayout, QLineEdit, QLabel,
  QPushButton, QMessageBox, QDateEdit, QFileDialog
)
from PyQt6.QtGui import QPixmap, QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, QDate

# LIBRARIES
import re

class VisitorInformation(QGroupBox):
  def __init__(self, display_photo):
    super().__init__()
    self.setTitle("Информация о посетителе")

    # Инициализация переменных
    self.display_photo = display_photo
    self.selectedAilesLbl = None
    self.number = None
    self.email = None
    self.series = None
    self.phone = None
    self.birthdate = None
    self.patronymic = None
    self.note = None
    self.name = None
    self.organization = None
    self.surname = None
    self.photo = None
    self.file_photo = None
    
    self.initGUI()
  def initGUI(self):
    grid = QGridLayout()                         # создание сетки
    grid.setAlignment(Qt.AlignmentFlag.AlignTop) # выравнивание по верху группового блока
    self.setLayout(grid)                         # добавление сетки в групповой блок
    
    if self.display_photo:
      # Окно с картинкой и полем загрузить фотографию
      group_photo = QVBoxLayout()
  
      # фотография
      self.photo = QLabel()
      self.photo.setFixedSize(200, 200)
      self.photo.setPixmap(QPixmap("./assets/img/one.jpg"))
      self.photo.setScaledContents(True)
      group_photo.addWidget(self.photo)
      group_photo.setAlignment(
        self.photo, Qt.AlignmentFlag.AlignHCenter
      )
      
      # кнопка "Загрузить фото"
      button = QPushButton("Загрузить фото")
      button.setFixedWidth(100)
      button.clicked.connect(self.load_image)
      group_photo.addWidget(button)
      group_photo.setAlignment(
        button, Qt.AlignmentFlag.AlignHCenter
      )
    
      grid.addLayout(group_photo, 0, 4, 6, 1)
    
    INPUT_LENGTH = 50
  
    # "Фамилия" && "Организация"
    grid.addWidget(QLabel("Фамилия*:"), 0, 0)
    self.surname = QLineEdit() ; self.surname.setMaxLength(INPUT_LENGTH)
    self.surname.textEdited.connect(
      lambda: self.surname.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.surname.text().title())
      )
    )
    grid.addWidget(self.surname, 0, 1)
    
    grid.addWidget(QLabel("Организация:"), 0, 2)
    self.organization = QLineEdit() ; self.organization.setMaxLength(INPUT_LENGTH)
    grid.addWidget(self.organization, 0, 3)
    
    # "Имя" && "Примечание"
    grid.addWidget(QLabel("Имя*:"), 1, 0)
    self.name = QLineEdit() ; self.name.setMaxLength(INPUT_LENGTH)
    self.name.textEdited.connect(
      lambda: self.name.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.name.text().title())
      )
    )
    grid.addWidget(self.name, 1, 1)
    
    grid.addWidget(QLabel("Примечание*:"), 1, 2)
    self.note = QLineEdit() ; self.note.setMaxLength(INPUT_LENGTH)
    grid.addWidget(self.note, 1, 3)
    
    # "Отчество" && "Дата рождения"
    grid.addWidget(QLabel("Отчество*:"), 2, 0)
    self.patronymic = QLineEdit() ; self.patronymic.setMaxLength(25)
    self.patronymic.textEdited.connect(
      lambda: self.patronymic.setText(
        re.sub(r'[^а-яА-ЯёЁ]', '', self.patronymic.text().title())
      )
    )
    grid.addWidget(self.patronymic, 2, 1)
    
    grid.addWidget(QLabel("Дата рождения:"), 2, 2)
    self.birthdate = QDateEdit(); self.birthdate.setCalendarPopup(True)
    self.birthdate.setMaximumDate(QDate.currentDate().addYears(-16))
    grid.addWidget(self.birthdate, 2, 3)
    
    # "Телефон" && "Серия паспорта"
    grid.addWidget(QLabel("Телефон:"), 3, 0)
    self.phone = QLineEdit() ; self.phone.setInputMask('+7 (999) 999-99-99')
    grid.addWidget(self.phone, 3, 1)
    
    grid.addWidget(QLabel("Серия паспорта*:"), 3, 2)
    self.series = QLineEdit() ; self.series.setMaxLength(4)
    self.series.setValidator(QIntValidator())
    grid.addWidget(self.series, 3, 3)
    
    # "E-mail" && "Номер паспорта
    grid.addWidget(QLabel("E-mail*:"), 4, 0)
    self.email = QLineEdit()
    self.email.setValidator(QRegularExpressionValidator(
      QRegularExpression(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    ))
    grid.addWidget(self.email, 4, 1)
    
    grid.addWidget(QLabel("Номер паспорта*:"), 4, 2)
    self.number = QLineEdit() ; self.number.setMaxLength(6)
    self.number.setValidator(QIntValidator())
    grid.addWidget(self.number, 4, 3)

  # ЗАГРУЗКА ИЗОБРАЖЕНИЯ
  def load_image(self):
    try:
      self.file_photo, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")
      if self.file_photo != "":
        self.photo.setPixmap(QPixmap(self.file_photo))
        self.photo.setScaledContents(True)
      else:
        self.file_photo = None
    except Exception as error:
      QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить фото: {error}")