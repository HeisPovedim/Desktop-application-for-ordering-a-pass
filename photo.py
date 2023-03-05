from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class Example(QWidget):
    def __init__(self):
        super().__init__()

        # Создание кнопки для вызова диалога выбора файлов
        self.choose_file_btn = QPushButton("Выбрать файлы")
        self.choose_file_btn.clicked.connect(self.show_file_dialog)

        # Метка для отображения выбранных файлов
        self.selected_files_lbl = QLabel()

        # Создание вертикального макета и добавление в него кнопки и метки
        vbox = QVBoxLayout()
        vbox.addWidget(self.choose_file_btn)
        vbox.addWidget(self.selected_files_lbl)

        # Установка вертикального макета в качестве макета главного окна
        self.setLayout(vbox)

    def show_file_dialog(self):
        # Отображение диалогового окна выбора файлов
        file_names, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "All Files (*);;Text Files (*.txt)")

        # Отображение выбранных файлов в метке
        self.selected_files_lbl.setText("Выбранные файлы: " + ", ".join(file_names))

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec()
