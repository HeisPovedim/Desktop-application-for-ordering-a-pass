from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit

import re

# Автоматическое добавление виджетов
def add_widgets_to_layout(layout, widgets):
  for widget in widgets:
    layout.addWidget(widget)

# Создание поля с датой
def create_date_edit_with():
  date_edit = QDateEdit()
  date_edit.setCalendarPopup(True)  # включение календаря
  date_edit.setMinimumDate(QDate.currentDate()) # выбор даты не меньше текущей
  date_edit.setMaximumDate( # макс можно выбрать на 15 вперед от текущей даты
    QDate.currentDate().addDays(15)
  )
  date_edit.setFixedWidth(150)
  return date_edit

# Проверка на длину
def check_three_words(text):
  words = text.split()
  if len(words) == 3:
    return True
  else:
    return False
