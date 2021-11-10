# -*- encoding=utf8 -*-
from airtest.core.api import *
import logging
from PIL import Image
from init_airtest import AirConn
from photos import Base,exists_ui,touch_ui,find_ui
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
        if exists_ui('消息1'):
            return
        else:
            touch_ui('消息2')

    def search_the_SMR(self):
        '''
        search the luoshu SMR in chat-list.
        '''
        if exists_ui('清空'):
            touch_ui('清空')
        sleep(0.2)
        if exists_ui('搜索框'):
            touch_ui('搜索框')
        text('洛书SMR')
        sleep(1)
        touch_ui('洛书SMR1')
        # if exists_ui('应用与小程序'):
            # if exists_ui('洛书SMR1'):
            #     touch_ui('洛书SMR1')
            # elif exists_ui('洛书SMR2'):
            #     touch_ui('洛书SMR2')
            # else:
            #     logger.error('can not find the LuoShu-SMR mini-program')
        # else:
        #     logger.error('can not find app and mini-program')

    def back_to_latest_position(self):
        '''
        turn to the latest position
        '''
        if exists_ui('回到最新位置'):
            touch_ui('回到最新位置')

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
        self.connect_to_select_custom_panel()
        self.connect_to_desktop()
        try:
            #此处写寻找标签逻辑
            touch_ui('确定')
            self.connect_to_select_custom_panel()
            sleep(0.5)
            touch_ui('全选客户',x=-25)
            sleep(0.5)
            touch_ui('确定')
        except Exception as e:
            logger.error(f'—— some error occured when selected the customer,detil error info: ——\n\t {e}')

    def test(self):
        '''
        test
        '''
        self.connect_to_select_custom_panel()
        self.connect_to_desktop()
        touch_ui('全选客户',x=-25)

    def run_task(self):
        '''
        '''
        self.find_the_chat()
        # self.search_the_SMR()
        # self.back_to_latest_position()
        # self.receipt_the_custom_sop()

        # self.open_sending_helper()
        # self.select_the_customer()
        # self.select_customer_tag()

        # self.search_target_tag()
        self.test()

task = EveryDayTask()
task.run_task()
