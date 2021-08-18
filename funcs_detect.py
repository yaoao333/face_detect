import cv2
import numpy as np

from mtcnn import mtcnn


#马赛克处理
def do_auto_mosaic(rectangles,img, neighbor=9):
    """
    :param rgb_img
    :param int x :  马赛克左顶点
    :param int y:  马赛克左顶点
    :param int w:  马赛克宽
    :param int h:  马赛克高
    :param int neighbor:  马赛克每一块的宽
    """
    cv2.imwrite("img_tempout/former_cover.jpg", img)
    for rectangle in rectangles:
        x = int(rectangle[0])
        y = int(rectangle[1])
        w = int(rectangle[2]) - int(rectangle[0])
        h = int(rectangle[3]) - int(rectangle[1])
        for i in range(0, h, neighbor):
            for j in range(0, w, neighbor):
                rect = [j + x, i + y]
                color = img[i + y][j + x].tolist()  # 关键点1 tolist
                left_up = (rect[0], rect[1])
                x2 = rect[0] + neighbor - 1  # 关键点2 减去一个像素
                y2 = rect[1] + neighbor - 1
                if x2 > x + w:
                    x2 = x + w
                if y2 > y + h:
                    y2 = y + h
                right_down = (x2, y2)
                cv2.rectangle(img, left_up, right_down, color, -1)  # 替换为为一个颜值值
    cv2.imwrite("img_tempout/cover.jpg",img)

def do_manual_mosaic(img,x,y,w,h,neighbor=9):
    cv2.imwrite("img_tempout/former_cover.jpg", img)
    for i in range(0, h, neighbor):
        for j in range(0, w, neighbor):
            rect = [j + x, i + y]
            color = img[i + y][j + x].tolist()  # 关键点1 tolist
            left_up = (rect[0], rect[1])
            x2 = rect[0] + neighbor - 1  # 关键点2 减去一个像素
            y2 = rect[1] + neighbor - 1
            if x2 > x + w:
                x2 = x + w
            if y2 > y + h:
                y2 = y + h
            right_down = (x2, y2)
            cv2.rectangle(img, left_up, right_down, color, -1)  # 替换为为一个颜值值
    cv2.imwrite("img_tempout/cover.jpg", img)

def do_auto_cover(rectangles,img,coverImg_path):
    coverImg = cv2.imread(coverImg_path)
    cv2.imwrite("img_tempout/former_cover.jpg", img)
    coverImg_gray = cv2.cvtColor(coverImg, cv2.COLOR_BGR2GRAY)
    _, coverImg_bAw = cv2.threshold(coverImg_gray, 230, 255, cv2.THRESH_BINARY)
    for rectangle in rectangles:
        x = int(rectangle[0])
        y = int(rectangle[1])
        w = int(rectangle[2]) - int(rectangle[0])
        h = int(rectangle[3]) - int(rectangle[1])
        coverImg_resize=cv2.resize(coverImg,(w,h),interpolation=cv2.INTER_AREA)
        coverImg_bAw_resize=cv2.resize(coverImg_bAw,(w,h),interpolation=cv2.INTER_AREA)
        u,v,_=coverImg_resize.shape
        for i in range(u):
            for j in range(v):
                if coverImg_bAw_resize[i, j] == 0:
                    img[y+i, x+j] = coverImg_resize[i, j]
    cv2.imwrite("img_tempout/cover.jpg", img)

def do_manual_cover(x,y,w,h,img,coverImg_path):
    coverImg = cv2.imread(coverImg_path)
    cv2.imwrite("img_tempout/former_cover.jpg", img)
    coverImg_gray = cv2.cvtColor(coverImg, cv2.COLOR_BGR2GRAY)
    _, coverImg_bAw = cv2.threshold(coverImg_gray, 230, 255, cv2.THRESH_BINARY)
    coverImg_resize = cv2.resize(coverImg, (w, h), interpolation=cv2.INTER_AREA)
    coverImg_bAw_resize = cv2.resize(coverImg_bAw, (w, h), interpolation=cv2.INTER_AREA)
    u, v, _ = coverImg_resize.shape
    for i in range(u):
        for j in range(v):
            if coverImg_bAw_resize[i, j] == 0:
                img[y + i, x + j] = coverImg_resize[i, j]
    cv2.imwrite("img_tempout/cover.jpg", img)



#根据path获取图片，检测人脸并加马赛克
def detect(path):

    model = mtcnn()

    # -------------------------------------#
    #   设置检测门限
    # -------------------------------------#
    threshold = [0.5, 0.6, 0.7]
    # -------------------------------------#
    #   读取图片,注意cv2.imread默认以BGR色调读取图片，需手动转换成RGB色调
    # -------------------------------------#
    img = cv2.imread(path)
    temp_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imshow("111",temp_img)
    # -------------------------------------#
    #   将图片传入并检测
    # -------------------------------------#
    rectangles = model.detectFace(temp_img, threshold)

    draw = img.copy()
    for rectangle in rectangles:
        cv2.rectangle(draw, (int(rectangle[0]), int(rectangle[1])), (int(rectangle[2]), int(rectangle[3])), (0, 255, 0),2)
        # do_mosaic(draw1, int(rectangle[0]), int(rectangle[1]), W, H, 9)


        # for i in range(5, 15, 2):
        #     cv2.circle(draw, (int(rectangle[i + 0]), int(rectangle[i + 1])), 1, (255, 0, 0), 4)
    cv2.imwrite("img_tempout/detect.jpg", draw)
    # cv2.imwrite("img_tempout/mosaic.jpg", draw1)
    return rectangles