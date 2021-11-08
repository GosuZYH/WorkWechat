# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from baidu_OCR import CodeDemo
from init_airtest import AirConn
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot


class EveryDayTask():
    def __init__(self):
        conn = AirConn()
        conn.connect_to_workwechat()

    def find_the_chat(self):
        '''
        turn to the chat panel.
        '''
        if not exists(Template(r'photos\\消息.png')):
            print('already in 消息')
        else:
            touch(Template(r'photos\\消息.png'))

    def search_the_SMR(self):
        '''
        search the luoshu SMR in chat-list.
        '''
        touch(Template(r'photos\\搜索框.png'))


task = EveryDayTask()
task.search_the_SMR()
