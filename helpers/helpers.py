from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit

import re

def add_widgets_to_layout(layout, widgets):
  for widget in widgets:
    layout.addWidget(widget)

def create_date_edit_with():
  date_edit = QDateEdit()
  date_edit.setCalendarPopup(True)  # включение календаря
  date_edit.setMinimumDate(QDate.currentDate()) # выбор даты не меньше текущей
  date_edit.setMaximumDate( # макс можно выбрать на 15 вперед от текущей даты
    QDate.currentDate().addDays(15)
  )
  date_edit.setFixedWidth(150)
  return date_edit

def capitalize_text(selection, text):
  array = ["FIO", "Surname", "Other"]
  if selection == array[0]: # FIO
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s ]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text
  elif selection == array[1]: # Surname
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s-]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text
  elif selection == array[2]:
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text