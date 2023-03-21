from PyQt6.QtWidgets import (
  QMainWindow, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel,
  QTableWidget, QTableWidgetItem, QScrollArea
)

# DATABASE
from database.requests import *

# LIBRARY
import datetime

class PersonalApplication(QMainWindow):
  def __init__(self, personal_account):
    super().__init__()
    
    # Настройки окна
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(600, 400)
    self.setCentralWidget(QWidget())
    
    # Инициализация переменных
    self.personal_account = personal_account
    self.info_application = getting_personal_applications()
    
    self.initGUI()
  
  def initGUI(self):
    grid = QGridLayout() # сетка

    # Создание таблицы
    table = QTableWidget()
    table.setRowCount(len(self.info_application) + 1)
    table.setColumnCount(3)

    # добавление полей в таблицу
    table.setItem(0, 0, QTableWidgetItem("Подразделение для доступа"))
    table.setItem(0, 1, QTableWidgetItem("Дата и время"))
    table.setItem(0, 2, QTableWidgetItem("Статус"))

    # перебор и запись данных в БД
    key_array = ['division', 'creation_time', 'status']
    for i in range(len(self.info_application)):
      for j in range(3):
        if type(self.info_application[i][key_array[j]]) == datetime.datetime:
          date = self.info_application[i][key_array[j]]
          table.setItem(i + 1, j, QTableWidgetItem(date.strftime("%Y-%m-%d %H:%M:%S")))
        else:
          table.setItem(i + 1, j, QTableWidgetItem(self.info_application[i][key_array[j]]))

    # кнопка переноса в предыдущее окно
    btn_return_back = QPushButton("Назад")
    btn_return_back.clicked.connect(lambda: self.return_back())

    # добавление в сетку
    grid.addWidget(table, 0, 0)
    grid.addWidget(btn_return_back, 1, 0)
    
    self.centralWidget().setLayout(grid) # размещение элементов в окне
  
  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.personal_account.show()
    