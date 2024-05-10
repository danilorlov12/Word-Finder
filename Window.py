from PyQt5 import QtCore, QtGui, QtWidgets, QtTest

en_letter = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '', '',
             'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '', '',
             'Z', 'X', 'C', 'V', 'B', 'N', 'M', '', '']

ru_letter = ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ',
             'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э',
             'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю']

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.field_frame = []
        self.letter = []
        self.field = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        with open("Style/style.qss", encoding='utf-8') as f:
            MainWindow.setStyleSheet(f.read())

        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(0, 0, 900, 25))
        self.label_status.setObjectName('labelStatus')
        self.label_status.hide()

        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(400, 470, 130, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.clearButton.setFont(font)
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setText("CLEAR")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(625, 470, 130, 60))
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.startButton.setText("START")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 25, 240, 525))
        font.setPointSize(16)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.keyboard()

        self.srcLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.srcLanguage.setObjectName("srcLanguage")
        self.srcLanguage.setGeometry(QtCore.QRect(320, 40, 125, 30))

        self.lcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd.display(3)
        self.lcd.setGeometry(QtCore.QRect(725, 40, 50, 30))

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(500, 25, 190, 60))
        self.slider.setRange(3, 9)
        self.slider.valueChanged[int].connect(self.lcd.display)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        x, y = 0, 0
        for i in range(9):
            self.startButton.setFont(font)
            self.field.append(QtWidgets.QLabel(self.centralwidget))
            self.field[i].setGeometry(QtCore.QRect(280 + x, 100 + y, 231, 71))
            if i < 3:
                self.field_fill(i)
            else:
                self.field_clear(i)
            font.setPointSize(15)
            self.field[i].setFont(font)
            self.field[i].setAlignment(QtCore.Qt.AlignCenter)
            x += 125
            if i == 4:
                y += 100
                x = 75
        self.field_clear(3)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def field_clear(self, i):
        self.field[i].setStyleSheet('QLabel {min-width: 76px; max-width: 76px; '
                                    'min-height: 76px; max-height: 76px;'
                                    'border-radius: 38px; border-style: solid; '
                                    'border-color: black; border-width: 2px;}')

    def field_fill(self, i):
        self.field[i].setStyleSheet('QLabel { background-color: #ffffff; '
                                    'min-width: 76px; max-width: 76px; '
                                    'min-height: 76px; max-height: 76px;'
                                    'border-radius: 38px; border-style: solid; '
                                    'border-color: black; border-width: 2px;}')

    def keyboard(self):
        x, y = 0, 0
        font = QtGui.QFont()
        font.setPointSize(15)
        for i in range(32):
            self.letter.append(QtWidgets.QPushButton(self.centralwidget))
            self.letter[i].setGeometry(QtCore.QRect(280 + x, 310 + y, 43, 43))
            self.letter[i].setText(en_letter[i])
            self.letter[i].setFont(font)
            x += 50
            if i == 11:
                y += 50
                x = 25
            elif i == 22:
                x = 50
                y += 50
        self.backspace = QtWidgets.QPushButton(self.centralwidget)
        self.backspace.setGeometry(QtCore.QRect(780, 410, 90, 43))
        self.backspace.setText('Backspace')
        font = QtGui.QFont()
        font.setPointSize(10)
        self.backspace.setFont(font)

    def key_pos(self, lang):
        if lang == 'English':
            list = en_letter
        elif lang == 'Russian':
            list = ru_letter
        for i in range(32):
            self.letter[i].setText(list[i])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
