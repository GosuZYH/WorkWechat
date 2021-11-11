# -*- encoding=utf8 -*-
__author__ = "zyh"

from abc import ABC
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from setup_log import Logger

from init_airtest import AirConn


class Base(ABC):
    '''
    base operation in workwechat.
    '''
    def __init__(self):
        log = Logger(level='debug')
        self.log = log.logger

    # example
    def click_search_frame(self):
        '''
        search the luoshu SMR in chat-list.
        '''
        touch(Template(r'photos\\搜索框.png'))

    def check_window_exists(self,title=''):
        '''
        check all exists windows the
        '''
        handlers = []
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            if win32gui.GetWindowText(handler) == title:
                return True
        self.log.error(f'\n\t ***{title} window not fount or don not exists! ***')
        return False

    def connect_to_desktop(self):
        '''
        connect to the windows desktop
        '''
        if not cli_setup():
            auto_setup(__file__,logdir=True,devices=["Windows:///",])
        else:
            self.log.error('\n\t ***can not connect to the windows desktop***.')
            return False

    def connect_to_special_panel(self,title=''):
        '''
        connect to the workwechat main window.
        '''
        conn = AirConn(title=title)
        try:
            conn.connect_to_target_window()
            return True
        except Exception as e:
            self.log.error(f'\n\t *** can not connect to the workwechat,detil error info: ***\n\t {e}')
            return False

    # def connect_to_sop_chat(self):
    #     '''
    #     connect to the sop chat panel.
    #     '''
    #     conn = AirConn(title='SOP消息')
    #     try:
    #         conn.connect_to_target_window()
    #     except Exception as e:
    #         self.log.error(f'\n\t —— can not connect to the sop-chat panel,detil error info: ——\n\t {e}')
    #     sleep(0.2)

    # def connect_to_sending_helper(self):
    #     '''
    #     connect to the sending-msg-to-my-customer panel.
    #     '''
    #     conn = AirConn(title='向我的客户发消息')
    #     try:
    #         conn.connect_to_target_window()
    #     except Exception as e:
    #         self.log.error(f'\n\t —— can not connect to the sending-panel,detil error info: ——\n\t {e}')
    #     sleep(0.2)
    
    # def connect_to_select_custom_panel(self):
    #     '''
    #     connect to the workwechat main window.
    #     '''
    #     conn = AirConn(title='选择客户')
    #     try:
    #         conn.connect_to_target_window()
    #     except Exception as e:
    #         self.log.error(f'\n\t —— can not connect to the workwechat,detil error info: ——\n\t {e}')
    #     sleep(0.2)
    
    # def connect_to_msg_sending_confirm(self):
    #     '''
    #     connect to the message-sending-confirm panel.
    #     '''
    #     conn = AirConn(title='消息发送确认')
    #     try:
    #         conn.connect_to_target_window()
    #     except Exception as e:
    #         self.log.error(f'\n\t —— can not connect to the workwechat,detil error info: ——\n\t {e}')
    #     sleep(0.2)

    # def connect_to_text(self):
    #     '''
    #     connect to the message-sending-confirm panel.
    #     '''
    #     conn = AirConn(title='123.txt - 记事本')
    #     try:
    #         conn.connect_to_target_window()
    #     except Exception as e:
    #         self.log.error(f'\n\t —— can not connect to the workwechat,detil error info: ——\n\t {e}')
    #     sleep(0.2)

    def send_keys(self, keys):
        """
        输入keys中的内容，如果是'\n'则意为回车发送
        """
        if keys in ('\n',):
            pywinauto.keyboard.SendKeys('\n', with_newlines=True)
            return
        # parsed_keys = self.parse_key(keys)
        parsed_keys = keys
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
        try:
            pos = find_all(Template('photos\%s.png' %photo_name))
            if pos is not None:
                offset_x = 0 if kwargs.get('x') is None else kwargs.get('x')
                offset_y = 0 if kwargs.get('y') is None else kwargs.get('y')
                pos_x = int(pos[0].get('result')[0]) + offset_x
                pos_y = int(pos[0].get('result')[1]) + offset_y
                touch((pos_x,pos_y))
                return True
            else:
                return False
        except Exception as e:
            print(f'\n\t ***some error occured when touch target ui:{e}***')
            return False
    else:
        try:
            touch(Template('photos\%s.png' %photo_name))
            return True
        except Exception as e:
            print(f'\n\t ***some error occured when touch target ui:{e}***')
            return False

def exists_ui(photo_name=''):
    '''
    judge if the ui exists.
    '''
    try:
        res = exists(Template('photos\%s.png' %photo_name))
        if res:
            return True
        else:
            return False
    except Exception as e:
            print(f'\n\t ***some error occured when judge target ui exists:{e}***')
            return False

def find_ui(photo_name=''):
    '''
    find all exists ui in panel.
    '''
    res = find_all(Template('photos\%s.png' %photo_name))
    if res is not None:
        return res
    else:
        return False

def shot(photo_name=''):
    snapshot(filename = '..\\photos\\%s.png' % photo_name,quality=99,max_size=1200)