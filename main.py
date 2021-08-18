import sys

import cv2

from PyQt5.QtWidgets import QApplication, QMainWindow

import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setFixedSize(1300, 940)

    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

