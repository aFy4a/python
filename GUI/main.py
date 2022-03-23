import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer
import main_window
import window_loading
import window_result

AGE = ""


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_btn_calculate.clicked.connect(self.check)

    def check(self):
        if self.main_lineEdit_age.text():
            global AGE
            AGE = self.main_lineEdit_age.text()
            self.close()
            self.window_loading = WindowLoading()
            self.window_loading.show()


class WindowLoading(QtWidgets.QMainWindow, window_loading.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(100, self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.close()
            self.window_result = WindowResult()
            self.window_result.show()

        i = random.randint(1, 3)
        self.step += i
        self.loading_progressBar.setValue(self.step)


class WindowResult(QtWidgets.QMainWindow, window_result.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.result_label.setText("Вам " + AGE + " лет.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
