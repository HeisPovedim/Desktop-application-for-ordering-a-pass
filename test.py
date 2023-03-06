import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Загрузить фото")
        self.setGeometry(100, 100, 500, 500)

        # Добавление кнопки "Загрузить фото"
        self.button = QPushButton("Загрузить фото", self)
        self.button.setGeometry(50, 50, 150, 50)
        self.button.clicked.connect(self.load_image)

        # Добавление области для отображения фотографии
        self.label = QLabel(self)
        self.label.setGeometry(50, 110, 400, 400)

        # Загрузка фотографии по умолчанию
        self.default_image = QPixmap("./img/group.jpg")
        self.label.setPixmap(self.default_image)
        self.label.setScaledContents(True)

    def load_image(self):
        # Открытие диалогового окна для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")

        if file_name:
            # Загрузка выбранного изображения
            image = QPixmap(file_name)
            self.label.setPixmap(image)
            self.label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())