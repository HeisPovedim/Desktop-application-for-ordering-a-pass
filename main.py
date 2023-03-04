import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QGridLayout, QLineEdit, QCalendarWidget, QComboBox, QPushButton, QFileDialog, QDateEdit, QVBoxLayout

# Форма: Информация для пропуска
class FormInfoPass(QWidget):
  def __init__(self):
    super().__init__()

    # Создание виджета окна и его отображение
    self.setWindowTitle('Информация для пропуска')
    self.setGeometry(50, 50, 100, 100)

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Создание виджета окна и его отображение
    self.setWindowTitle('Форма записи на посещение мероприятия')
    self.setGeometry(100, 100, 600, 400)

    # Создание основного виджета и размещение на нем компонентов
    widget = QWidget(self)
    self.setCentralWidget(widget)
    grid_layout = QGridLayout(widget)
    
    # Размещение форм
    self.setCentralWidget(FormInfoPass())

if __name__ == '__main__':
  app = QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show() 
  sys.exit(app.exec())
