# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from baidu_OCR import CodeDemo
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot


class AirConn():
    '''
    find the workwechat app and let airtest connect to the windows.
    '''
    def __init__(self):
        self.target_handlers = None

    def get_target_handlers(self,title='企业微信'): 
        handlers = []
        time.sleep(0.1)
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            if win32gui.GetWindowText(handler) == title:
                self.target_handlers = handler
                break

    def connect_to_workwechat(self):
        windowtitle = '企业微信'
        win_dlg = pywinauto.Desktop()[windowtitle]
        win_dlg.set_focus()
        self.get_target_handlers()
        if not cli_setup():
            auto_setup(__file__,logdir=True,devices=["Windows:///%s" % self.target_handlers])

# conn = AirConn()
# conn.connect_to_workwechat()
# if not exists(Template(r'photos\\消息.png')):
#     print('already in 消息')
# else:
#     touch(Template(r'photos\\消息.png'))
