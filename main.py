import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QFormLayout, QDateEdit, QWidget, QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QFileDialog

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # задаем фиксированный размер главного окна и его заголовок
    self.setWindowTitle("IDVisitor")
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

  # Окно индивидуального посещения
  def individual_visit_window(self):

    # создаем новое окно и задаем его фиксированный размер, и его заголовок
    new_window = QMainWindow(self) 
    new_window.setWindowTitle("IDVisitor")
    new_window.setFixedSize(1000, 700)
    new_window.setCentralWidget(QWidget())


    # создаем форму => Информация для пропуска
    infoForThePass__groupBox = QGroupBox("Информация для пропуск") # создаем групповой блок
    infoForThePass__formLayout = QFormLayout()                     # создаем форму
    infoForThePass__groupBox.setLayout(infoForThePass__formLayout) # добавление формы в групповой блок
    
    infoForThePassDate_editWith = QDateEdit(infoForThePass__groupBox) # создание поля с датой "с*"
    infoForThePassDate_editWith.setCalendarPopup(True)                # включение календаря
    infoForThePassDate_editWith.setMinimumDate(QDate.currentDate())   # установка текущей даты
    
    infoForThePassDate_editAbout = QDateEdit(infoForThePass__groupBox) # создание поля с датой "по"
    infoForThePassDate_editAbout.setCalendarPopup(True)                # включение календаря
    infoForThePassDate_editAbout.setMinimumDate(QDate.currentDate())   # установка текущей даты
    
    infoForThePass__comboBox = QComboBox() # строка выбора "Цель посещения"
    infoForThePass__comboBox.addItems(["Ознакомление", "Экскурсия", "Мне просто спросить"])
    
    infoForThePass__formLayout.addRow(QLabel("Срок действия заявки:"))     # 1-я строка
    infoForThePass__formLayout.addRow("с*", infoForThePassDate_editWith)   # 2-я строка
    infoForThePass__formLayout.addRow("по*", infoForThePassDate_editAbout) # 3-я строка
    infoForThePass__formLayout.addRow(QLabel("Цель посещения:"))           # 4-я строка
    infoForThePass__formLayout.addRow(infoForThePass__comboBox)            # 5-я строка


    # создаем форму => Принимающая сторона
    receivingParty__groupBox = QGroupBox("Принимающая сторона")    # создаем групповой блок
    receivingParty__formLayout = QFormLayout()                     # создаем форму
    receivingParty__groupBox.setLayout(receivingParty__formLayout) # добавление формы в групповой блок
    
    receivingParty__comboBox = QComboBox() # строка выбора "Подразделение"
    receivingParty__comboBox.addItems(["ТКМП", "ЮФУ", "ГИБДД"])
    
    receivingParty_FIO = QLineEdit() # строка ввода фамилии
    
    receivingParty__formLayout.addRow(QLabel("Подразделение*:")) # 1-я строка
    receivingParty__formLayout.addRow(receivingParty__comboBox)  # 2-я строка
    receivingParty__formLayout.addRow(QLabel("ФИО*:"))           # 3-я строка
    receivingParty__formLayout.addRow(receivingParty_FIO)        # 4-я строка


    # создаем форму => Информация о посетителе
    visitorInformation__groupBox = QGroupBox("Информация о посетителе") # создаем групповой блок
    visitorInformation__formLayout = QFormLayout()                      # создаем форму
    visitorInformation__grid = QGridLayout()                            # создание сетки
    visitorInformation__grid.setAlignment(Qt.AlignmentFlag.AlignTop)    # выравние по верху группового блока
    visitorInformation__groupBox.setLayout(visitorInformation__grid)    # добавление формы в групповой блок

    # 1-я строка
    visitorInformation__grid.addWidget(QLabel("Фамилия*:"), 0, 0)
    visitorInformation__formLayout_surname = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_surname, 0, 1)
    visitorInformation__grid.addWidget(QLabel("Организация:"), 0, 2)
    visitorInformation__formLayout_organization = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_organization, 0, 3)
    # 2-я строка
    visitorInformation__grid.addWidget(QLabel("Имя*:"), 1, 0)
    visitorInformation__formLayout_name = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_name, 1, 1)
    visitorInformation__grid.addWidget(QLabel("Примечание:"), 1, 2)
    visitorInformation__formLayout_note = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_note, 1, 3)
    # 3-я строка
    visitorInformation__grid.addWidget(QLabel("Отчество*:"), 2, 0)
    visitorInformation__formLayout_patronymic  = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_patronymic , 2, 1)
    visitorInformation__grid.addWidget(QLabel("Дата рождения:"), 2, 2)
    visitorInformation_editWith = QDateEdit(visitorInformation__groupBox) # создание поля с датой рождения
    visitorInformation_editWith.setCalendarPopup(True) # включение календаря
    visitorInformation__grid.addWidget(visitorInformation_editWith, 2, 3)
    # 4-я строка
    visitorInformation__grid.addWidget(QLabel("Телефон:"), 3, 0)
    visitorInformation__formLayout_phone = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_phone, 3, 1)
    visitorInformation__grid.addWidget(QLabel("Серия:"), 3, 2)
    visitorInformation__formLayout_series = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_series, 3, 3)
    # 5-я строка
    visitorInformation__grid.addWidget(QLabel("E-mail:"), 4, 0)
    visitorInformation__formLayout_email = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_email, 4, 1)
    visitorInformation__grid.addWidget(QLabel("Номер:"), 4, 2)
    visitorInformation__formLayout_number = QLineEdit()
    visitorInformation__grid.addWidget(visitorInformation__formLayout_number, 4, 3)


    # создаем форму => Прикрепляемые документы
    attachedDocuments__groupBox = QGroupBox("Прикрепляемые документы")   # создаем групповой блок
    attachedDocuments__formLayout = QFormLayout()                        # создаем форму
    attachedDocuments__groupBox.setLayout(attachedDocuments__formLayout) # добавление формы в групповой блок
    
    # cоздание кнопки для вызова диалога выбора файлов
    attachedDocuments_chooseFileBtn = QPushButton("Выбрать файлы")
    attachedDocuments_chooseFileBtn.clicked.connect(self.show_file_dialog)
    
    
    self.attachedDocuments_selectedАilesLbl = QLabel() # метка для отображения выбранных файлов
    
    attachedDocuments__formLayout.addRow(attachedDocuments_chooseFileBtn)
    attachedDocuments__formLayout.addRow(self.attachedDocuments_selectedАilesLbl)


    # создаем кнопку назад и привязываем к ней событие нажатия
    back_button = QPushButton("Назад", new_window)
    back_button.clicked.connect(lambda: self.show_main_window(new_window))


    # конфигнурация QGridLayout
    grid = QGridLayout()                               # grid - для размещения элементов по сетке
    grid.addWidget(infoForThePass__groupBox, 0, 0)     # Информация для пропуска
    grid.addWidget(receivingParty__groupBox, 0, 1)     # Принимающая сторона
    grid.addWidget(visitorInformation__groupBox, 1, 0) # Информация о посетителе
    grid.addWidget(attachedDocuments__groupBox, 2, 0)  # Прикрепляемые документы
    grid.addWidget(back_button, 2, 2)
    
    grid.setSpacing(5)
    new_window.centralWidget().setLayout(grid)


    # привязываем к новому окну событие закрытия окна
    new_window.closeEvent = lambda event: self.show_main_window(new_window)


    # показываем новое окно
    new_window.show()
    self.hide()

  # Окно группового посещения
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

  # Закрытие нового окна и открытие главного
  def show_main_window(self, new_window):
    # показываем главное окно и закрываем новое окно
    new_window.hide()
    self.show()

  # Отображение диалогового окна выбора файлов
  def show_file_dialog(self):
    file_names, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "All Files (*);;Text Files (*.txt)")
    self.attachedDocuments_selectedАilesLbl.setText("Выбранные файлы: " + ", ".join(file_names)) # отображение выбранных файлов в метке

# Вызов кода только в этом файле
if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())