# coding=utf-8
import time
import sys
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtTest
from Window import *
from io import open

LANGUAGES = {
    'English': 'en',
    'Russian': 'ru',
}

KEYBOARD_LANG = {
    '0x4090409': 'English',
    '0x4190419': 'Russian',
    '-0xf57fbde': 'Russian',
}

EN_LETTER = {
    0: 'Q', 1: 'W', 2: 'E', 3: 'R', 4: 'T', 5: 'Y', 6: 'U', 7: 'I', 8: 'O', 9: 'P',
    12: 'A', 13: 'S', 14: 'D', 15: 'F', 16: 'G', 17: 'H', 18: 'J', 19: 'K', 20: 'L',
    23: 'Z', 24: 'X', 25: 'C', 26: 'V', 27: 'B', 28: 'N', 29: 'M',
}

RU_LETTER = {
    0: 'Й', 1: 'Ц', 2: 'У', 3: 'К', 4: 'Е', 5: 'Н', 6: 'Г', 7: 'Ш', 8: 'Щ', 9: 'З', 10: 'Х', 11: 'Ъ',
    12: 'Ф', 13: 'Ы', 14: 'В', 15: 'А', 16: 'П', 17: 'Р', 18: 'О', 19: 'Л', 20: 'Д', 21: 'Ж', 22: 'Э',
    23: 'Я', 24: 'Ч', 25: 'С', 26: 'М', 27: 'И', 28: 'Т', 29: 'Ь', 30: 'Б', 31: 'Ю',
}

EN_KEY = {
    81: 'Q', 87: 'W', 69: 'E', 82: 'R', 84: 'T', 89: 'Y', 85: 'U', 73: 'I', 79: 'O', 80: 'P', 91: '', 93: '',
    65: 'A', 83: 'S', 68: 'D', 70: 'F', 71: 'G', 72: 'H', 74: 'J', 75: 'K', 76: 'L', 59: '', 39: '',
    90: 'Z', 88: 'X', 67: 'C', 86: 'V', 66: 'B', 78: 'N', 77: 'M', 44: '', 46: '',
    1049: 'Q', 1062: 'W', 1059: 'E', 1050: 'R', 1045: 'T', 1053: 'Y', 1043: 'U', 1064: 'I', 1065: 'O', 1047: 'P', 1061: '', 1066: '',
    1060: 'A', 1067: 'S', 1042: 'D', 1040: 'F', 1055: 'G', 1056: 'H', 1054: 'J', 1051: 'K', 1044: 'L', 1046: '', 1028: '',
    1071: 'Z', 1063: 'X', 1057: 'C', 1052: 'V', 1048: 'B', 1058: 'N', 1068: 'M', 1041: '', 1070: '',
    1031: '', 1069: '', 1030: 'S',
}

RU_KEY = {
    81: 'Й', 87: 'Ц', 69: 'У', 82: 'К', 84: 'Е', 89: 'Н', 85: 'Г', 73: 'Ш', 79: 'Щ', 80: 'З', 91: 'Х', 93: 'Ъ',
    65: 'Ф', 83: 'Ы', 68: 'В', 70: 'А', 71: 'П', 72: 'Р', 74: 'О', 75: 'Л', 76: 'Д', 59: 'Ж', 39: 'Э',
    90: 'Я', 88: 'Ч', 67: 'С', 86: 'М', 66: 'И', 78: 'Т', 77: 'Ь', 44: 'Б', 46: 'Ю',
    1049: 'Й', 1062: 'Ц', 1059: 'У', 1050: 'К', 1045: 'Е', 1053: 'Н', 1043: 'Г', 1064: 'Ш', 1065: 'Щ', 1047: 'З', 1061: 'Х', 1066: 'Ъ',
    1060: 'Ф', 1067: 'Ы', 1042: 'В', 1040: 'А', 1055: 'П', 1056: 'Р', 1054: 'О', 1051: 'Л', 1044: 'Д', 1046: 'Ж', 1028: 'Э',
    1071: 'Я', 1063: 'Ч', 1057: 'С', 1052: 'М', 1048: 'И', 1058: 'Т', 1068: 'Ь', 1041: 'Б', 1070: 'Ю', 1031: 'Ъ', 1069: 'Э', 1030: 'Ы',
}

#start_time = time.time()
Filename_en = "Words/english.txt"
Filename_ru = "Words/russian.txt"

STATUS = False

class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QtWidgets.QWidget.__init__(self, parent)

        self.keyboard_layout()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Filename = Filename_en
        self.ui.field_letter = 0
        self.status = False

        for i in range(32):
            self.ui.letter[i].pressed.connect(lambda v=i: self.input_letter(v))

        self.ui.startButton.clicked.connect(self.startButton)
        self.ui.clearButton.clicked.connect(self.clearButton)
        self.ui.backspace.clicked.connect(self.backspace)
        self.ui.srcLanguage.addItems(LANGUAGES.keys())
        self.ui.srcLanguage.currentTextChanged[str].connect(self.update_src_language)
        self.ui.srcLanguage.setCurrentText('English')

        #self.ui.slider.value()

    def keyboard_layout(self):
        u = ctypes.windll.LoadLibrary("user32.dll")
        pf = getattr(u, "GetKeyboardLayout")
        x_key = hex(pf(0))
        print(KEYBOARD_LANG.get(x_key))


    def startButton(self):
        global STATUS
        if STATUS == False:
            if self.ui.field_letter >= 3:
                self.ui.startButton.setText('STOP')
                QtTest.QTest.qWait(100)
                STATUS = True
                mass = []
                for i in range(self.ui.field_letter):
                    x = (self.ui.field[i].text()).lower()
                    mass.append(x)
                main(mass)
            else:
                self.ui.label_status.show()
                self.ui.label_status.setText("Error!!! Please fill in at least the fields marked in white!!!")
                self.ui.label_status.setAlignment(QtCore.Qt.AlignCenter)
                QtTest.QTest.qWait(1000)
                self.ui.label_status.hide()
        else:
            STATUS = False
            self.ui.startButton.setText('START')

    def clearButton(self):
        for i in range(0, self.ui.field_letter, 1):
            self.ui.field[i].clear()
        self.ui.field_letter = 0

    def input_letter(self, v):
        if self.ui.field_letter == 9:
            print('None')
        elif EN_LETTER.get(v) == None:
            print('None_1')
        else:
            i = self.ui.field_letter
            if self.ui.Filename == 'Words/english.txt':
                self.ui.field[i].setText(str(EN_LETTER.get(v)))
            elif self.ui.Filename == 'Words/russian.txt':
                self.ui.field[i].setText(str(RU_LETTER.get(v)))
            if i > 2:
                self.ui.field_fill(i)
            self.ui.field_letter += 1

    def update_src_language(self, l):
        self.language_src = LANGUAGES[l]
        self.ui.key_pos(l)
        if self.ui.Filename == 'Words/english.txt':
            self.ui.Filename = Filename_ru
        elif self.ui.Filename == 'Words/russian.txt':
            self.ui.Filename = Filename_en
        self.ui.srcLanguage.setEnabled(False)
        QtTest.QTest.qWait(100)
        self.ui.srcLanguage.setEnabled(True)
        self.clearButton()

    def backspace(self):
        try:
            if self.ui.field_letter == 0:
                pass
            else:
                self.ui.field_letter -= 1
                i = self.ui.field_letter
                self.ui.field[i].clear()
            if i > 2:
                self.ui.field_clear(i)
        except:
            pass

    def event_fill(self, event):
        i = self.ui.field_letter
        if self.ui.Filename == 'Words/english.txt':
            self.ui.field[i].setText(str(EN_KEY.get(event.key())))
        elif self.ui.Filename == 'Words/russian.txt':
            self.ui.field[i].setText(str(RU_KEY.get(event.key())))
        if i > 2:
            self.ui.field_fill(i)
        self.ui.field_letter += 1

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Shift or event.key() == Qt.Key_Alt:
            QtTest.QTest.qWait(300)
            u = ctypes.windll.LoadLibrary("user32.dll")
            pf = getattr(u, "GetKeyboardLayout")
            print(hex(pf(0)))
        if event.key() == Qt.Key_Backspace:
            self.backspace()
        elif event.key() == Qt.Key_Return:
            self.startButton()
        elif event.key():
            if self.ui.field_letter == 9:
                pass
            elif self.ui.Filename == 'Words/english.txt':
                if EN_KEY.get(event.key()) is None or EN_KEY.get(event.key()) == '':
                    print('None_1')
                else:
                    self.event_fill(event)
            else:
                self.event_fill(event)


def variations(elements, size):
    ret = []
    for i in combinations(elements, size):
        ret.extend(permutations(i))
    return ret

def combinations(elements, size):
    if len(elements) == size or size == 1:
        return elements

    ret = []
    for i, item in enumerate(elements):
        for j in combinations(elements[i + 1:], size - 1):
            ret.append(item + j)
    return ret

def permutations(elements):
    if len(elements) <= 1:
        return elements

    ret = []
    for i, item in enumerate(elements):
        for j in permutations(elements[:i] + elements[i + 1:]):
            ret.append(item + j)
        ret.append(item)
    return ret

def main(word_list):
    print(word_list)

    #print("--- %s seconds ---" % (time.time() - start_time))
    g = []
    #input = [ "r", "e", "l", "a","t", "t"]
    print("Input {}:".format(input))
    print("Permutations:")
    ret1 = (variations(word_list, len(word_list) - 1))
    ret2 = (permutations(word_list))
    ret = ret1 + ret2
    # print("--- %s seconds ---" % (time.time() - start_time))
    print("Считанные сообщения")
    kol = 0
    with open(myapp.ui.Filename, encoding='utf-8') as file:
        for line in file:
            for i in range(0, len(ret), 1):
                if not STATUS:
                    break
                if ret[i] in line and ret[i] not in g:
                    if len(line) == len(ret[i]) + 1 and len(ret[i]) > 2:
                        g.append(ret[i])
                        print(ret[i])
                        QtTest.QTest.qWait(500)
                        myapp.ui.listWidget.insertItem(kol, ret[i])
                        kol += 1

    myapp.ui.listWidget.insertItem(kol, 'Найдено слов:'+ str(len(g)))
    print(len(g))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

    #print("--- %s seconds ---" % (time.time() - start_time))
