from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton

class PersonalAccount(QMainWindow):
  def __init__(self, selection_window):
    super().__init__()
    
    # Настройки окна
    self.setWindowTitle("Персональный аккаунт")
    self.setFixedSize(600, 400)
    self.setCentralWidget(QWidget())

    
    self.initGUI()
    
  def initGUI(self):
    
    pass