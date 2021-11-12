# -*- encoding=utf8 -*-
__author__ = "zyh"

import winreg
from abc import ABC
import logging
import time
import win32gui
import pywinauto
import pytesseract
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from setup_log import Logger
from psutil import process_iter
from init_airtest import AirConn


global hwnd_title
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

    def check_window_exists(self,title='',all=False):
        '''
        check all exists windows the
        '''

        if all == True:
            set1 = {0}
            win32gui.EnumWindows(self.get_all_hwnd, 0)
            for h, t in self.hwnd_title.items():
                if t not in list:
                    set1.update(t)
            return set1
        elif all == False:
            handlers = []
            win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
            time.sleep(0.1)
            for handler in handlers:
                if win32gui.GetWindowText(handler) == title:
                    return True
            return False

    def connect_to_desktop(self):
        '''
        connect to the windows desktop
        '''
        if not cli_setup():
            auto_setup(__file__,logdir=True,devices=["Windows:///",])

    def connect_to_special_panel(self,title=''):
        '''
        connect to the workwechat main window.
        '''
        conn = AirConn(title=title)
        try:
            conn.connect_to_target_window()
            return True
        except Exception as e:
            self.log.error(f'\n\t —— can not connect to the workwechat,detil error info: ——\n\t {e}')
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

    def get_WXWork_pid(self):
        '''
        Determine whether WXWork's process exists
        If it doesn't exist,then return False
        :return:
        '''
        try:
            PID = process_iter()
            for pid_temp in PID:
                pid_dic = pid_temp.as_dict(attrs=['pid', 'name'])
                if pid_dic['name'] == 'WXWork.exe':
                    pid_num = pid_dic['pid']
                    return pid_num
                else:
                    continue
            return False
        except Exception as e:
            return False

    def start_WXWork(self):
        '''
        通过链表找到企微的执行文件并启动
        如果找到就启动它并返回True
        否则就返回False
        '''
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Tencent\WXWork')  # 利用系统的链表
            file_path = str(winreg.QueryValueEx(key, "Executable")[0])
            app = pywinauto.Application(backend='uia')
            app.start(file_path)
            self.log.info('企微窗口启动成功')
            return True
        except Exception as e:
            self.log.info('企微窗口启动失败'+str(e))
            return False

    def get_all_hwnd(self,hwnd, mouse):
        self.hwnd_title ={}
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


    def get_WXWork_handle(self):

        win32gui.EnumWindows(self.get_all_hwnd, 0)
        for h, t in self.hwnd_title.items():
            if t == '企业微信':
                return True
            else:
                pass
        return False

    def open_WXWork_window(self):
        '''
        start WorkChat windows
        if WXWork-process is killed
        then return:False
        else return:True
        '''
        global hwnd_title
        hwnd_title = {}
        if self.get_WXWork_pid() != False:
            self.log.info('找到企业微信pid')
            if self.get_WXWork_handle() == False:
                self.log.info('找到企业微信的handle')
                try:
                    if self.start_WXWork():
                        self.log.info('企微窗口唤起成功')
                        return True
                    else:
                        self.log.error('企微窗口启动失败')
                        return False
                except Exception as e:
                    self.log.error('企微窗口启动失败'+str(e))
                    return False
            elif self.get_WXWork_handle() == True:
                if self.start_WXWork():
                    self.log.info('企微窗口唤起成功')
                    return True
                else:
                    self.log.error('企微窗口启动失败')
                    return False
            else:
                return False
        else:
            if self.start_WXWork():
                sleep(2)
                return True
            else:
                return False

    def connect_to_workwechat(self):
        '''
        保证企微进程以及窗口在最上边
        :return:
        '''
        if self.connect_to_special_panel('企业微信'):
            self.log.info('企业微信已连接')
            return True
        else:
            while True:
                if self.open_WXWork_window():
                    if self.start_WXWork():
                        self.connect_to_special_panel('企业微信')
                        return True
                    else:
                        self.start_WXWork()
                        sleep(2)
                        self.connect_to_special_panel('企业微信')
                        return True
                else:
                    self.log.info('链接微信失败')
                    return False

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
            touch((pos_x,pos_y))
        else:
            return False
    else:

        return touch(Template('photos\%s.png' % photo_name))

def exists_ui(photo_name=''):
    '''
    judge if the ui exists.
    '''
    try:
        res = exists(Template('photos\%s.png' % photo_name))
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
    return find_all(Template('photos\%s.png' %photo_name))

def find_all_ui(photo_name=''):
    '''
    find all exists ui in panel.
    '''
    list = []
    res = find_all(Template(r'photos\%s.png' % photo_name))
    if res is not None:
        for i in res:
            list.append(i.get('result'))
        return list
    else:
        return False

def shot(photo_name=''):
    snapshot(filename = '..\\photos\\%s.png' % photo_name,quality=99,max_size=1200)



if __name__ == '__main__':
    a = Base()
    a.connect_to_workwechat()
    # hwnd_title ={}
    # res = a.check_window_exists(all=True)
    # res = find_ui('任务类型1v1')
    # res1 = find_all_ui('任务类型1v1')
    # print(res)
    # print(res1)
    # print(get_windows_handle())