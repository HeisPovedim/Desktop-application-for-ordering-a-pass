from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QLabel

# DATABASE
from database.requests import *

class PersonalAccount(QMainWindow):
  def __init__(self, selection_window):
    super().__init__()
    
    # Настройки окна
    self.setWindowTitle("Личный кабинет")
    self.setFixedSize(600, 400)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.selection_window = selection_window
    self.info_user_arr = getting_user_information()
    
    self.initGUI()
    
  def initGUI(self):
    grid = QGridLayout() # сетка

    user_information = QLabel("Информация о пользователе")
    user_information.setStyleSheet("font-size: 20px; font-weight: bold;")
    grid.addWidget(user_information, 0, 0, 1, 3)
    
    grid.addWidget(QLabel(f"Id: {self.info_user_arr[0][0]}"), 1, 0)
    grid.addWidget(QLabel(f"Email: {self.info_user_arr[0][1]}"), 1, 1)
    grid.addWidget(QLabel(f"Login: {self.info_user_arr[0][2]}"), 1, 2)
    
    
    btn_return_back = QPushButton("Назад")
    btn_return_back.clicked.connect(lambda: self.return_back())
    grid.addWidget(btn_return_back, 2, 0, 1, 3)
    
    self.centralWidget().setLayout(grid) # размещение элементов в окне
    
  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.selection_window.show()