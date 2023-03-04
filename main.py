import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Задаем фиксированный размер главного окна
        self.setFixedSize(600, 400)

        # Создаем виджет, на котором будут расположены картинки и подписи
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Создаем лейблы для каждой картинки и подписи
        label1 = QLabel(widget)
        label1.setPixmap(QPixmap("./img/one.jpg").scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        label1.move(25, 50)
        caption1 = QLabel("Image 1", widget)
        caption1.move(105, 315)

        label2 = QLabel(widget)
        label2.setPixmap(QPixmap("./img/group.jpg").scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        label2.move(325, 50)
        caption2 = QLabel("Image 2", widget)
        caption2.move(405, 315)

        # Привязываем к лейблам события нажатия на них
        label1.mousePressEvent = lambda event: self.open_new_window()
        label2.mousePressEvent = lambda event: self.open_new_window()

    def open_new_window(self):
        # Создаем новое окно и задаем его фиксированный размер
        new_window = QMainWindow(self)
        new_window.setFixedSize(600, 400)

        # Создаем кнопку назад и привязываем к ней событие нажатия
        back_button = QPushButton("Back", new_window)
        back_button.move(260, 200)
        back_button.clicked.connect(lambda: self.show_main_window(new_window))

        # Привязываем к новому окну событие закрытия окна
        new_window.closeEvent = lambda event: self.show_main_window(new_window)

        # Показываем новое окно
        new_window.show()
        self.hide()

    def show_main_window(self, new_window):
        # Показываем главное окно и закрываем новое окно
        new_window.hide()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())