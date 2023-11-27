# -*- encoding=utf8 -*-
from airtest.cli.parser import cli_setup
import time
import win32gui
import pywinauto
from airtest.core.api import auto_setup


class AirConn():
    '''
    find the workwechat app and let airtest connect to the windows.
    '''
    def __init__(self,title):
        self.target_handler = None
        self.title = title

    def get_target_handler(self): 
        handlers = []
        time.sleep(0.1)
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            if win32gui.GetWindowText(handler) == self.title:
                self.target_handler = handler
                break

    def connect_to_target_window(self):
        win_dlg = pywinauto.Desktop()[self.title]
        win_dlg.set_focus()
        self.get_target_handler()
        print('*********connect to the window:',self.title,'***********')
        if not cli_setup():
            auto_setup(__file__,devices=["Windows:///%s" % self.target_handler])
