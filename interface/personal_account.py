from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel

# WINDOW
from interface.personal_applications import PersonalApplication

# WIDGETS
from interface.widgets.user_information import UserInformation

# DATABASE
from database.requests import *

class PersonalAccount(QMainWindow):
  def __init__(self, selection_window):
    super().__init__()
    
    # Настройки окна
    self.setWindowTitle("IDVisitor")
    self.setFixedSize(600, 400)
    self.setCentralWidget(QWidget())

    # Инициализация переменных
    self.selection_window = selection_window
    self.user_information = UserInformation()
    self.info_user_arr = getting_user_information()
    
    self.initGUI()
    
  def initGUI(self):
    grid = QGridLayout() # сетка

    title = QLabel("Информация о пользователе")
    title.setStyleSheet("font-size: 20px; font-weight: bold;")

    btn_personal_applications = QPushButton("Личные заявки")
    btn_personal_applications.clicked.connect(lambda: self.show_personal_applications())
    btn_group_applications = QPushButton("Групповые заявки")
    applications = QHBoxLayout()
    applications.addWidget(btn_personal_applications)
    applications.addWidget(btn_group_applications)
    
    btn_return_back = QPushButton("Назад")
    btn_return_back.clicked.connect(lambda: self.return_back())
    
    
    # добавление к grid
    grid.addWidget(title, 0, 0)
    grid.addWidget(self.user_information, 1, 0)
    grid.addLayout(applications, 2, 0)
    grid.addWidget(btn_return_back, 3, 0)
    
    # настройки положения grid
    grid.setAlignment(title, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    grid.setAlignment(self.user_information, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    grid.setAlignment(applications, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    grid.setAlignment(btn_return_back, Qt.AlignmentFlag.AlignBottom)
    
    self.centralWidget().setLayout(grid) # размещение элементов в окне
    
  # ОКНО ЛИЧНЫХ ЗАЯВОК
  def show_personal_applications(self):
    self.close()
    PersonalApplication(self).show()
    
  # ВОЗВРАЩЕНИЕ К ПРЕДЫДУЩЕМУ ОКНУ
  def return_back(self):
    self.close()
    self.selection_window.show()