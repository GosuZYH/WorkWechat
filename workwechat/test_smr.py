from airtest.core.api import *  # Template, touch, auto_setup, connect_device
from airtest.aircv import *
from airtest.aircv import cv2
import numpy as np
import os
import time
import win32clipboard
import logging
import pytesseract
from base import Base
from everyday_task import EveryDayTask

logger = logging.getLogger(__name__)


def find_contours(img_screen):
	height, width, channels = img_screen.shape
	img_binary = np.zeros((height, width), dtype='uint8')
	
	for i in range(height):
		for j in range(width):
			if (img_screen[i, j][0] == 237 and
					img_screen[i, j][1] == 237 and
					img_screen[i, j][2] == 237):
				img_binary[i, j] = 255
	
	contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	logger.info('\n\tNumber of contours: %s' % len(contours))
	print('\n\tNumber of contours: %s' % len(contours))
	# cv2.imshow('001', img_binary)
	#     cv2.waitKey(0)
	return contours


# every_day_task = Base()
every_day_task = EveryDayTask()

# "SOP消息"界面
every_day_task.connect_to_special_panel('SOP消息')
touch(Template(r"photos\tpl1636618032406.png", record_pos=(-0.01, 0.003), resolution=(600, 720)))
#   # 获取复制内容（并做处理）
win32clipboard.OpenClipboard()
label_target = win32clipboard.GetClipboardData()
label_target = label_target.replace('_', ' ')
win32clipboard.CloseClipboard()
#   # “转跳到群发助手”
touch(Template(r"photos\tpl1636619069985.png", record_pos=(-0.003, 0.51), resolution=(600, 720)))


print('\t -111')


# “向我的客户发消息”
every_day_task.connect_to_special_panel('向我的客户发消息')
touch(Template(r"photos\tpl1636619146759.png", record_pos=(-0.234, -0.229), resolution=(500, 415)))

print('\t 222')

# "选择客户" 界面
every_day_task.connect_to_special_panel('选择客户')

print('\t 333')

#   # 保证为未点击状态（操作比较复杂）
# if not exists(Template(r"tpl1636535273023.png", record_pos=(-0.423, -0.216), resolution=(620, 500))):
#     print('\t111')
#     every_day_task.select_customer_tag()

img_select_custom_panel_name = 'screen_select_custom_panel.png'
screen_img_path = os.path.join(os.getcwd(), 'photos', img_select_custom_panel_name)
snapshot(filename=screen_img_path, msg=img_select_custom_panel_name)
img_select_custom_panel = cv2.imread(screen_img_path)
h_select_custom_panel, w_select_custom_panel = img_select_custom_panel.shape[:2]
print('\t\t', h_select_custom_panel, w_select_custom_panel)
template_select_custom_panel = Template(r"%s" % screen_img_path)

# 桌面截屏
every_day_task.connect_to_desktop()

screen_desk = G.DEVICE.snapshot()
x_m, y_m = template_select_custom_panel.match_in(screen_desk)

# 截屏范围
x_s = x_m - w_select_custom_panel / 2
y_s = y_m - h_select_custom_panel / 2
x_t = x_m + w_select_custom_panel / 2
y_t = y_m + h_select_custom_panel / 2

# 再次进入"选择客户"界面，并点击
every_day_task.connect_to_special_panel('选择客户')
every_day_task.select_customer_tag()
time.sleep(1)
# 再次桌面截屏，并选取变化之后的"选择客户"界面
every_day_task.connect_to_desktop()
screen_desk = G.DEVICE.snapshot()
time.sleep(0.5)
local_screen = aircv.crop_image(screen_desk, (x_s, y_s, x_t, y_t))
# cv2.imshow('000', local_screen)
# # cv2.waitKey(0)
local_contours = find_contours(local_screen)
list_rst_cnt = []
kernel = np.ones((2, 2), np.uint8)

for cnt in local_contours:
	if cv2.contourArea(cnt) > 100:
		x, y, w, h = cv2.boundingRect(cnt)
		img_ocr = aircv.crop_image(local_screen, (x, y, x + w, y + h))
		img_ocr = cv2.cvtColor(img_ocr, cv2.COLOR_BGR2GRAY)
		img_ocr = cv2.resize(img_ocr, (0, 0), fx=2.9, fy=2.9, interpolation=cv2.INTER_CUBIC)
		ocr_text = pytesseract.image_to_string(
			img_ocr, lang='chi_sim', config="-c page_separator=''")
		touch_x = x_s + x + w / 2
		touch_y = y_s + y + h / 2
		list_rst_cnt.append([ocr_text.strip(), [touch_x, touch_y]])
	# cv2.imshow('zzz', img_ocr)
	# print('ocr_text = ', ocr_text)
	# cv2.waitKey(0)

touch_pos = []
for rst_cnt in list_rst_cnt:
	print(rst_cnt)
	if rst_cnt[0] == label_target:
		touch_pos = rst_cnt[1]

print('\ttouch_pos = ', touch_pos)
# cv2.waitKey(0)

# TODO 翻屏操作
