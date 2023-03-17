# ВИДЖЕТ - ПРИКРЕПЛЯЕМЫЕ ДОКУМЕНТЫ
from PyQt6.QtWidgets import QGroupBox, QFormLayout, QPushButton, QLabel, QMessageBox, QFileDialog
import os

class AttachingDocuments(QGroupBox):
  def __init__(self):
    super().__init__()
    self.setTitle("Прикрепляемые документы")
    self.setFixedWidth(700)

    # Инициализация переменных
    self.file_document_name = None
    self.file_document = None
    self.selectedAilesLbl = None
    
    self.initGUI()
    
  def initGUI(self):
    formLayout = QFormLayout()  # создаем форму
    self.setLayout(formLayout)  # добавление формы в групповой блок
  
    chooseFileBtn = QPushButton("Выбрать файлы")  # cоздание кнопки для вызова диалога выбора файлов
    chooseFileBtn.clicked.connect(self.load_document)
    self.selectedAilesLbl = QLabel()  # метка для отображения выбранных файлов
    formLayout.addRow(chooseFileBtn)
    formLayout.addRow(self.selectedAilesLbl)

  # ЗАГРУЗКА ФАЙЛА
  def load_document(self):
    try:
      self.file_document, _ = QFileDialog.getOpenFileName(self, "Выберите файлы", "", "*.pdf")
      self.file_document_name = os.path.basename(self.file_document)
      self.selectedAilesLbl.setText("Выбранные файлы: " + self.file_document)
    except Exception as error:
      QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файлы: {error}")