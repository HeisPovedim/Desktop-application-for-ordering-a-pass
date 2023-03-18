# ВИДЖЕТ - ПРИНИМАЮЩАЯ СТОРОНА
from PyQt6.QtWidgets import QGroupBox, QGridLayout, QComboBox, QLineEdit, QLabel
from PyQt6.QtCore import Qt

# LIBRARIES
import re

class ReceivingParty(QGroupBox):
  def __init__(self):
    super().__init__()
    self.setTitle("Принимающая сторона")

    # Инициализация переменных
    self.fio = None
    self.comboBox = None
    
    self.initGUI()

  def initGUI(self):
      grid = QGridLayout()                         # создание сетки
      grid.setAlignment(Qt.AlignmentFlag.AlignTop) # выравнивание по верху группового блока
      self.setLayout(grid)                         # добавление сетки в групповой блок
  
      self.comboBox = QComboBox()                      # строка выбора "Подразделение"
      self.comboBox.addItems(["ТКМП", "ЮФУ", "ГИБДД"]) # добавление списка из состоящего из массива
  
      self.fio = QLineEdit()  # строка ввода фамилии
      self.fio.textChanged.connect(self.validate_input_fio)
      self.fio.textChanged.connect(
        lambda: self.fio.setText(
          re.sub(r'[^а-яА-Я\\s ]', '', self.fio.text().title())
        )
      )
      self.fio.setMaxLength(50)
  
      grid.addWidget(QLabel("Подразделение*:"), 0, 0) # 1-я строка
      grid.addWidget(self.comboBox, 1, 0)             # 2-я строка
      grid.addWidget(QLabel("ФИО*:"), 2, 0)           # 3-я строка
      grid.addWidget(self.fio, 3, 0)                  # 4-я строка

  # ВАЛИДАЦИЯ ФИО НА ВВОД МАКС. 3-Х СЛОВ
  def validate_input_fio(self):
    text = self.fio.text().strip()
    words = text.split()
    if len(words) > 3:
      cursor_pos = self.fio.cursorPosition()
      self.fio.setText(" ".join(words[:3]))
      self.fio.setCursorPosition(cursor_pos - 1)

  # EVENT ВВОДА ФАМИЛИИ (НЕ БОЛЬШЕ 3-Х СЛОВ)
  def keyPressEvent(self, event):
    if event.key() == Qt.Key and len(self.fio.text().split()) >= 3:
      event.ignore()
    else:
      super().keyPressEvent(event)