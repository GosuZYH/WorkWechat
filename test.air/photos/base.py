# -*- encoding=utf8 -*-
__author__ = "26579"

from abc import ABC
import logging
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup

from init_airtest import AirConn



logger = logging.getLogger(__name__)


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

    def connect_to_workwechat(self):
        '''
        connect to the workwechat main window.
        '''
        conn = AirConn(title='企业微信')
        try:
            conn.connect_to_target_window()
        except Exception as e:
            logger.error(f'—— can not connect to the workwechat,detil error info: ——\n\t {e}')
        sleep(0.2)

    def connect_to_sop_chat(self):
        '''
        connect to the sop chat panel.
        '''
        conn = AirConn(title='SOP消息')
        try:
            conn.connect_to_target_window()
        except Exception as e:
            logger.error(f'—— can not connect to the sop-chat panel,detil error info: ——\n\t {e}')
        sleep(0.2)

    def connect_to_sending_helper(self):
        '''
        connect to the sending-msg-to-my-customer panel.
        '''
        conn = AirConn(title='向我的客户发消息')
        try:
            conn.connect_to_target_window()
        except Exception as e:
            logger.error(f'—— can not connect to the sending-panel,detil error info: ——\n\t {e}')
        sleep(0.2)

    def connect_to_select_custom_panel(self):
        '''
        connect to the workwechat main window.
        '''
        conn = AirConn(title='选择客户')
        try:
            conn.connect_to_target_window()
        except Exception as e:
            logger.error(f'—— can not connect to the workwechat,detil error info: ——\n\t {e}')
        sleep(0.2)

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
    return exists(Template('photos\%s.png' %photo_name))

def find_all_ui(photo_name=''):
    '''
    judge if the ui find_all.
    :return 所有的匹配到的元素坐标-->list[(x1, y1),(x2, y2)...(xn, yn)]
    '''
    list = []
    result = find_all(Template('photos\%s.png' %photo_name))
    for i in result:
        list.append(i.get('result'))
    return list
