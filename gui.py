import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QFileDialog, QLabel
import funcs_detect



class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    rectangles= []
    path=""
    #鼠标点击事件
    def mousePressEvent(self,event):
        print("点击事件")
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
    #鼠标释放事件
    def mouseReleaseEvent(self,event):
        print("释放事件")
        self.flag = False
        print(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
    #鼠标移动事件
    def mouseMoveEvent(self,event):
        # print("移动事件")
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
    #绘制事件
    def paintEvent(self, event):
        # print("绘制事件")
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)


class Ui_MainWindow(object):
    path_flag=False
    mosaic_flag=False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 870)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = MyLabel(self.centralwidget)
        # self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 1280, 720))
        self.label.setText("")
        self.label.setObjectName("label")
        background = QtGui.QPixmap("pictures/background.jpg")
        self.label.setPixmap(background)

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(20, 735,1000, 30))
        self.label1.setText("欢迎使用人脸马赛克系统！")
        self.label1.setObjectName("label1")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(330, 755, 611, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        # self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_5.setObjectName("pushButton_5")
        # self.horizontalLayout.addWidget(self.pushButton_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1299, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.menu.addAction(self.actionopen)
        self.menu.addAction(self.actionsave)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.slot)
        self.pushButton_1.clicked.connect(self.slot1)
        self.pushButton_2.clicked.connect(self.slot2)
        self.pushButton_3.clicked.connect(self.slot3)
        self.pushButton_4.clicked.connect(self.slot4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def slot(self):
        path,type=QFileDialog.getOpenFileName()
        print("导入图片路径:")
        print(path)
        if path!="":
            self.label.path=path
            self.path_flag=True
            self.mosaic_flag=False
            self.label1.setText(path)
            jpg = QtGui.QPixmap(path)
            self.label.setPixmap(jpg)

    def slot1(self):
        if self.path_flag:
            path = self.label1.text()
            self.label.rectangles=funcs_detect.detect(path)
            jpg_tempout = QtGui.QPixmap("img_tempout/detect.jpg")
            self.label.setPixmap(jpg_tempout)
            self.mosaic_flag=True


    def slot2(self):
        if self.mosaic_flag:
            jpg = cv2.imread(self.label.path)
            funcs_detect.do_auto_dogtag(self.label.rectangles,jpg)
            jpg_tempout_mosaic = QtGui.QPixmap("img_tempout/dogtag.jpg")
            self.label.setPixmap(jpg_tempout_mosaic)

    def slot3(self):
        if self.mosaic_flag:
            path = self.label1.text()
            jpg = cv2.imread("img_tempout/mosaic.jpg")
            jpg_name = path[55:-4]
            jpg_prefix = path[0:50]
            jpg_savepath = jpg_prefix + "imgs_out/" + jpg_name + "_out.jpg"
            cv2.imwrite(jpg_savepath, jpg)


    def slot4(self):
        if self.mosaic_flag:
            print(self.label.x0)
            jpg = cv2.imread("img_tempout/mosaic.jpg")
            print("222222222")
            funcs_detect.do_manual_mosaic(jpg, self.label.x0, self.label.y0, abs(self.label.x1 - self.label.x0),
                                   abs(self.label.y1 - self.label.y0), 9)
            print("1111111111")
            cv2.imwrite("img_tempout/mosaic.jpg", jpg)
            jpg_tempout = QtGui.QPixmap("img_tempout/mosaic.jpg")
            self.label.setPixmap(jpg_tempout)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸马赛克系统"))
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/icon.jpg"))
        MainWindow.setWindowIcon(icon)
        self.pushButton.setText(_translate("MainWindow", "导入文件"))
        self.pushButton_1.setText(_translate("MainWindow", "人脸检测"))
        self.pushButton_2.setText(_translate("MainWindow", "自动马赛克"))
        self.pushButton_3.setText(_translate("MainWindow", "保存文件"))
        self.pushButton_4.setText(_translate("MainWindow", "手动马赛克"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.actionopen.setText(_translate("MainWindow", "打开"))
        self.actionsave.setText(_translate("MainWindow", "保存"))