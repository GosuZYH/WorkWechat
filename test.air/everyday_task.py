# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import time
import win32gui
import pywinauto
import pytesseract
import logging
from PIL import Image
from baidu_OCR import CodeDemo
from init_airtest import AirConn
from photos import Base,exists_ui,touch_ui
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot


logger = logging.getLogger(__name__)
class EveryDayTask(Base):
    def __init__(self):
        conn = AirConn()
        conn.connect_to_workwechat()
        self.end_flag = False

    def find_the_chat(self):
        '''
        turn to the chat panel.
        '''
        if exists_ui('消息1'):
            return
        else:
            touch_ui('消息2')

    def search_the_SMR(self):
        '''
        search the luoshu SMR in chat-list.
        '''
        if exists_ui('清空'):
            touch_ui('清空')
        sleep(0.2)
        if exists_ui('搜索框'):
            touch_ui('搜索框')

        self.send_keys('洛书SMR')
        touch_ui('洛书SMR1')
        # if exists_ui('应用与小程序'):
        #     if exists_ui('洛书SMR1'):
        #         touch_ui('洛书SMR1')
        #     elif exists_ui('洛书SMR2'):
        #         touch_ui('洛书SMR2')
        #     else:
        #         logger.error('can not find the LuoShu-SMR mini-program')
        # else:
        #     logger.error('can not find app and mini-program')

    def back_to_latest_position(self):
        '''
        turn to the latest position
        '''
        if exists_ui('回到最新位置'):
            touch_ui('回到最新位置')

    def receipt_the_custom_sop(self):
        '''
        receipt the 1v1 custom sop everyday.
        '''
        pass
    
    def test(self):
        '''
        test
        '''

    def run_task(self):
        '''
        '''
        self.find_the_chat()
        # self.search_the_SMR()
        # self.back_to_latest_position()
        # self.receipt_the_custom_sop()
        self.test()

        


task = EveryDayTask()
task.run_task()
