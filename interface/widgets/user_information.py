from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QLabel

# DATABASE
from database.requests import *

class UserInformation(QGroupBox):
  def __init__(self):
    super().__init__()
    
    # Инициализация переменных
    self.info_user_arr = getting_user_information()
    
    self.initGUI()
    
  def initGUI(self):
    group = QHBoxLayout() # сетка
    self.setLayout(group)

    group.addWidget(QLabel(f"ID: {self.info_user_arr['id']}"))
    group.addWidget(QLabel(f"Email: {self.info_user_arr['email']}"))
    group.addWidget(QLabel(f"Login: {self.info_user_arr['login']}"))