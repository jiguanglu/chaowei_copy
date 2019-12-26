# 导入模块
import pytesseract
# 导入图片库 【注意】需要安装库: pip install Pillow
# 导入库
from PIL import Image
import cv2 as cv
import numpy as np




def threshold_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    print("threshold value %s"%ret)
    cv.namedWindow("binary0", cv.WINDOW_NORMAL)
    cv.imshow("binary0", binary)

def local_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    gray = cv.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    #自适应阈值化能够根据图像不同区域亮度分布，改变阈值
    # binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)
    # binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV, 25, 10)
    # cv.namedWindow("binary1", cv.WINDOW_NORMAL)
    # cv.imshow("binary1", binary)
    cv.imwrite('../data/test02.jpg',gray)


def custom_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    h, w =gray.shape[:2]
    m = np.reshape(gray, [1,w*h])
    mean = m.sum()/(w*h)
    print("mean:",mean)
    # ret, binary =  cv.threshold(gray, mean, 255, cv.THRESH_BINARY_INV)
    retval, gray_img = cv.threshold(gray, 0, 255, cv.THRESH_OTSU);
    # cv.namedWindow("binary2", cv.WINDOW_NORMAL)
    # cv.imshow("binary2", binary)
    cv.imwrite('../data/test02.jpg',gray_img)

src = cv.imread('../data/test.png')
# local_threshold(image)

# cv.namedWindow('input_image', cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
# cv.imshow('input_image', src)
# threshold_demo(src)
# local_threshold(src)
custom_threshold(src)
# cv.waitKey(0)lang=None, config='', nice=0)
# cv.destroyAllWindows()

# 创建图片对象
image = Image.open(r"../data/test02.jpg")
# 识别图片
print(pytesseract.image_to_string(image, config='-l eng --oem 3 --psm 12'))
# print(pytesseract.image_to_string(image, lang=None, config='', nice=0))
