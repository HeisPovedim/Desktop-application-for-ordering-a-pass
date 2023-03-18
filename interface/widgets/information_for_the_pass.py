# ВИДЖЕТ - ИНФОРМАЦИЯ ДЛЯ ПРОПУСКА
from PyQt6.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt

# HELPERS
from helpers.helpers import *

class InformationPass(QGroupBox):
  def __init__(self):
    super().__init__()
    self.setTitle("Информация для пропуска")
    
    # Инициализация переменных
    self.dateAbout = None
    self.dateWith = None
    self.comboBox = None
    
    self.initGUI()
  def initGUI(self):
    grid = QGridLayout()  # создание сетки
    grid.setAlignment(    # выравнивание сетки
      Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
    )
    self.setLayout(grid) # добавление сетки в группу

    self.dateWith = create_date_edit_with()  # создание поля с датой "с*"
    self.dateAbout = create_date_edit_with() # создание поля с датой "по*"

    self.dateWith.dateChanged.connect(self.update_max_date)  # обновление даты после её выбора

    groupDate = QHBoxLayout()  # создание группового горизонтального блока с полями даты
    add_widgets_to_layout(
      groupDate,
      [QLabel("c"), self.dateWith, QLabel("по"), self.dateAbout]
    )

    self.comboBox = QComboBox() # строка выбора "Цель посещения"
    self.comboBox.addItems(     # добавление списка из состоящего из массива
      ["Ознакомление", "Экскурсия", "Мне просто спросить"]
    )

    grid.addWidget(QLabel("Срок действия заявки*:"), 0, 0)  # 1-я строка
    grid.addLayout(groupDate, 1, 0)                         # 2-я строка
    grid.addWidget(QLabel("Цель посещения*:"), 2, 0)        # 3-я строка
    grid.addWidget(self.comboBox, 3, 0)                     # 4-я строка

    # ОБНОВЛЕНИЕ ДАТЫ
  def update_max_date(self):
    self.dateAbout.setMinimumDate(self.dateWith.date())
    self.dateAbout.setMaximumDate(self.dateWith.date().addDays(15))