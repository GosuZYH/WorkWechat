# -*- encoding=utf8 -*-
__author__ = "zyh"
import os
import time

import win32gui
import win32con
import logging
import winreg

from abc import ABC
import pywinauto
from psutil import process_iter
import pytesseract
import numpy as np
from airtest.core.api import *
from airtest.core.settings import Settings
from airtest.cli.parser import cli_setup
from airtest.aircv import cv2
from airtest.aircv import *
from pywinauto import Application, mouse

from init_airtest import AirConn
from setup_log import Logger

# ST.RESIZE_METHOD = staticmethod(cocos_min_strategy)
ST.THRESHOLD = 0.5  # [0, 1]图像识别的阈值
ST.THRESHOLD_STRICT = 0.7  # [0, 1]这是一个更加严格的阈值设定，只用于assert_exists(图片)接口。
ST.OPDELAY = 0.1  # 即每一步操作后等待0.1秒
ST.FIND_TIMEOUT = 3  # 设置寻找元素的等待时间,默认为20  默认是find_timeout = ST.FIND_TIMEOUT
ST.FIND_TIMEOUT_TMP = 3  ##设置寻找元素的等待时间,默认为3   默认是find_timeout = ST.FIND_TIMEOUT
# ST.PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "") # for using other script

class Base(ABC):
    '''
    base operation in workwechat.
    '''
    def __init__(self):
        log = Logger(level='debug')
        self.log = log.logger
        self.copy_tag = None


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

    # def check_window_exists(self,title='',all=False):
    #     '''
    #     check all exists windows the
    #     '''
    #     if all == True:
    #         set1 = {0}
    #         win32gui.EnumWindows(self.get_all_hwnd, 0)
    #         for h, t in self.hwnd_title.items():
    #             if t not in list:
    #                 set1.update(t)
    #         return set1
    #     elif all == False:
    #         handlers = []
    #         win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
    #         time.sleep(0.1)
    #         for handler in handlers:
    #             if win32gui.GetWindowText(handler) == title:
    #                 return True
    #         return False

    def get_all_hwnd(self,hwnd, mouse):
        self.hwnd_title ={}
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    def connect_to_desktop(self):
        '''
        connect to the windows desktop
        '''
        if not cli_setup():
            auto_setup(__file__,logdir=True,devices=["Windows:///",])
            return True
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

    def mouse_scroll(self, x: int = None, y: int = None, wheel_dist: int = 1) -> None:
        self.log.info(f"mouse scroll at ({x},{y}) with wheel dist {wheel_dist}")
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

    def find_contours(self,img_screen):
        height, width, channels = img_screen.shape
        img_binary = np.zeros((height, width), dtype='uint8')
        
        for i in range(height):
            for j in range(width):
                if (img_screen[i, j][0] == 237 and
                        img_screen[i, j][1] == 237 and
                        img_screen[i, j][2] == 237):
                    img_binary[i, j] = 255
        
        contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        logging.info('\n\tNumber of contours: %s' % len(contours))
        # print('\n\tNumber of contours: %s' % len(contours))
        # cv2.imshow('001', img_binary)
        # cv2.waitKey(1)
        return contours
    
    def select_customer_tag(self):
        '''
        select the customer tags.
        '''
        if self.check_window_exists(title='选择客户'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='选择客户'):
                if touch_ui('不限标签'):
                    sleep(0.5)
                    self.log.info('\n\t —— touch the tag mini-menu ——')
                    return True
                self.log.error('\n\t *** can not find select tag mini-menu! ***')
        return False
    
    def get_target_tag_position(self):
        '''
        get target tag's position by OCR.
        '''
        img_select_custom_panel_name = 'screen_select_custom_panel.png'
        screen_img_path = os.path.join(os.getcwd(), 'photos', img_select_custom_panel_name)
        snapshot(filename=screen_img_path, msg=img_select_custom_panel_name)
        img_select_custom_panel = cv2.imread(screen_img_path)
        h_select_custom_panel, w_select_custom_panel = img_select_custom_panel.shape[:2]
        print('\t\t', h_select_custom_panel, w_select_custom_panel)
        template_select_custom_panel = Template(r"%s" % screen_img_path)
        
        # 桌面截屏
        self.connect_to_desktop()
        screen_desk = G.DEVICE.snapshot()
        x_m, y_m = template_select_custom_panel.match_in(screen_desk)

        # 截屏范围
        x_s = x_m - w_select_custom_panel / 2
        y_s = y_m - h_select_custom_panel / 2
        x_t = x_m + w_select_custom_panel / 2
        y_t = y_m + h_select_custom_panel / 2

        # 再次进入"选择客户"界面，并点击
        self.connect_to_special_panel('选择客户')
        # self.select_customer_tag()
        time.sleep(1)
        # 再次桌面截屏，并选取变化之后的"选择客户"界面
        self.connect_to_desktop()
        screen_desk = G.DEVICE.snapshot()
        time.sleep(0.5)
        local_screen = aircv.crop_image(screen_desk, (x_s, y_s, x_t, y_t))
        # cv2.imshow('000', local_screen)
        # cv2.waitKey(0)
        local_contours = self.find_contours(local_screen)
        list_rst_cnt = []
        kernel = np.ones((2, 2), np.uint8)

        for cnt in local_contours:
            if cv2.contourArea(cnt) > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                img_ocr = aircv.crop_image(local_screen, (x, y, x + w, y + h))
                img_ocr = cv2.cvtColor(img_ocr, cv2.COLOR_BGR2GRAY)
                img_ocr = cv2.resize(img_ocr, (0, 0), fx=2.9, fy=2.9, interpolation=cv2.INTER_CUBIC)
                ocr_text = pytesseract.image_to_string(
                    img_ocr, lang='chi_sim', config="-c page_separator=''")
                touch_x = x_s + x + w / 2
                touch_y = y_s + y + h / 2
                list_rst_cnt.append([ocr_text.strip(), [touch_x, touch_y]])
                # cv2.imshow('zzz', img_ocr)
                # print('ocr_text = ', ocr_text)
                # cv2.waitKey(0)

        touch_pos = []
        for rst_cnt in list_rst_cnt:
            print(rst_cnt)
            if rst_cnt[0] == self.copy_tag:
                touch_pos = rst_cnt[1]
        return touch_pos

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
                    self.log.info('找到企微pid')
                    pid_num = pid_dic ['pid']
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
            if self.connect_to_special_panel('企业微信'):
                return True
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Tencent\WXWork')  # 利用系统的链表
            file_path = str(winreg.QueryValueEx(key, "Executable")[0])
            app = pywinauto.Application(backend='uia')
            app.start(file_path)
            sleep(2)
            conut = 1
            c = True
            while c:
                app = pywinauto.Application(backend='uia')
                app.start(file_path)
                sleep(2)
                if self.connect_to_special_panel('企业微信'):
                    self.log.info('企微窗口启动成功')
                    return True
                elif conut <= 10:
                    self.log.info(f'尝试第{conut}次启动企业微信')
                    conut+=1
                    continue
                else:
                    self.log.info(f'{conut}次启动企业微信失败,返回False')
                    return False
        except Exception as e:
                self.log.info('企微窗口启动失败'+str(e))
                return False
    
    def get_WXWork_handle(self,title='企业微信'):

        win32gui.EnumWindows(self.get_all_hwnd, 0)
        for h, t in self.hwnd_title.items():
            if t == title:
                return h
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
        if self.check_window_exists(title='企业微信'):
            if self.connect_to_special_panel('企业微信'):
                self.log.info('企业微信已经连接')
                return True
        if self.start_WXWork():
            sleep(2)
            if self.connect_to_special_panel('企业微信'):
                self.log.info('企业微信已经连接')
                return True
        if self.get_WXWork_pid():
            self.log.info('找到企业微信pid')
            if self.get_WXWork_handle() == False:
                self.log.info('找到企业微信的handle')
                try:
                    if self.connect_to_special_panel('企业微信'):
                        self.log.info('企微窗口唤起成功')
                        return True
                    else:
                        self.log.error('企微窗口启动失败')
                        return False
                except Exception as e:
                    self.log.error('企微窗口启动失败'+str(e))
                    return False
            elif self.check_window_exists(title='企业微信') == True:
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
        count = 1

        while True:
            if self.open_WXWork_window():
                return True
            else:
                if count<=10:
                    continue
                else:
                    return self.open_WXWork_window()
    def H5_page_get_element(self,title='回执',page='SOP消息',type='Text',click=False):
        '''
        寻找h5页面的元素,如果找到返回坐标信息,但是类型是pywinauto的类型
        :param title: 需要链接的企业微信下的页面元素名
        :param page: 需要链接企业微信下的页面title
        :param type: 需要寻找的元素类型
        :param click: 默认为False不进行点击操作,True则进行点击操作
        :return: True:执行成功/False:执行失败
        '''
        try:
            self.app = Application(backend='uia')
            self.app.connect(process=self.get_WXWork_pid())
            self.win = self.app[page]   #.print_control_identifiers()
            res = self.win.child_window(title=title,control_type=type)
            position = res.rectangle()
            if click==True:
                self.log.info('\n\t点击复制')
                mouse.click(button='left', coords=(position.left + 10, position.top + 10))
                return True
            elif click == False:
                return True
        except Exception as e:
            self.log.error('寻找元素时出错'+str(e))
            return False
        # mouse.click(button='left', coords=(position.left + 10, position.top + 10))

        # return res

    def kill_target_windows(self,target_title=[]):
        '''
        kill all unuseful panel by handle
        '''
        handlers = []
        win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
        time.sleep(0.1)
        for handler in handlers:
            title = win32gui.GetWindowText(handler)
            if title in target_title:
                self.log.info(f'kill window {title}')
                win32gui.PostMessage(handler,win32con.WM_CLOSE,0,0)

def touch_ui(photo_name='',threshold=ST.THRESHOLD,rgb=False,**kwargs):
    '''
    touch the ui in photo.
    * if have kwargs: will touch the central point coordinate offset.
    '''
    if kwargs:
        try:
            pos = find_all(Template('photos\%s.png' %photo_name,threshold=threshold,rgb=rgb))
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
            touch(Template('photos\%s.png' %photo_name,threshold=threshold,rgb=rgb))
            return True
        except Exception as e:
            print(f'\n\t ***some error occured when touch target ui:{e}***')
            return False

def touch_ui1(photo_name=''):
    '''
    只是判断能不能点击
    '''
    try:
        touch(Template('photos\%s.png' %photo_name))
        return True
    except Exception as e:
        print(f'\n\t ***some error occured when touch target ui:{e}***')
        return False

def exists_ui(photo_name='',threshold=ST.THRESHOLD,rgb=False):
    '''
    judge if the ui exists.
    '''
    try:
        res = exists(Template('photos\%s.png' %photo_name,threshold=threshold,rgb=rgb))
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

def find_all_ui(photo_name='',threshold=ST.THRESHOLD, rgb=False):
    '''
    find all exists ui in panel.
    '''
    list = []
    res = find_all(Template(r'photos\%s.png' % photo_name,threshold=threshold, rgb=rgb))
    if res is not None:
        for i in res:
            list.append(i.get('result'))
        return list
    else:
        return False

def shot(photo_name=''):
    snapshot(filename = '..\\photos\\%s.png' % photo_name,quality=99,max_size=1200)

def show_ui(photo_name=''):
    local = aircv.imread('photos\%s.png' % photo_name)
    show_origin_size(img = local)

if __name__ == '__main__':
    a = Base()


