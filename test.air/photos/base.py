# -*- encoding=utf8 -*-
__author__ = "zyh"

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

    def connect_to_desktop(self):
        '''
        connect to the windows desktop
        '''
        if not cli_setup():
            auto_setup(__file__,logdir=True,devices=["Windows:///",])

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
    
    def connect_to_msg_sending_confirm(self):
        '''
        connect to the message-sending-confirm panel.
        '''
        conn = AirConn(title='消息发送确认')
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

def touch_ui(photo_name='',**kwargs):
    '''
    touch the ui in photo.
    * if have kwargs: will touch the central point coordinate offset.
    '''
    if kwargs:
        pos = find_all(Template('photos\%s.png' %photo_name))
        if pos is not None:
            offset_x = 0 if kwargs.get('x') is None else kwargs.get('x')
            offset_y = 0 if kwargs.get('y') is None else kwargs.get('y')
            pos_x = int(pos[0].get('result')[0]) + offset_x
            pos_y = int(pos[0].get('result')[1]) + offset_y
            print(pos_x,pos_y)
            touch((pos_x,pos_y))
    else:
        touch(Template('photos\%s.png' %photo_name))

def exists_ui(photo_name=''):
    '''
    judge if the ui exists.
    '''
    return exists(Template('photos\%s.png' %photo_name))

def find_ui(photo_name=''):
    '''
    find all exists ui in panel.
    '''
    return find_all(Template('photos\%s.png' %photo_name))