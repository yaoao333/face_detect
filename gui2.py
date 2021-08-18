import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QAction, QLabel, QFileDialog

import funcs_detect


class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    moveFlag=0
    openFlag=0
    formerFlag=0
    motionFlag=0
    flag = False
    rectangles= []
    path=""
    #鼠标点击事件
    def mousePressEvent(self,event):
        if self.openFlag==1:
            self.moveFlag = 0
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
    #鼠标释放事件
    def mouseReleaseEvent(self,event):
        if self.openFlag == 1:
            self.flag = False
            if self.moveFlag == 0:
                self.x0 = 0
                self.x1 = 0
                self.y0 = 0
                self.y1 = 0
                temp = QtGui.QPixmap("img_tempout/cover.jpg")
                self.setPixmap(temp)
    #鼠标移动事件
    def mouseMoveEvent(self,event):
            self.moveFlag = 1
            if self.flag:
                self.x1 = event.x()
                self.y1 = event.y()
                self.update()
    #绘制事件
    def paintEvent(self, event):
            super().paintEvent(event)
            rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)

class Ui_MainWindow(object):

    path_flag = False
    detect_flag = False
    coverType = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_img = MyLabel(self.centralwidget)
        self.label_img.setGeometry(QtCore.QRect(10, 10, 1280, 720))
        self.label_img.setText("")
        self.label_img.setObjectName("label_img")
        background = QtGui.QPixmap("pictures/background.jpg")
        self.label_img.setPixmap(background)

        # self.label_img = QtWidgets.QLabel(self.centralwidget)
        # self.label_img.setGeometry(QtCore.QRect(10, 0, 1280, 720))
        # self.label_img.setObjectName("label_img")

        self.label_path = QtWidgets.QLabel(self.centralwidget)
        self.label_path.setGeometry(QtCore.QRect(10, 740, 1280, 30))
        self.label_path.setObjectName("label_path")
        self.label_path.setText("欢迎使用人脸马赛克系统，请先打开照片！")

        self.label_message = QtWidgets.QLabel(self.centralwidget)
        self.label_message.setGeometry(QtCore.QRect(10, 775, 1280, 30))
        self.label_message.setObjectName("label_message")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(500, 805, 250, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # self.pushButton_open = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_open.setObjectName("pushButton_open")
        # self.horizontalLayout.addWidget(self.pushButton_open)
        #
        # self.pushButton_detect = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_detect.setObjectName("pushButton_detect")
        # self.horizontalLayout.addWidget(self.pushButton_detect)
        #
        # self.pushButton_auto = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_auto.setObjectName("pushButton_auto")
        # self.horizontalLayout.addWidget(self.pushButton_auto)
        #
        # self.pushButton_manual = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_manual.setObjectName("pushButton_manual")
        # self.horizontalLayout.addWidget(self.pushButton_manual)
        #
        # self.pushButton_erase = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_erase.setObjectName("pushButton_erase")
        # self.horizontalLayout.addWidget(self.pushButton_erase)
        #
        # self.pushButton_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_save.setObjectName("pushButton_save")
        # self.horizontalLayout.addWidget(self.pushButton_save)
        #
        self.label_coverType = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_coverType.setObjectName("label_coverType")
        self.horizontalLayout.addWidget(self.label_coverType)

        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 22))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_set = QtWidgets.QMenu(self.menubar)
        self.menu_set.setObjectName("menu_set")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        open=QAction(QIcon("pictures/open.jpg"),"打开",self.toolBar)
        self.toolBar.addAction(open)
        detect = QAction(QIcon("pictures/detect.jpg"), "检测人脸", self.toolBar)
        self.toolBar.addAction(detect)
        auto_cover = QAction(QIcon("pictures/cover.jpg"), "自动遮挡", self.toolBar)
        self.toolBar.addAction(auto_cover)
        manual_cover = QAction(QIcon("pictures/manual.jpg"), "手动遮挡", self.toolBar)
        self.toolBar.addAction(manual_cover)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        former = QAction(QIcon("pictures/former.jpg"), "上一步", self.toolBar)
        self.toolBar.addAction(former)
        next = QAction(QIcon("pictures/next.jpg"), "下一步", self.toolBar)
        self.toolBar.addAction(next)
        clean = QAction(QIcon("pictures/clean.jpg"), "清除", self.toolBar)
        self.toolBar.addAction(clean)
        restart = QAction(QIcon("pictures/restart.jpg"), "重新加载", self.toolBar)
        self.toolBar.addAction(restart)
        save = QAction(QIcon("pictures/save.jpg"), "保存", self.toolBar)
        self.toolBar.addAction(save)
        self.toolBar.actionTriggered[QAction].connect(self.toolbtnpressed)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.action_import = QtWidgets.QAction(MainWindow)
        self.action_import.setObjectName("action_import")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.menu_file.addAction(self.action_import)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_exit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_set.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        # self.pushButton_open.clicked.connect(self.slot_open)
        # self.pushButton_detect.clicked.connect(self.slot_detect)
        # self.pushButton_auto.clicked.connect(self.slot_auto)
        # self.pushButton_manual.clicked.connect(self.slot_manual)
        # self.pushButton_erase.clicked.connect(self.slot_erase)
        # self.pushButton_save.clicked.connect(self.slot_save)
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def toolbtnpressed(self,a):
        if a.text()=="打开":
            self.slot_open()
        elif a.text()=="检测人脸":
            self.slot_detect()
        elif a.text()=="自动遮挡":
            self.slot_auto()
        elif a.text()=="手动遮挡":
            self.slot_manual()
        elif a.text()=="上一步":
            print("shangyibu")
            if self.label_img.formerFlag==0 and self.label_img.motionFlag==1:
                self.label_img.formerFlag=1
                img_former=cv2.imread("img_tempout/former_cover.jpg")
                img=cv2.imread("img_tempout/cover.jpg")
                cv2.imwrite("img_tempout/cover.jpg",img_former)
                cv2.imwrite("img_tempout/cover_copy.jpg",img)
                jpg_tempout = QtGui.QPixmap("img_tempout/cover.jpg")
                self.label_img.setPixmap(jpg_tempout)
                self.label_message.setText("成功返回上一步！")
                self.label_message.setStyleSheet("color:green")
            else:
                self.label_message.setText("只能返回上一步！")
                self.label_message.setStyleSheet("color:red")
        elif a.text()=="下一步":
            print("xiayibu")
            if self.label_img.formerFlag==1:
                self.label_img.formerFlag=0
                img = cv2.imread("img_tempout/cover_copy.jpg")
                cv2.imwrite("img_tempout/cover.jpg", img)
                jpg_tempout = QtGui.QPixmap("img_tempout/cover.jpg")
                self.label_img.setPixmap(jpg_tempout)
                self.label_message.setText("成功向后一步！")
                self.label_message.setStyleSheet("color:green")
            else:
                self.label_message.setText("当前已是最后一步！")
                self.label_message.setStyleSheet("color:red")
        elif a.text()=="清除":
            self.slot_erase()
        elif a.text()=="重新加载":
            if self.label_img.openFlag==1:
                img=cv2.imread(self.label_img.path)
                cv2.imwrite("img_tempout/cover.jpg",img)
                cv2.imwrite("img_tempout/former_cover.jpg",img)
                self.label_img.motionFlag=0
                jpg = QtGui.QPixmap(self.label_img.path)
                self.label_img.setPixmap(jpg)
                self.label_message.setText("已重新加载！")
                self.label_message.setStyleSheet("color:green")
            else:
                self.label_message.setText("请先打开图片！")
                self.label_message.setStyleSheet("color:red")
        elif a.text()=="保存":
            self.slot_save()

    def slot_open(self):
        path, type = QFileDialog.getOpenFileName()
        if path != "":
            self.label_img.motionFlag=0
            self.label_img.openFlag=1
            self.label_img.path = path
            self.path_flag = True
            self.detect_flag = False
            self.label_path.setText(path)
            self.label_message.setText("照片导入成功！")
            self.label_message.setStyleSheet("color:green")
            img=cv2.imread(path)
            img_resize = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)
            cv2.imwrite("img_tempout/cover.jpg", img_resize)
            cv2.imwrite(path,img_resize)
            jpg = QtGui.QPixmap(path)
            self.label_img.setPixmap(jpg)
        else:
            self.label_message.setText("请选择照片！")
            self.label_message.setStyleSheet("color:red")

    def slot_detect(self):
        if self.path_flag:
            # if self.detect_flag==False:
            #     path = self.label_path.text()
            self.label_img.motionFlag=1
            formerImg=cv2.imread("img_tempout/cover.jpg")
            cv2.imwrite("img_tempout/former_cover.jpg",formerImg)
            self.label_img.rectangles = funcs_detect.detect("img_tempout/cover.jpg")
            self.label_message.setStyleSheet("color:green")
            self.label_message.setText("人脸检测成功！共检测到" + str(len(self.label_img.rectangles)) + "人脸！")
            jpg_tempout = QtGui.QPixmap("img_tempout/detect.jpg")
            self.label_img.setPixmap(jpg_tempout)
            self.detect_flag = True
            self.label_img.formerFlag=0
            # else:
            #     img=cv2.imread("img_tempout/cover.jpg")
            #     for rectangle in self.label_img.rectangles:
            #         cv2.rectangle(img, (int(rectangle[0]), int(rectangle[1])), (int(rectangle[2]), int(rectangle[3])),
            #                       (0, 255, 0), 2)
            #     cv2.imwrite("img_tempout/cover.jpg",img)
            #     jpg_tempout = QtGui.QPixmap("img_tempout/cover.jpg")
            #     self.label_img.setPixmap(jpg_tempout)
        else:
            self.label_message.setText("请先导入图片！")
            self.label_message.setStyleSheet("color:red")

    def slot_auto(self):
        if self.detect_flag:
            self.label_img.motionFlag = 1
            jpg = cv2.imread("img_tempout/cover.jpg")
            if self.coverType==0:
                funcs_detect.do_auto_mosaic(self.label_img.rectangles, jpg)
            elif self.coverType==1:
                cover_path="pictures/dog1.jpg"
                funcs_detect.do_auto_cover(self.label_img.rectangles, jpg,cover_path)
            elif self.coverType==2:
                cover_path="pictures/cartoon.jpg"
                funcs_detect.do_auto_cover(self.label_img.rectangles, jpg,cover_path)
            jpg_tempout_cover = QtGui.QPixmap("img_tempout/cover.jpg")
            self.label_img.setPixmap(jpg_tempout_cover)
            self.label_img.formerFlag = 0
            self.label_message.setText("成功进行自动脸部遮挡！")
            self.label_message.setStyleSheet("color:green")
        else:
            self.label_message.setText("请先进行人脸检测！")
            self.label_message.setStyleSheet("color:red")

    def slot_manual(self):
        if self.path_flag:
            self.label_img.motionFlag = 1
            jpg = cv2.imread("img_tempout/cover.jpg")
            w=abs(self.label_img.x1 - self.label_img.x0)
            h=abs(self.label_img.y1 - self.label_img.y0)
            if w*h!=0:
                if self.coverType == 0:
                    funcs_detect.do_manual_mosaic(jpg, self.label_img.x0, self.label_img.y0,
                                                  abs(self.label_img.x1 - self.label_img.x0),
                                                  abs(self.label_img.y1 - self.label_img.y0), 9)
                elif self.coverType == 1:
                    funcs_detect.do_manual_cover(self.label_img.x0, self.label_img.y0,
                                                 abs(self.label_img.x1 - self.label_img.x0),
                                                 abs(self.label_img.y1 - self.label_img.y0), jpg, "pictures/dog1.jpg")
                elif self.coverType == 2:
                    funcs_detect.do_manual_cover(self.label_img.x0, self.label_img.y0,
                                                 abs(self.label_img.x1 - self.label_img.x0),
                                                 abs(self.label_img.y1 - self.label_img.y0), jpg, "pictures/cartoon.jpg")
                cv2.imwrite("img_tempout/cover.jpg", jpg)
                jpg_tempout = QtGui.QPixmap("img_tempout/cover.jpg")
                self.label_img.setPixmap(jpg_tempout)
                self.label_img.formerFlag = 0
                self.label_message.setText("成功进行手动脸部遮挡！")
                self.label_message.setStyleSheet("color:green")
            else:
                self.label_message.setText("请绘制有效区域！")
                self.label_message.setStyleSheet("color:red")
        else:
            self.label_message.setText("请先导入图片！")
            self.label_message.setStyleSheet("color:red")

    def slot_erase(self):
        self.label_img.motionFlag = 1
        w = abs(self.label_img.x1 - self.label_img.x0)
        h = abs(self.label_img.y1 - self.label_img.y0)
        print(self.label_img.x0,self.label_img.y0,self.label_img.x1,self.label_img.y1)
        if w * h != 0:
            img=cv2.imread(self.label_img.path)
            img_cover=cv2.imread("img_tempout/cover.jpg")
            cv2.imwrite("img_tempout/former_cover.jpg", img_cover)
            x=self.label_img.x0
            y=self.label_img.y0
            for i in range(w):
                for j in range(h):
                    img_cover[y + j,x+i] = img[y+j,x+i]
            cv2.imwrite("img_tempout/cover.jpg", img_cover)
            jpg_tempout = QtGui.QPixmap("img_tempout/cover.jpg")
            self.label_img.setPixmap(jpg_tempout)
            self.label_img.formerFlag=0
            self.label_message.setText("擦除成功！")
            self.label_message.setStyleSheet("color:green")
        else:
            self.label_message.setText("请绘制有效区域！")
            self.label_message.setStyleSheet("color:red")

    def slot_save(self):
        if self.path_flag:
            path = self.label_path.text()
            jpg = cv2.imread("img_tempout/cover.jpg")
            jpg_name = path[55:-4]
            jpg_prefix = path[0:50]
            jpg_savepath = jpg_prefix + "imgs_out/" + jpg_name + "_out.jpg"
            cv2.imwrite(jpg_savepath, jpg)
            self.label_message.setText("保存成功！地址为："+jpg_savepath)
            self.label_message.setStyleSheet("color:green")
        else:
            self.label_message.setText("请先导入图片！")
            self.label_message.setStyleSheet("color:red")

    def selectionchange(self,i):
        self.coverType=i

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸马赛克系统"))
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/icon.jpg"))
        MainWindow.setWindowIcon(icon)
        self.label_path.setText(_translate("MainWindow", "欢迎使用人脸马赛克系统!"))
        self.label_message.setText(_translate("MainWindow", "请先打开照片！"))
        self.label_message.setStyleSheet("color:green")
        # self.pushButton_detect.setText(_translate("MainWindow", "检测人脸"))
        # self.pushButton_open.setText(_translate("MainWindow", "导入照片"))
        self.label_coverType.setText(_translate("MainWindow", "  遮挡方式："))
        self.comboBox.setItemText(0, _translate("MainWindow", "马赛克"))
        self.comboBox.setItemText(1, _translate("MainWindow", "狗头贴纸"))
        self.comboBox.setItemText(2, _translate("MainWindow", "动漫人脸"))
        # self.pushButton_auto.setText(_translate("MainWindow", "自动遮挡"))
        # self.pushButton_manual.setText(_translate("MainWindow", "手动遮挡"))
        # self.pushButton_erase.setText(_translate("MainWindow", "手动擦除"))
        # self.pushButton_save.setText(_translate("MainWindow", "保存照片"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_set.setTitle(_translate("MainWindow", "设置"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_import.setText(_translate("MainWindow", "导入"))
        self.action_save.setText(_translate("MainWindow", "保存"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
