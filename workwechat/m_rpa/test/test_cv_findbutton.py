
import cv2
import numpy as np
import os

ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
UI_PATH = os.path.join(DATA_PATH, "ui")
img_path = UI_PATH + '\\SCREENSHOT.png'     # C:\Users\User\AppData\Roaming\SMR\ui\SCREENSHOT.png is necessary.

img_screen = cv2.imread(img_path)
cv2.namedWindow('3.原图',cv2.WINDOW_NORMAL) 
cv2.imshow('3.原图', img_screen)
gray = cv2.cvtColor(img_screen,cv2.COLOR_BGR2GRAY)
gray_inverse_img = 255 - gray    # 灰度值反转
cv2.imshow('4.灰度值反转', gray_inverse_img)
ret, img_ojb_inverse = cv2.threshold(gray_inverse_img.copy(), 70, 255, cv2.THRESH_BINARY)
cv2.imshow('5.二值化处理', img_ojb_inverse)

#输出图像大小，方便根据图像大小调节minRadius和maxRadius
print(img_screen.shape)
circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=300)
print(circles)
print(len(circles[0]))

for circle in circles[0]:
    print(circle[2])
    x=int(circle[0])
    y=int(circle[1])
    r=int(circle[2])
    img=cv2.circle(img_screen,(x,y),r,(0,0,255),-1)
cv2.imshow('res',img)
cv2.waitKey(0)

# circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,600,param1=100,param2=30)
# circles = circles1[0,:,:]
# circles = np.uint16(np.around(circles))
# for i in circles[:]: 
#     cv2.circle(img_screen,(i[0],i[1]),i[2],(255,0,0),5)
#     # cv2.circle(img_screen,(i[0],i[1]),2,(255,0,255),10)
#     # cv2.rectangle(img_screen,(i[0]-i[2],i[1]+i[2]),(i[0]+i[2],i[1]-i[2]),(255,255,0),5)

# cv2.imshow('circle',img_screen)
# cv2.waitKey(0)
