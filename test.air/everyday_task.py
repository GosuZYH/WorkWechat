# -*- encoding=utf8 -*-
from airtest.core.api import *
import logging
from PIL import Image
from init_airtest import AirConn
from photos import Base,exists_ui,touch_ui,find_all_ui
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot


logger = logging.getLogger(__name__)
class EveryDayTask(Base):
    def __init__(self):
        self.end_flag = False
        self.connect_to_workwechat()

    def find_the_chat(self):
        '''
        turn to the chat panel.
        '''
        conn = AirConn(title='企业微信')
        conn.connect_to_target_window()
        if exists_ui('消息2'):
            logger.info('点击消息按钮')
            touch_ui('消息2')
        else:
            logger.info('当前页面是消息页面')

    def search_the_SMR(self,str='洛书SMR-test'):
        '''
        search the str in chat-list.
        return Ture:已找到 False:未找到
        '''
        conn = AirConn(title='企业微信')
        conn.connect_to_target_window()
        if exists_ui('搜索框'):
            logger.info('点击放大镜')
            touch_ui('搜索框放大镜')
        if exists_ui('搜索框取消'):
            logger.info('检测到搜索框中有文字,点击清空搜索框')
            touch_ui('搜索框取消')
        sleep(0.2)
        # self.send_keys(str)
        text(str)
        if exists_ui('查询结果-洛书'):
            logger.info('LuoShu-SMP mini program has been found and is ready to click on it')
            touch_ui('查询结果-洛书')
            return True
        else:
            logger.error('can not find the LuoShu-SMR mini-program')
            return False

    def back_to_latest_position(self):
        '''
        turn to the latest position
        '''
        if exists_ui('回到最新位置'):
            touch_ui('回到最新位置')

    def click_message_list_task(self,coordinate):
        '''
        Click to open the SOP box
        :param coordinate:(x,y)坐标  -->The type is a tuple.
        :return:
        eg:点击窗口的x=100,y=100处位置
            click_message_list_task(100,100)
        '''

        touch(coordinate)
    def find_sop_task(self):
        '''
        Coordinates of all matched elements in the window
        :param pic:a image path
        :return:
        找到元素,返回每个元素的坐标 [(x1,y1),(x2,y2),...,(xn,yn)]
        一直找到最顶上的消息都没有找到元素的坐标就返回 Fales
        '''
        conn = AirConn(title='企业微信')
        conn.connect_to_target_window()




    def receipt_the_custom_sop(self):
        '''
        receipt the 1v1 custom sop everyday.
        '''

        pass

    def open_sending_helper(self):
        '''
        every day 1V1 sending.
        '''
        self.connect_to_sop_chat()
        sleep_time = 0
        while True:
            if exists_ui('跳转到群发助手') or sleep_time > 5:
                sleep(0.2)
                break
            else:
                self.connect_to_sop_chat()
                logger.info('can not find sending button,time sleep 1s..')
                sleep_time += 1
                sleep(1)
        try:
            touch_ui('跳转到群发助手')
        except:
            logger.info('can not find sending button')

    def select_the_customer(self):
        '''
        after open the sending helper,select the customer tag.
        '''
        self.connect_to_sending_helper()
        sleep_time = 0
        while True:
            if exists_ui('选择客户') or sleep_time > 5:
                sleep(0.2)
                break
            else:
                self.connect_to_sending_helper()
                logger.info('can not find select customer button,time sleep 1s..')
                sleep_time += 1
                sleep(1)
        try:
            touch_ui('选择客户')
        except:
            logger.info('can not find select customer button')

    def select_customer_tag(self):
        '''
        select the customer tags.
        '''
        self.connect_to_select_custom_panel()
        sleep_time = 0
        while True:
            if exists_ui('选择客户标签') or sleep_time > 5:
                sleep(0.2)
                break
            else:
                self.connect_to_select_custom_panel()
                logger.info('can not find select tag mini-menu,time sleep 1s..')
                sleep_time += 1
                sleep(1)
        try:
            touch_ui('选择客户标签')
        except:
            logger.info('can not find select tag mini-menu')

    def search_target_tag(self):
        '''
        search target customer tag from the list.
        '''
        pass

    def test(self):
        '''
        test
        '''
        sleep(2)

    def run_task(self):
        '''
        '''
        # self.find_the_chat()
        # self.search_the_SMR()
        # self.back_to_latest_position()
        # self.receipt_the_custom_sop()
        self.open_sending_helper()
        self.select_the_customer()
        self.select_customer_tag()
        #self.connect_to_sop_chat()
        a = self.find_sop_task()
        print(a)
        # touch((411, 149))
        # a =  [(445, 378),(445, 195)]
        # # b =
        # print(a[0])
        # self.click_message_list_task(a[0])



task = EveryDayTask()
task.run_task()
