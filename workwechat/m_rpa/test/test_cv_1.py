import cv2
import numpy as np
import os
import site
import pytesseract
from datetime import datetime

ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
UI_PATH = os.path.join(DATA_PATH, "ui")


def get_context_contour_w_h_ratio(contour):
    ratio_w_h = 0.0
    pos_x = 0.0
    pos_y = 0.0
    img_path = UI_PATH + '\\SCREENSHOT.png'     # C:\Users\User\AppData\Roaming\SMR\ui\SCREENSHOT.png is necessary.
    img_screen = cv2.imread(img_path, 0)
    cv2.imshow('1.cv读图', img_screen)

    h_screen, w_screen = img_screen.shape
    y_ojb_b, y_ojb_e, x_ojb_b, x_ojb_e = int(contour[0]*h_screen),int(contour[1]*h_screen),int(contour[2]*w_screen),int(contour[3]*w_screen)

    cut_img = img_screen[y_ojb_b: y_ojb_e, x_ojb_b: x_ojb_e]
    new_cut_img = np.zeros(cut_img.shape)
    cv2.imshow('2.切图', cut_img)

    gray_img = cv2.cvtColor(cut_img, cv2.COLOR_GRAY2BGR)
    cv2.imshow('3.色彩转换', gray_img)

    gray_inverse_img = 255 - cut_img    # 灰度值反转
    cv2.imshow('4.灰度值反转', gray_inverse_img)

    s_time = datetime.now()
    text = pytesseract.image_to_string(gray_img,lang='chi_sim')
    e_time = datetime.now()
    print(f'文字识别结果:{text},用时:{(e_time-s_time).total_seconds()}s')
    
    ret, img_ojb_inverse = cv2.threshold(gray_inverse_img.copy(), 70, 255, cv2.THRESH_BINARY)
    cv2.imshow('5.二值化处理', img_ojb_inverse)

    gray_inverse_img_2 = 255 - img_ojb_inverse.copy()    # 二次灰度值反转
    cv2.imshow('6.二次灰度值反转', gray_inverse_img_2)

    c, _ = cv2.findContours(gray_inverse_img_2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if c:
        x, y, w, h = cv2.boundingRect(c[0])

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))   # 元素膨胀
    dilate_img = cv2.dilate(gray_inverse_img_2.copy(), kernel, iterations=2)
    dilate_img = dilate_img.astype(np.uint8)
    cv2.imshow('7.dilate_img', dilate_img)

    dilation_contours, _ = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if dilation_contours:
        x_, y_, w_contour_ojb, h_contour_ojb = cv2.boundingRect(dilation_contours[0])
        cv2.drawContours(gray_img, dilation_contours, -1, (0, 0, 255), 2)
        cv2.imshow('8.框出轮廓', gray_img)
        pos_x = x_ojb_b + x + w_contour_ojb/2
        pos_y = y_ojb_b + y + h_contour_ojb/2
        ratio_w_h = float(w_contour_ojb) / float(h_contour_ojb)
        for i in range(len(dilation_contours)):
            theRect = cv2.minAreaRect(dilation_contours[i])
            cv2.circle(gray_img, (int(theRect[0][0]),int(theRect[0][1])), 1, (0, 255, 0), 4)
            cv2.imshow('9.中心点', gray_img)
    else:
        pass
    return ratio_w_h, pos_x, pos_y

# # # 分享
# #   pos :  [0.5, 0.9625]
ratio_w_h_share = get_context_contour_w_h_ratio((0.94, 0.98, 0.3, 0.7))
print('ratio_w_h_share = ', ratio_w_h_share)    # threshold 参考值 5.32

# # # 回执
# #   pos :  [0.8666666666666667, 0.844375]
# ratio_w_h_reply = get_context_contour_w_h_ratio((0.79, 0.9, 0.75, 0.98))
# print('ratio_w_h_reply = ', ratio_w_h_reply)    # threshold 参考值：回执1.67，已回执2.40

cv2.waitKey(0)
