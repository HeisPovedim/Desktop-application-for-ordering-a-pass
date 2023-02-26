from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

class Window(QMainWindow):
  def add_label(self):
    print("add")
  
  def __init__(self):
    super(Window, self).__init__()
    
    self.setWindowTitle("Простая программа")
    self.setGeometry(300, 250 ,350, 200)
    
    self.main_text = QtWidgets.QLabel(self)
    self.main_text.setText("Я ебал того рот что она творит")
    self.main_text.move(100, 100)
    self.main_text.adjustSize()
    
    self.btn = QtWidgets.QPushButton(self)
    self.btn.move(70, 150)
    self.btn.setText("Трахни меня")
    self.btn.setFixedWidth(200)
    self.btn.clicked.connect(self.add_label)
    

def application():
  app = QApplication(sys.argv)
  window = Window()
  
  
  
  window.show()
  sys.exit(app.exec_())
  
if __name__ == "__main__":
  application()