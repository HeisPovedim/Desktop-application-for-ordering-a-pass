from PyQt6.QtWidgets import QApplication, QMainWindow

class Test(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setFixedSize(600, 600)
    
    self.show()