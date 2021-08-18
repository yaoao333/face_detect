import sys

import cv2

from PyQt5.QtWidgets import QApplication, QMainWindow

import gui2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setFixedSize(1300, 940)

    ui = gui2.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # img0=cv2.imread("imgs/panyuchen.jpg")
    # img=cv2.imread("imgs/dog1.jpg")
    # img1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # _, img2= cv2.threshold(img1, 230, 255, cv2.THRESH_BINARY)
    # # cv2.imshow("hhh",img2)
    # u,v,_=img.shape
    # for i in range(u):
    #     for j in range(v):
    #         if img2[i, j] == 0:
    #             img0[i, j] = img[i, j]
    # img3=cv2.resize(img0,(500,500),interpolation=cv2.INTER_AREA)
    # cv2.imshow("hhh",img3)
    # cv2.waitKey(0)

    # img0 = cv2.imread("imgs/panyuchen.jpg")
    # print("1111111111")
    # dogtag = cv2.imread("imgs/dog1.jpg")
    # dogtag_gray = cv2.cvtColor(dogtag, cv2.COLOR_BGR2GRAY)
    # _, dogtag_bAw = cv2.threshold(dogtag_gray, 230, 255, cv2.THRESH_BINARY)
    # dogtag_resize = cv2.resize(dogtag, (200, 100), interpolation=cv2.INTER_AREA)
    # dogtag_bAw_resize = cv2.resize(dogtag_bAw, (200, 100), interpolation=cv2.INTER_AREA)
    # print("2222222222222")
    # u, v, _ = dogtag_resize.shape
    # for i in range(u):
    #     for j in range(v):
    #         if dogtag_bAw_resize[i, j] == 0:
    #            img0[300 + i, 700 + j] = dogtag_resize[i, j]
    # cv2.imshow("hhh",img0)
    # cv2.waitKey(0)