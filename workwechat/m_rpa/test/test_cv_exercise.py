import cv2
import numpy as np
import os
import site

ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
UI_PATH = os.path.join(DATA_PATH, "ui")

# img_path = r'C:\Users\Administrator\AppData\Roaming\SMR\ui\gray_screen_not_sent.jpg'  # gray_screen_not_sent   screen
# cv2.imshow('0', img_screen)
# print(h_screen,w_screen)
# cv2.imwrite(r'C:\Users\Tian\AppData\Roaming\SMR\ui\test1.png', img_screen)

# def screenshot_to_file(self):
#     adb_path = site.getsitepackages()[1] + r'\airtest\core\android\static\adb\windows\adb.exe'
#     self.dev.shell("/system/bin/screencap -p /sdcard/screenshot.png")
#     os.system(f'{adb_path} pull /sdcard/screenshot.png {UI_PATH}\\SCREENSHOT.png')

def get_context_contour_w_h_ratio(contour):
    ratio_w_h = 0.0
    pos_x = 0.0
    pos_y = 0.0
    img_path = UI_PATH + '\\SCREENSHOT.png'     # C:\Users\User\AppData\Roaming\SMR\ui\SCREENSHOT.png is necessary.
    print(img_path)
    img_screen = cv2.imread(img_path, 0)
    h_screen, w_screen = img_screen.shape
    y_ojb_b, y_ojb_e, x_ojb_b, x_ojb_e = int(contour[0]*h_screen),int(contour[1]*h_screen),int(contour[2]*w_screen),int(contour[3]*w_screen)
    h_ojb = y_ojb_e - y_ojb_b
    w_ojb = x_ojb_e - x_ojb_b
    img_ojb = img_screen[y_ojb_b: y_ojb_e, x_ojb_b: x_ojb_e]
    img_ojb_color = cv2.cvtColor(img_ojb, cv2.COLOR_GRAY2BGR)
    img_ojb_new = np.zeros(img_ojb.shape)
    # cv2.imshow('ojb', img_ojb)
    # cv2.imwrite(r'C:\Users\Administrator\AppData\Roaming\SMR\ui\gray_ojb_not_sent.jpg', img_ojb)

    img_ojb_inverse = 255 - img_ojb.copy()
    # cv2.imshow('img_ojb_inverse 0', img_ojb_inverse)
    ret, img_ojb_inverse = cv2.threshold(img_ojb_inverse, 70, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_ojb_inverse.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if contours:
        c = contours[0]
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img_ojb_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

        img_contour = cv2.drawContours(img_ojb_color.copy(), c, -1, (0, 0, 255), 2)
        # cv2.imshow('img_contour', img_contour)
        for i in range(h_ojb):
            for j in range(w_ojb):
                if cv2.pointPolygonTest(c, (j, i), False) >= 0:
                    if img_ojb_inverse[i, j] != 255:
                        img_ojb_new[i, j] = 255

        img_ojb_new = cv2.morphologyEx(img_ojb_new, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        dilation_ojb = cv2.dilate(img_ojb_new, np.ones((7, 7), np.uint8), iterations=2)

        dilation_ojb = dilation_ojb.astype(np.uint8)
        # cv2.imshow('dilation_ojb', dilation_ojb)
        dilation_contours, _ = cv2.findContours(dilation_ojb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if dilation_contours:
            (x_, y_, w_contour_ojb, h_contour_ojb) = cv2.boundingRect(dilation_contours[0])
            cv2.rectangle(img_ojb_color, (x_, y_), (x_ + w_contour_ojb, y_ + h_contour_ojb), (255, 0, 0), 2)
            pos_x = x_ojb_b + x + w_contour_ojb/2
            pos_y = y_ojb_b + y + h_contour_ojb/2
            ratio_w_h = float(w_contour_ojb) / float(h_contour_ojb)
        else:
            pass
    else:
        pass
    cv2.imshow('img_ojb_inverse', img_ojb_inverse)
    cv2.imshow('img_ojb_color', img_ojb_color)
    cv2.imshow('img_ojb_new', img_ojb_new)
    return ratio_w_h, pos_x, pos_y

# # 分享
#   pos :  [0.5, 0.9625]
ratio_w_h_share = get_context_contour_w_h_ratio((0.94, 0.98, 0.3, 0.7))
print('ratio_w_h_share = ', ratio_w_h_share)    # threshold 参考值 5.4

# # 回执
#   pos :  [0.8666666666666667, 0.844375]
# ratio_w_h_reply = get_context_contour_w_h_ratio((0.79, 0.9, 0.75, 0.98))
# print('ratio_w_h_reply = ', ratio_w_h_reply)    # threshold 参考值：回执1.67，已回执2.40

cv2.waitKey(0)
