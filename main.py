import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QGridLayout, QLineEdit, QCalendarWidget, QComboBox, QPushButton, QFileDialog, QDateEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание виджета окна и его отображение
        self.setWindowTitle('Заявка на посещение')
        self.setGeometry(100, 100, 400, 200)

        # Создание основного виджета и размещение на нем компонентов
        widget = QWidget(self)
        self.setCentralWidget(widget)
        grid_layout = QGridLayout(widget)

        # Создание и размещение компонентов для выбора срока действия заявки
        # start_date_label = QLabel('C', self)
        # end_date_label = QLabel('По', self)
        # self.start_date_edit = QLineEdit(self)
        # self.end_date_edit = QLineEdit(self)
        # self.start_date_edit.setReadOnly(True)
        # self.end_date_edit.setReadOnly(True)
        # self.start_date_edit.mousePressEvent = lambda event: self.select_date(event, self.start_date_edit)
        # self.end_date_edit.mousePressEvent = lambda event: self.select_date(event, self.end_date_edit)
        # grid_layout.addWidget(start_date_label, 0, 0)
        # grid_layout.addWidget(self.start_date_edit, 0, 1)
        # grid_layout.addWidget(end_date_label, 1, 0)
        # grid_layout.addWidget(self.end_date_edit, 1, 1)
        

        # Создание и размещение компонентов для выбора цели посещения
        purpose_label = QLabel('Цель посещения', self)
        self.purpose_combo = QComboBox(self)
        self.purpose_combo.addItems(['Конференция', 'Семинар', 'Встреча'])
        grid_layout.addWidget(purpose_label, 2, 0)
        grid_layout.addWidget(self.purpose_combo, 2, 1)

        # Создание и размещение кнопки отправки заявки
        self.submit_button = QPushButton('Отправить', self)
        self.submit_button.clicked.connect(self.submit_request)
        grid_layout.addWidget(self.submit_button, 3, 0, 1, 2)

    

    def select_date(self, event, edit):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked.connect(lambda date: self.set_date(date, edit, cal))
        cal.setGeometry(400, 400, 200, 200)
        cal.show()

    def set_date(self, date, edit, cal):
        edit.setText(date.toString())
        cal.deleteLater()

    def submit_request(self):
        start_date = self.start_date_edit.text()
        end_date = self.end_date_edit.text()
        purpose = self.purpose_combo.currentText()
        print(f'Заявка на посещение отправлена\nC: {start_date}\nПо: {end_date}\nЦель: {purpose}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
