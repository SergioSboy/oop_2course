from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QHBoxLayout, QBoxLayout, QGroupBox, QMenuBar, QMenu, QDialog, QFileDialog, QComboBox, QTextEdit, QMessageBox, \
    QInputDialog

import sys
import studenty
import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.bigEditor = QTextEdit()
        self.bigEditor.setFontFamily("Consolas");


        self.createFileGroupBox()
        self.createReportGroupBox()

        self.setWindowTitle("Студенты")
        self.setMinimumWidth(650)
        self.setMinimumHeight(400)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.fileGroupBox)
        mainLayout.addWidget(self.reportGroupBox)
        mainLayout.addWidget(self.bigEditor)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def createFileGroupBox(self):
        self.fileGroupBox = QGroupBox("Файл данных")
        layout = QHBoxLayout()

        self.edtFile = QLineEdit()
        self.edtFile.setPlaceholderText('Введите путь к файлу данных')
        layout.addWidget(self.edtFile)

        btnFile = QPushButton("Выбрать файл данных")
        btnFile.setFixedWidth(150)
        btnFile.clicked.connect(self.open_file_dialog)
        layout.addWidget(btnFile)

        self.fileGroupBox.setLayout(layout)

    def createReportGroupBox(self):
        self.reportGroupBox = QGroupBox("Файл данных")
        layout = QHBoxLayout()

        self.cb_report = QComboBox(self)
        self.cb_report.addItem('Общая ведомость')
        self.cb_report.addItem('Справка о студенте по номеру зачетки')
        self.cb_report.addItem('Ведомость о выполнении студентами задания с указанным номером')
        self.cb_report.addItem('Список студентов с заданным номером варианта, имеющих заданную сумму баллов по всем 3 задачам')
        self.cb_report.addItem('Список студентов, не получивших задание с указанным номером')
        self.cb_report.activated.connect(self.report_update)

        layout.addWidget(self.cb_report)
        
        self.reportParamGroupBox = QGroupBox("Параметрый отчет")
        self.reportParamGroupBox.setFixedWidth(250);
        layout2 = QHBoxLayout()
        self.edtVariant = QLineEdit()
        self.edtVariant.setPlaceholderText('Введите вариант')
        self.edtSum = QLineEdit()
        self.edtSum.setPlaceholderText('Введите сумму')
        layout2.addWidget(self.edtVariant)
        layout2.addWidget(self.edtSum)
        self.reportParamGroupBox.setLayout(layout2)
        self.reportParamGroupBox.setVisible(self.cb_report.currentIndex() == 3);
        layout.addWidget(self.reportParamGroupBox)

        btnFile = QPushButton("Выполнить")
        btnFile.setFixedWidth(90)
        btnFile.clicked.connect(self.report)
        layout.addWidget(btnFile)

        self.reportGroupBox.setLayout(layout)


    def report(self):
        # чистим старые данные
        self.bigEditor.clear()

        if  self.edtFile.text() == '':
            QMessageBox.about(self, "Ошибка", "Выберите файл данных")
            return

        if self.cb_report.currentIndex() == 0:
            result = studenty.getGeneralStatement(self.edtFile.text())
            self.bigEditor.append(result)
        elif self.cb_report.currentIndex() == 1:
            # Справка о студенте по номеру зачетки
            id, okPressed = QInputDialog.getInt(self, '', 'Введите номер зачетки')
            if okPressed:
                result = studenty.getStudentById(self.edtFile.text(), id)
                self.bigEditor.append(result)
        elif self.cb_report.currentIndex() == 2:
            # Ведомость о выполнении студентами задания с указанным номером
            id, okPressed = QInputDialog.getInt(self, '', 'Введите номер задания')
            if okPressed:
                result = studenty.getTaskByNumber(self.edtFile.text(), id)
                self.bigEditor.append(result)
                
        elif self.cb_report.currentIndex() == 3:
            # Список студентов с заданным номером варианта, имеющих заданную сумму баллов по всем 3 задачам
            result = studenty.getStudentListBySum(self.edtFile.text(), int(self.edtVariant.text()), int(self.edtSum.text()))
            print(result)
            self.bigEditor.append(result)      
        elif self.cb_report.currentIndex() == 4:
            # писок студентов, не получивших задание с указанным номером
            id, okPressed = QInputDialog.getInt(self, '', 'Введите номер задания', 1, 1, 3)
            if okPressed:
                result = studenty.getStudentListNotTaskByNumber(self.edtFile.text(),  str(id))
                self.bigEditor.append(result)                              
                 
        else:
            QMessageBox.about(self, "Ошибка", "Не выбрана форма отчета")


    def report_update(self):
        # чистим старые данные
        self.bigEditor.clear()
        self.reportParamGroupBox.setVisible(self.cb_report.currentIndex() == 3);

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory('')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("dat (*.dat)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.edtFile.setText(filenames[0])


app = QApplication(sys.argv)
window = MainWindow()
window.show()
# app.exec()
sys.exit(app.exec())