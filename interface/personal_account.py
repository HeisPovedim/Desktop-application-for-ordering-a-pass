from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel

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
    grid.addWidget(user_information, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    
    info_user = QHBoxLayout()
    info_user.addWidget(QLabel(f"Id: {self.info_user_arr[0]['id']}"))
    info_user.addWidget(QLabel(f"Email: {self.info_user_arr[0]['email']}"))
    info_user.addWidget(QLabel(f"Login: {self.info_user_arr[0]['login']}"))
    grid.addLayout(info_user, 1, 0, Qt.AlignmentFlag.AlignBottom)
    
    btn_return_back = QPushButton("Назад")
    btn_return_back.clicked.connect(lambda: self.return_back())
    grid.addWidget(btn_return_back, 2, 0, 1, 3, Qt.AlignmentFlag.AlignBottom)
    
    self.centralWidget().setLayout(grid) # размещение элементов в окне
    
  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.selection_window.show()