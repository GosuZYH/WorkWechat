# -*- encoding=utf8 -*-
__author__ = "26579"

from abc import ABC
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup

# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=["Windows:///67706",])

class Base(ABC):
    '''
    base operation in workwechat.
    '''
    def __init__(self) -> None:
        pass

    # example
    def click_search_frame(self):
        '''
        search the luoshu SMR in chat-list.
        '''
        touch(Template(r'photos\\搜索框.png'))

    def send_keys(self, keys):
        """
        输入keys中的内容，如果是'\n'则意为回车发送
        """
        if keys in ('\n',):
            pywinauto.keyboard.SendKeys('\n', with_newlines=True)
            return
        parsed_keys = self.parse_key(keys)
        pywinauto.keyboard.SendKeys(parsed_keys, with_spaces=True)
        return False if parsed_keys == keys else True

    def parse_key(self,keys=None, parse_to=" ") -> str:
        """
        字符转换，将字符串中特殊字符转化为空格
        """
        str = []
        index = 0
        while index < len(keys):
            c = keys[index]
            index += 1
            if c in ('(', ')', '{', '}', '[', ']', '~', '+', '^', '%'):
                c = ' '
                str.append(c)
            elif ord(c) > 65535:
                c = parse_to
                str.append(c)
            else:
                str.append(c)

        return ''.join(str)


def touch_ui(photo_name=''):
    '''
    touch the ui in photo.
    '''
    touch(Template('photos\%s.png' %photo_name))

def exists_ui(photo_name=''):
    '''
    judge if the ui exists.
    '''
    exists(Template('photos\%s.png' %photo_name))
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
