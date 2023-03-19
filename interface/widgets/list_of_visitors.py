# ВИДЖЕТ - ПРИКРЕПЛЯЕМЫЕ ДОКУМЕНТЫ
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QGridLayout, QPushButton, QLabel, QMessageBox, QFileDialog

# LIBRARIES
import os

class ListOfVisitors(QGroupBox):
  def __init__(self):
    super().__init__()
    self.setTitle("Список посетителей")
    self.setFixedWidth(277)
    
    # Инициализация переменных
    self.file_document_name = None
    self.file_document = None
    self.path = None
    
    self.initGUI()
  
  def initGUI(self):
    grid = QGridLayout()  # создаем форму
    grid.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.setLayout(grid)  # добавление формы в групповой блок
    
    chooseFileBtn = QPushButton("Выбрать файлы")  # cоздание кнопки для вызова диалога выбора файлов
    chooseFileBtn.clicked.connect(self.load_document)
    self.path = QLabel()  # метка для отображения выбранных файлов
    grid.addWidget(QLabel("Загрузите список посетителей в xlsx."), 0, 0)
    grid.addWidget(chooseFileBtn, 1, 0)
    grid.addWidget(self.path, 2, 0)
  
  # ЗАГРУЗКА ФАЙЛА
  def load_document(self):
    try:
      self.file_document, _ = QFileDialog.getOpenFileName(self, "Выберите файлы", "", "*.xlsx")
      self.file_document_name = os.path.basename(self.file_document)
      self.path.setText("Выбранный файл: " + self.file_document_name)
      self.path.setWordWrap(True)
    except Exception as error:
      QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файлы: {error}")