# -*- encoding=utf8 -*-
__author__ = "26579"

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

from init_airtest import AirConn
from psutil import process_iter

logger = logging.getLogger(__name__)
global hwnd_title


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
            return True
        except Exception as e:
            logger.error(f'—— can not connect to the workwechat,detil error info: ——\n\t {e}')
            sleep(0.2)
            return False


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

    def connect_to_text_panel(self):
        '''
        connect to the workwechat main window.
        '''
        conn = AirConn(title='镜像源.txt - 记事本')
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
    return find_all(Template(rf'photos\{photo_name}.png'))

def find_all_ui(photo_name=''):
    '''
    find all exists ui in panel.
    '''
    list = []
    res = find_all(Template(r'photos\%s.png' % photo_name))
    for i in res:
        list.append(i.get('result'))
    return list

def shot(photo_name=''):
    snapshot(filename = '..\\photos\\%s.png' % photo_name,quality=99,max_size=1200)

def get_WXWork_pid():
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
                logger.info('找到企微 pid')
                return pid_num
            else:
                logger.info('没有找到企微pid')
                continue
        logger.info('不存在企业微信pid')
        return False
    except Exception as e:
        logger.error('获取pid时出错'+str(e))
        return False

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

def get_WXWork_handle():
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t == '企业微信':
            return True
        else:
            pass
    return False

def start_WXWork():
    '''
    通过链表找到企微的执行文件并启动
    如果找到就启动它并返回True
    否则就返回False
    '''
    try:
        logger.info('获取企微执行文件路径')
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Tencent\WXWork')  # 利用系统的链表
        file_path = str(winreg.QueryValueEx(key, "Executable")[0])
        logger.info('打开企业微信窗口')
        app = pywinauto.Application(backend='uia')
        app.start(file_path)
        return True
    except Exception as e:
        logger.error('启动企微程序时出错'+str(e))
        return False

def open_WXWork_window():
    '''
    start WorkChat windows
    if WXWork-process is killed
    then return:False
    else return:True
    '''
    global hwnd_title
    hwnd_title = {}
    if get_WXWork_pid() != False:
        if get_WXWork_handle() == False:
            try:
                if start_WXWork():
                    return True
                else:
                    return False
            except Exception as e:
                logger.error('获取企微执行文件路径过程中出错'+str(e))
                return False
        elif get_WXWork_handle() == True:
            return True
        else:
            return False
    else:
        logger.info('企微没有运行,尝试启动企业微信')
        if start_WXWork():
            sleep(2)
            return True
        else:
            return False

if __name__ == '__main__':
    print(open_WXWork_window())