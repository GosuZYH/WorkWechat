# -*- encoding=utf8 -*-
__author__ = "zyh"
import time
import re
import requests
import json
import socket
from datetime import datetime

from win32api import GetSystemMetrics
import win32gui, win32print, win32con

Screen_dict = {"wide": GetSystemMetrics(win32con.SM_CXSCREEN), "high": GetSystemMetrics(win32con.SM_CYSCREEN)}

import winreg
from abc import ABC
import pywinauto
from airtest.core.api import ST, auto_setup, sleep
from airtest.aircv import imread, get_resolution
from airtest.cli.parser import cli_setup
from pywinauto import Application, mouse
from psutil import process_iter

from .init_airtest import AirConn
from .setup_log import Logger
from .baidu_OCR import SMROCR
from .constants import *

# ST.RESIZE_METHOD = staticmethod(cocos_min_strategy)
ST.THRESHOLD = 0.5  # [0, 1]图像识别的阈值
ST.THRESHOLD_STRICT = 0.7  # [0, 1]这是一个更加严格的阈值设定，只用于assert_exists(图片)接口。
ST.OPDELAY = 0.1  # 即每一步操作后等待0.1秒
ST.FIND_TIMEOUT = 2  # 设置寻找元素的等待时间,默认为20  默认是find_timeout = ST.FIND_TIMEOUT
ST.FIND_TIMEOUT_TMP = 3  ##设置寻找元素的等待时间,默认为3   默认是find_timeout = ST.FIND_TIMEOUT


# ST.DEBUG=True
# ST.LOG_DIR='photos\\log'
# ST.LOG_FILE='log.log'
# ST.SAVE_IMAGE = False
# ST.PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "") # for using other script


class Base(ABC):
    """
    base operation in workwechat.
    """

    def __init__(self):
        log = Logger(level='debug')
        self.log = log.logger
        self.copy_tag = None
        self.ocr_results = None
        self.file_name = None
        self.scale = round(get_real_resolution()['wide'] / Screen_dict['wide'], 2)
        self.handle = None
        self.hwnd_title = {}

    def check_window_exists(self, title=''):
        """
        check all exists windows the
        """
        handlers = []
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            if win32gui.GetWindowText(handler) == title:
                return True
        self.log.error(f'\n\t ***{title} window not found or not exists! ***')
        return False

    def get_all_hwnd(self, hwnd, mouse):

        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    def connect_to_desktop(self):
        """
        connect to the windows desktop
        """
        if not cli_setup():
            auto_setup(__file__, devices=["Windows:///", ])
            return True
        else:
            self.log.error('\n\t ***can not connect to the windows desktop***.')
            return False

    def connect_to_special_panel(self, title=''):
        """
        connect to the workwechat main window.
        """
        i = 0
        try:
            qwx_pid = self.get_WXWork_pid()
            if not qwx_pid:
                self.start_WXWork()
            conn = AirConn(title=title)
            conn.connect_to_target_window()
            self.handle = conn.target_handler
            return True
        except Exception as e:
            i += 1
            if i <= 3:
                self.log.error(f'\n\t *** 第 %d 次连接 title=%s 窗体失败，将再做尝试 ***\n\t' % (i, title))
                return self.connect_to_special_panel('企业微信')
            else:
                self.log.error(f'\n\t *** can not connect to the workwechat,detil error info: ***\n\t {e}')
                return False

    def start_WXWork(self):
        """
        通过链表找到企微的执行文件并启动
        如果找到就启动它并返回True
        否则就返回False
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Tencent\WXWork')
            file_path = str(winreg.QueryValueEx(key, "Executable")[0])
            app = pywinauto.Application(backend='uia')
            if self.get_WXWork_pid():
                app.start(file_path)
                sleep(1)
                return True
            else:
                self.log.info('\n\t未检测到企业微信进程id,准备启动企业微信')
                app.start(file_path)
                self.log.info('\n\t启动中......')
                sleep(3)
                self.log.info('\n\t启动成功...')
                return True
        except Exception as e:
            self.log.debug('企微窗口启动失败' + str(e))
            return False

    def mouse_scroll(self, x: int = None, y: int = None, wheel_dist: int = 1) -> None:
        self.log.debug(f"mouse scroll at ({x},{y}) with wheel dist {wheel_dist}")
        if (x is None and y is None) or (x < 0 or y < 0):
            raise ValueError(f"Can't click on given coordinates: ({x}, {y})")
        pywinauto.mouse.scroll(coords=(x, y), wheel_dist=wheel_dist)

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

    def parse_key(self, keys=None, parse_to=" ") -> str:
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

    def use_ocr(self, file_path):
        """
        Using baidu outline Ocr-SDK.
        """
        ocr = SMROCR()
        if file_path:
            return ocr.request_ocr(file_path, file_name=self.file_name)
        else:
            return ''

    def get_ocr_result(self, file_path):
        self.ocr_results = self.use_ocr(file_path)

    def get_target_position(self, target_text):
        """
        complete matching.
        """
        p = re.compile('(-|_|——| |)')
        target_text = p.sub('', target_text)
        for result in self.ocr_results:
            word = result.get('result')
            word = p.sub('', word)
            if target_text == word:
                x1 = result.get('x1')
                x2 = result.get('x2')
                x3 = result.get('x3')
                x4 = result.get('x4')
                y1 = result.get('y1')
                y2 = result.get('y2')
                y3 = result.get('y3')
                y4 = result.get('y4')
                posx = (x1 + x2) // 2
                posy = (y1 + y3) // 2
                return posx, posy
        return False

    def _get_target_position(self, target_text):
        """
        part matching.
        """
        p = re.compile('(-|_|——| |)')
        target_text = p.sub('', target_text)
        for result in self.ocr_results:
            word = result.get('result')
            word = p.sub('', word)
            if target_text in word:
                x1 = result.get('x1')
                x2 = result.get('x2')
                x3 = result.get('x3')
                x4 = result.get('x4')
                y1 = result.get('y1')
                y2 = result.get('y2')
                y3 = result.get('y3')
                y4 = result.get('y4')
                posx = (x1 + x2) // 2
                posy = (y1 + y3) // 2
                return posx, posy
        return False

    @staticmethod
    def move_window_to(hwin, x=5, y=5):
        hwin.move_window(x=x, y=y)

    def connect_window_before_shot(self, title):
        """
        connect to target window before screen shot it.
        (Exactly due to solve the connect too many times lead to window breakdown.)
        (Exactly used in close window)
        """

        self.connect_to_special_panel('企业微信')
        try:
            app = Application().connect(title_re=title, handle=self.handle)
            hwin = app.top_window()
            hwin.set_focus()
        except Exception as e:
            self.log.error(f'set focus error:{e}')
        return hwin

    def get_top_window_hwin(self, title):
        app = Application().connect(title_re=title)
        hwin = app.top_window()
        return hwin

    def shot_target_window(self, title, hwin, file_name=None):
        """
        connect to the target window and shotscreen.
        """
        try:
            if file_name is not None:
                self.file_name = title + '_' + file_name + '_' + str(round(time.time() * 1000))
            else:
                self.file_name = title + '_' + str(round(time.time() * 1000))
            file_path = r'%s\\%s.png' % (PHOTO_PATH, self.file_name)
            img = hwin.capture_as_image().save(file_path)
            return file_path
        except Exception as e:
            self.log.error(f'some error occured when connect to the {title} window,detail info:{e}')
            return None

    def get_WXWork_pid(self):
        """
        Determine whether WXWork's process exists
        If it doesn't exist,then return False
        :return:
        """
        try:
            PID = process_iter()
            for pid_temp in PID:
                pid_dic = pid_temp.as_dict(attrs=['pid', 'name'])
                if pid_dic['name'] == 'WXWork.exe':
                    self.log.debug('找到企微pid')
                    pid_num = pid_dic['pid']
                    return pid_num
                else:
                    continue
            return False
        except Exception as e:
            return False

    def get_WXWork_handle(self, title='企业微信'):

        win32gui.EnumWindows(self.get_all_hwnd, 0)
        for h, t in self.hwnd_title.items():
            if t == title:
                return h
            else:
                pass
        return False

    def H5_page_get_element(self, title='回执', page='SOP消息', type='Text', click=False):
        """
        寻找h5页面的元素,如果找到返回坐标信息,但是类型是pywinauto的类型
        :param title: 需要链接的企业微信下的页面元素名
        :param page: 需要链接企业微信下的页面title
        :param type: 需要寻找的元素类型
        :param click: 默认为False不进行点击操作,True则进行点击操作
        :return: True:执行成功/False:执行失败
        """
        try:
            self.app = Application(backend='uia')
            self.app.connect(process=self.get_WXWork_pid())
            self.win = self.app[page]  # .print_control_identifiers()
            res = self.win.child_window(title=title, control_type=type)
            position = res.rectangle()
            if click == True:
                self.log.debug('\n\t点击复制')
                mouse.click(button='left', coords=(position.left + 10, position.top + 10))
                return True
            elif click == False:
                return True
        except Exception as e:
            self.log.error('寻找元素时出错' + str(e))
            return False
        # mouse.click(button='left', coords=(position.left + 10, position.top + 10))

        # return res

    def kill_target_windows(self, target_title=[]):
        """
        kill all unuseful panel by handle
        """
        handlers = []
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            title = win32gui.GetWindowText(handler)
            if title in target_title:
                self.log.debug(f'kill window {title}')
                win32gui.PostMessage(handler, win32con.WM_CLOSE, 0, 0)

    def get_img_size(self, file_path):
        """
        give a opposite img file path,return img size.
        """
        img = imread(filename=file_path)
        h, w = get_resolution(img)
        # show_origin_size(img)
        h, w = get_resolution(img)
        return h, w

    def dingtalk_robot(self, time):
        # 获取RPA运作电脑名称
        hostname = socket.gethostname()
        if not hostname:
            hostname = '暂未获取到'
        # 获取本机IP
        rpa_ip = socket.gethostbyname(hostname)
        if not rpa_ip:
            hostname = '暂未获取到'

        # 钉钉监控群机器人
        url1 = 'https://oapi.dingtalk.com/robot/send?access_token=bb7dca554d5af31d967a3467ab76258b3aec87a2007b174398f78918590f2244'
        # ...更多群机器人

        program = {
            "msgtype": "text",
            "text": {"content": 'RPA机器名: ' + str(hostname) +
                                '\n机器IP: ' + str(rpa_ip) +
                                '\n开启了新一轮任务' +
                                '\n冷却时间：' + str(time) + '秒'
                                                        '\n日期: ' + str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                     }
        }
        headers = {'Content-Type': 'application/json'}
        try:
            f1 = requests.post(url1, data=json.dumps(program), headers=headers)
        except Exception as e:
            print('***send data error!***', e)


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return {"wide": wide, "high": high}


# if __name__ == '__main__':
#     ok = Base()
#     # ok.dingtalk_robot()
#     while True:
#         hwin = ok.connect_window_before_shot(title='企业微信')
#         file = ok.shot_target_window(title='企业微信', hwin=hwin)
#         h, w = ok.get_img_size(file_path=file)
#         ok.log.debug(f'\n\t —— 当前顶部窗口大小为{h}x{w},屏幕缩放比例为{ok.scale} ——')
