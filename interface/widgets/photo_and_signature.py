from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGridLayout, QLabel

class PhotoAndSignature(QGridLayout):
  def __init__(self):
    super().__init__()

    # Инициализация переменных
    self.individual_photo = None
    self.individual_signature = None
    self.group_photo = None
    self.group_signature = None

    self.initGUI()
    
  def initGUI(self):
    individual_box = QGridLayout()
    
    self.individual_photo = QLabel()
    self.individual_photo.setPixmap(
      QPixmap("./assets/img/one.jpg").scaled(250, 250, transformMode=Qt.TransformationMode.SmoothTransformation)
    )
    self.individual_signature = QLabel("Личное посещение")

    individual_box.addWidget(self.individual_photo, 0, 0, Qt.AlignmentFlag.AlignHCenter)
    individual_box.addWidget(self.individual_signature, 1, 0, Qt.AlignmentFlag.AlignHCenter)

    group_box = QGridLayout()

    self.group_photo = QLabel()
    self.group_photo.setPixmap(
      QPixmap("./assets/img/group.jpg").scaled(250, 250, transformMode=Qt.TransformationMode.SmoothTransformation)
    )
    self.group_signature = QLabel("Групповое посещение")

    group_box.addWidget(self.group_photo, 0, 0, Qt.AlignmentFlag.AlignHCenter)
    group_box.addWidget(self.group_signature, 1, 0, Qt.AlignmentFlag.AlignHCenter)


    self.addLayout(individual_box, 0, 0)
    self.addLayout(group_box, 0, 1)