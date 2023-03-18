# ВИДЖЕТ - КНОПКИ
from PyQt6.QtWidgets import QHBoxLayout, QPushButton


class Buttons(QHBoxLayout):
  def __init__(self):
    super().__init__()

    # Инициализация переменных
    self.further_button = None
    self.back_button = None

    self.initGUI()

  def initGUI(self):
    
    self.back_button = QPushButton("Назад")  # кнопка "Назад"
    self.back_button.setFixedWidth(80)

    self.further_button = QPushButton("Оформить заявку")  # кнопка "Оформить заявку"
    self.further_button.setFixedWidth(120)

    self.addWidget(self.back_button)
    self.addWidget(self.further_button)