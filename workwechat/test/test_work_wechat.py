#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import win32gui

import pywinauto
# import pytesseract
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot

def get_target_handlers(title='企业微信'):
    handlers = []
    time.sleep(0.1)
    win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
    time.sleep(0.1)
    target_handlers = []
    for handler in handlers:
        if win32gui.GetWindowText(handler) == title:
            target_handlers.append(handler)
    print('\n\t\t标题为 %s 的所有窗体 - %s' % (title, target_handlers))
    return target_handlers

q_wx_handler = get_target_handlers()[0]
print("Windows:///%s" % q_wx_handler)

windowtitle = '企业微信'
win_dlg = pywinauto.Desktop()[windowtitle]
win_dlg.set_focus()
# win_dlg.maximize()
# win_dlg.restore()

# set_up到windows
auto_setup(__file__, devices=["Windows:///%s" % q_wx_handler])
# 截图
screen = snapshot(filename='E:\\Git\\daqinjia\WorkWechat\\test.png',quality=99,max_size=1200)
# 转化为CV可读取格式
image = aircv.imread(filename='E:\\Git\\daqinjia\WorkWechat\\test.png')
# 切图
local = aircv.crop_image(image,(132,58,380,126))
# 显示(test)
aircv.show_origin_size(img=local)
# 尝试点击
if not exists(Template(r'E:\\Git\\daqinjia\WorkWechat\\消息.png')):
    print('already in 消息')
else:
    touch(Template(r'E:\\Git\\daqinjia\WorkWechat\\消息.png'))



print("-----------图片识别文字信息为--------------")
'''
百度OCR方法，暂时弃用（高效精准但是有每日调用api次数限制）
'''
# OCR_obj = CodeDemo(img_path="E:\\Git\\daqinjia\WorkWechat\\test.png")
# result_code = OCR_obj.getCode()
# words_result=result_code.get("words_result")
# words_list = [words.get('words') for words in words_result]
# words_str = str(words_list)
# print(words_str)

'''
tesseract-OCR方法
'''
text = pytesseract.image_to_string(image=local,lang='chi_sim')
print(text)

# # w_wx_window.restore()
# # app = Application().start('企业微信.exe')
# # app = Application()            
# # window = app.window_(handle = q_wx_handler)

# print(q_wx_handler)
# win32gui.SetForegroundWindow(q_wx_handler)
# win32gui.SetFocus(q_wx_handler)


