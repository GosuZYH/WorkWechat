# -*- encoding=utf8 -*-
__author__ = "zyh"
import os
import time
import win32gui
import logging

from abc import ABC
import pywinauto
import pytesseract
import win32clipboard
import numpy as np
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.aircv import cv2
from airtest.aircv import *

from init_airtest import AirConn
from setup_log import Logger

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
        # self.connect_to_special_panel('SOP消息')
        # touch(Template(r"photos\点击复制.png", record_pos=(-0.01, 0.003), resolution=(600, 720)))
        # #   # 获取复制内容（并做处理）
        # win32clipboard.OpenClipboard()
        # label_target = win32clipboard.GetClipboardData()
        # label_target = label_target.replace('_', ' ')
        # win32clipboard.CloseClipboard()
        
        # #   # “转跳到群发助手”
        # touch(Template(r"photos\tpl1636619069985.png", record_pos=(-0.003, 0.51), resolution=(600, 720)))

        # print('\t -111')

        # # “向我的客户发消息”
        # self.connect_to_special_panel('向我的客户发消息')
        # touch(Template(r"photos\tpl1636619146759.png", record_pos=(-0.234, -0.229), resolution=(500, 415)))

        # print('\t 222')

        # # "选择客户" 界面
        # self.connect_to_special_panel('选择客户')

        # print('\t 333')

        #   # 保证为未点击状态（操作比较复杂）
        # if not exists(Template(r"tpl1636535273023.png", record_pos=(-0.423, -0.216), resolution=(620, 500))):
        #     print('\t111')
        #     every_day_task.select_customer_tag()

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

def show_ui(photo_name=''):
    local = aircv.imread('photos\%s.png' % photo_name)
    show_origin_size(img = local)