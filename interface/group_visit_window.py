from PyQt6.QtWidgets import QMainWindow, QPushButton

class GroupVisit(QMainWindow):
  def __init__(self,start_window):
    super().__init__()
    
    self.setFixedSize(600, 400)
    # self.setCentralWidget(QWidget())
    
    self.start_window = start_window
  
    # создаем кнопку назад и привязываем к ней событие нажатия
    self.back_button = QPushButton("Назад", self)
    self.back_button.move(260, 200)
    self.back_button.clicked.connect(lambda: self.show_main_window())
    
  def show_main_window(self):
    # показываем главное окно и закрываем новое окно
    self.start_window.show()
    self.hide()

  # СОБЫТИЕ НА ЗАКРЫТИЕ ОКНА
  def closeEvent(self, event):
    self.start_window.show()
    self.hide()
