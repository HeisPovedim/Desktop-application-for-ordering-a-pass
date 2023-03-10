import sys
from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget, QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout
from helpers.capitalize_text import capitalize_text

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # задаем фиксированный размер главного окна и его заголовок
    self.setWindowTitle("IDVisitor")
    self.setWindowIcon(QIcon("./img/icon.png"))
    self.setFixedSize(600, 400)

    # создаем виджет, на котором будут расположены картинки и подписи
    widget = QWidget(self)
    self.setCentralWidget(widget)

    # создаем лейблы для каждой картинки и подписи
    label1 = QLabel(widget)
    label1.setPixmap(QPixmap("./img/one.jpg").scaled(250, 250, transformMode= Qt.TransformationMode.SmoothTransformation))
    label1.move(25, 50)
    caption1 = QLabel("Личное посещение", widget)
    caption1.move(105, 315)

    label2 = QLabel(widget)
    label2.setPixmap(QPixmap("./img/group.jpg").scaled(250, 250, transformMode = Qt.TransformationMode.SmoothTransformation))
    label2.move(325, 50)
    caption2 = QLabel("Групповое посещение", widget)
    caption2.move(405, 315)

    # привязываем к лейблам события нажатия на них
    label1.mousePressEvent = lambda event: self.individual_visit_window()
    label2.mousePressEvent = lambda event: self.group_visit_window()

  # #: ОКНО ИНДИВИДУАЛЬНОГО ПОСЕЩЕНИЯ
  def individual_visit_window(self):
    
    # ?: создаем новое окно и задаем ему фиксированный размер с заголовком
    new_window = QMainWindow(self)
    new_window.setWindowTitle("IDVisitor")
    new_window.setFixedSize(1000, 700)
    new_window.setCentralWidget(QWidget())
    
    # @: создаем форму => Информация для пропуска
    infoForThePass__groupBox = QGroupBox("Информация для пропуск")                            # создание группового блока
    infoForThePass__grid = QGridLayout()                                                      # создание сетки
    infoForThePass__grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) # выравнивание сетки
    infoForThePass__groupBox.setLayout(infoForThePass__grid)                                  # добавление формы в групповой блок
    
    self.infoForThePassDate_editWith = QDateEdit(infoForThePass__groupBox) # создание поля с датой "с*"
    self.infoForThePassDate_editWith.setFixedWidth(150)                    # фиксация ширины поля
    self.infoForThePassDate_editWith.setCalendarPopup(True)                # включение календаря
    self.infoForThePassDate_editWith.setMinimumDate(QDate.currentDate())
    self.infoForThePassDate_editWith.setMaximumDate(QDate.currentDate().addDays(15))
    
    self.infoForThePassDate_editAbout = QDateEdit(infoForThePass__groupBox) # создание поля с датой "по"
    self.infoForThePassDate_editAbout.setFixedWidth(150)                    # фиксация ширины поля
    self.infoForThePassDate_editAbout.setCalendarPopup(True)                # включение календаря
    self.infoForThePassDate_editAbout.setMinimumDate(self.infoForThePassDate_editWith.date())
    self.infoForThePassDate_editAbout.setMaximumDate(self.infoForThePassDate_editWith.date().addDays(15))
    
    self.infoForThePassDate_editWith.dateChanged.connect(self.update_max_date) # обновление даты после её выбора
    
    infoForThePass__comboBox = QComboBox() # строка выбора "Цель посещения"
    infoForThePass__comboBox.addItems(["Ознакомление", "Экскурсия", "Мне просто спросить"]) # добавление списка из состоящего из массива
    
    infoForThePass__QHBoxLayout = QHBoxLayout()                              # создание группового горинзотального блока
    infoForThePass__QHBoxLayout.addWidget(QLabel("c"))                       # добавление в блок
    infoForThePass__QHBoxLayout.addWidget(self.infoForThePassDate_editWith)  # добавление в блок
    infoForThePass__QHBoxLayout.addWidget(QLabel("по"))                      # добавление в блок
    infoForThePass__QHBoxLayout.addWidget(self.infoForThePassDate_editAbout) # добавление в блок
    
    infoForThePass__grid.addWidget(QLabel("Срок действия заявки*:"), 0, 0) # 1-я строка
    infoForThePass__grid.addLayout(infoForThePass__QHBoxLayout, 1, 0)      # 2-я строка
    infoForThePass__grid.addWidget(QLabel("Цель посещения*:"), 2, 0)       # 3-я строка
    infoForThePass__grid.addWidget(infoForThePass__comboBox, 3, 0)         # 4-я строка
    
    # @: создаем форму => Принимающая сторона
    receivingParty__groupBox = QGroupBox("Принимающая сторона")  # создаем групповой блок
    receivingParty__grid = QGridLayout()                         # создание сетки
    receivingParty__grid.setAlignment(Qt.AlignmentFlag.AlignTop) # выравнивание по верху группового блока
    receivingParty__groupBox.setLayout(receivingParty__grid)     # добавление сетки в групповой блок
    
    receivingParty__comboBox = QComboBox()                      # строка выбора "Подразделение"
    receivingParty__comboBox.addItems(["ТКМП", "ЮФУ", "ГИБДД"]) # добавление списка из состоящего из массива
    
    receivingParty_FIO = QLineEdit() # строка ввода фамилии
    receivingParty_FIO.setValidator(QRegularExpressionValidator(QRegularExpression("[А-Яа-я ]+")))
    
    receivingParty__grid.addWidget(QLabel("Подразделение*:"), 0, 0) # 1-я строка
    receivingParty__grid.addWidget(receivingParty__comboBox, 1, 0)  # 2-я строка
    receivingParty__grid.addWidget(QLabel("ФИО*:"), 2, 0)           # 3-я строка
    receivingParty__grid.addWidget(receivingParty_FIO, 3, 0)   # 4-я строка
    
    receivingParty_FIO.textEdited.connect(capitalize_text)
    
    # @: создаем форму => Информация о посетителе
    visitorInformation__groupBox = QGroupBox("Информация о посетителе") # создаем групповой блок
    visitorInformation__grid = QGridLayout()                            # создание сетки
    visitorInformation__grid.setAlignment(Qt.AlignmentFlag.AlignTop)    # выравнивание по верху группового блока
    visitorInformation__groupBox.setLayout(visitorInformation__grid)    # добавление сетки в групповой блок
    
    # ?: окно с картинкой и полем загрузить фотографию
    attachedPhoto__QVBoxLayout = QVBoxLayout() # создание вертикального блока
    attachedPhoto__button = QPushButton("Загрузить фото")
    attachedPhoto__button.setFixedWidth(100)
    attachedPhoto__button.clicked.connect(self.load_image)
    
    self.attachedPhoto__photo = QLabel()                          # добавление области для отображения фотографии
    self.attachedPhoto__photo.setFixedSize(200, 200)              # фиксация размера для фото
    self.attachedPhoto__photo.setPixmap(QPixmap("./img/one.jpg")) # загрузка фотографии по умолчанию
    self.attachedPhoto__photo.setScaledContents(True)             # скеил фотографии
    
    attachedPhoto__QVBoxLayout.addWidget(self.attachedPhoto__photo) # добавление в блок
    attachedPhoto__QVBoxLayout.addWidget(attachedPhoto__button)     # добавление в блок
    attachedPhoto__QVBoxLayout.setAlignment(self.attachedPhoto__photo, Qt.AlignmentFlag.AlignHCenter) # выравнивание по центру
    attachedPhoto__QVBoxLayout.setAlignment(attachedPhoto__button, Qt.AlignmentFlag.AlignHCenter)     # выравнивание по центру
    
    # 1-я строка
    visitorInformation__grid.addWidget(QLabel("Фамилия*:"), 0, 0)
    visitorInformation__surname = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__surname, 0, 1)
    visitorInformation__grid.addWidget(QLabel("Организация:"), 0, 2)
    visitorInformation__organization = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__organization, 0, 3)
    # 2-я строка
    visitorInformation__grid.addWidget(QLabel("Имя*:"), 1, 0)
    visitorInformation__name = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__name, 1, 1)
    visitorInformation__grid.addWidget(QLabel("Примечание:"), 1, 2)
    visitorInformation__note = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__note, 1, 3)
    # 3-я строка
    visitorInformation__grid.addWidget(QLabel("Отчество*:"), 2, 0)
    visitorInformation__patronymic = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__patronymic , 2, 1)
    visitorInformation__grid.addWidget(QLabel("Дата рождения:"), 2, 2)
    visitorInformation_editWith = QDateEdit(visitorInformation__groupBox) # создание поля с датой рождения
    visitorInformation_editWith.setCalendarPopup(True) # включение календаря
    visitorInformation__grid.addWidget(visitorInformation_editWith, 2, 3)
    # 4-я строка
    visitorInformation__grid.addWidget(QLabel("Телефон:"), 3, 0)
    visitorInformation__phone = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__phone, 3, 1)
    visitorInformation__grid.addWidget(QLabel("Серия:"), 3, 2)
    visitorInformation__series = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__series, 3, 3)
    # 5-я строка
    visitorInformation__grid.addWidget(QLabel("E-mail:"), 4, 0)
    visitorInformation__email = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__email, 4, 1)
    visitorInformation__grid.addWidget(QLabel("Номер:"), 4, 2)
    visitorInformation__number = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__number, 4, 3)
    # блок с фотографией
    visitorInformation__grid.addLayout(attachedPhoto__QVBoxLayout, 0, 4, 6, 1)
    
    # @: создаем форму => Прикрепляемые документы
    attachedDocuments__groupBox = QGroupBox("Прикрепляемые документы")   # создаем групповой блок
    attachedDocuments__formLayout = QFormLayout()                        # создаем форму
    attachedDocuments__groupBox.setFixedWidth(700)
    attachedDocuments__groupBox.setLayout(attachedDocuments__formLayout) # добавление формы в групповой блок
    
    attachedDocuments_chooseFileBtn = QPushButton("Выбрать файлы") # cоздание кнопки для вызова диалога выбора файлов
    attachedDocuments_chooseFileBtn.clicked.connect(self.show_file_dialog)
    self.attachedDocuments_selectedАilesLbl = QLabel() # метка для отображения выбранных файлов
    attachedDocuments__formLayout.addRow(attachedDocuments_chooseFileBtn)
    attachedDocuments__formLayout.addRow(self.attachedDocuments_selectedАilesLbl)


    # создаем кнопку назад и привязываем к ней событие нажатия
    back_button = QPushButton("Назад", new_window)
    back_button.setFixedWidth(80)
    back_button.clicked.connect(lambda: self.show_main_window(new_window))


    # создаем кнопку далее и привязываем к ней событие нажатия
    further_button = QPushButton("Оформить заявку", new_window)
    further_button.setFixedWidth(120)
    further_button.clicked.connect(lambda: self.make_application(new_window))
    
    # объединение кнопок в один горизонтальный блок
    buttons = QHBoxLayout()
    buttons.addWidget(back_button)
    buttons.addWidget(further_button)

    # конфигнурация QGridLayout
    grid = QGridLayout()                               # grid - для размещения элементов по сетке
    grid.addWidget(infoForThePass__groupBox, 0, 0)     # Информация для пропуска
    grid.addWidget(receivingParty__groupBox, 0, 1)     # Принимающая сторона
    grid.addWidget(visitorInformation__groupBox, 1, 0, 1, 2) # Информация о посетителе
    grid.addWidget(attachedDocuments__groupBox, 2, 0)  # Прикрепляемые документы
    grid.addLayout(buttons, 2, 1)
    
    # grid.setCol
    
    grid.setSpacing(5)
    new_window.centralWidget().setLayout(grid)


    # привязываем к новому окну событие закрытия окна
    new_window.closeEvent = lambda: self.show_main_window(new_window)


    # показываем новое окно
    new_window.show()
    self.hide()

  # #: ОКНО ГРУППОВГО ПОСЕЩЕНИЯ
  def group_visit_window(self):
    # создаем новое окно и задаем его фиксированный размер
    new_window = QMainWindow(self)
    new_window.setFixedSize(600, 400)
  
    # создаем кнопку назад и привязываем к ней событие нажатия
    back_button = QPushButton("Назад", new_window)
    back_button.move(260, 200)
    back_button.clicked.connect(lambda: self.show_main_window(new_window))

    # привязываем к новому окну событие закрытия окна
    new_window.closeEvent = lambda event: self.show_main_window(new_window)

    # показываем новое окно
    new_window.show()
    self.hide()

  # #: ЗАКРЫТИЕ НОВОГО ОКНА И ОТКРЫТИЕ ГЛАВНОГО
  def show_main_window(self, new_window):
    # показываем главное окно и закрываем новое окно
    new_window.hide()
    self.show()

  # #: ОТОБРАЖЕНИЕ ДИАЛОГОВОГО ОКНА ВЫБОРА ФАЙЛОВ
  def show_file_dialog(self):
    file_names, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "All Files (*);;Text Files (*.txt)")
    self.attachedDocuments_selectedАilesLbl.setText("Выбранные файлы: " + ", ".join(file_names)) # отображение выбранных файлов в метке
    
  # #: ОТКРЫТИЕ ДИАЛОГОВОГО ОКНА ДЛЯ ВЫБОРА ФАЙЛА
  def load_image(self):
    file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")
    if file_name:
      # Загрузка выбранного изображения
      image = QPixmap(file_name)
      self.attachedPhoto__photo.setPixmap(image)
      self.attachedPhoto__photo.setScaledContents(True)
      
  # #: ОБНОВЛЕНИЕ ТЕКУЩЕЙ ДАТЫ НА 15 ДНЕЙ ВПЕРЕД
  def update_max_date(self):
    self.infoForThePassDate_editAbout.setMinimumDate(self.infoForThePassDate_editWith.date())
    self.infoForThePassDate_editAbout.setMaximumDate(self.infoForThePassDate_editWith.date().addDays(15))
    
# #: ВЫЗОВ КОДА ТОЛЬКО В ЭТОМ ФАЙЛЕ
if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())