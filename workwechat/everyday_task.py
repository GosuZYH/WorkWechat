# -*- encoding=utf8 -*- 
from airtest.core.api import *
from PIL import Image
from base import Base,exists_ui,touch_ui,find_ui,shot
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot,assert_equal


class EveryDayTask(Base):
    def __init__(self):
        super().__init__()
        # self.connect_to_workwechat()

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
        * base on having openned the customer-sop.
        '''
        self.connect_to_special_panel(title='SOP消息')
        try_times = 0
        while True:
            if try_times > 3:
                return False
            if exists_ui('跳转到群发助手'):
                self.log.info('\n\t —— find the group sending helper! ——')
                sleep(0.2)
                break
            else:
                self.connect_to_special_panel(title='SOP消息')
                self.log.info('\n\t —— can not find the group sending helper! ——')
                try_times += 1
                sleep(3)
        try:
            touch_ui('跳转到群发助手')
            self.log.info('\n\t —— touch the button ——')
            return True
        except:
            self.log.error('\n\t —— can not find sending button——')

    def select_the_customer(self):
        '''
        after open the sending helper,select the customer tag.
        '''
        self.connect_to_special_panel(title='向我的客户发消息')
        try_times = 0
        while True:
            if try_times > 3:
                return False
            if exists_ui('选择客户'):
                sleep(0.2)
                break
            else:
                self.connect_to_special_panel(title='向我的客户发消息')
                try_times += 1
                sleep(3)
        try:
            touch_ui('选择客户')
            return True
        except:
            self.log.error('\n\t —— can not find select customer button——')

    def select_customer_tag(self):
        '''
        select the customer tags.
        '''
        self.connect_to_special_panel(title='选择客户')
        try_times = 0
        while True:
            if try_times > 3:
                return False
            if exists_ui('不限标签'):
                sleep(0.2)
                break
            else:
                self.connect_to_special_panel(title='选择客户')
                try_times += 1
                sleep(3)
        try:
            touch_ui('不限标签')
            return True
        except:
            self.log.error('\n\t —— can not find select tag mini-menu ——')

    def search_target_tag(self):
        '''
        search target customer tag from the list.
        '''
        self.connect_to_special_panel(title='选择客户')
        self.connect_to_desktop()
        try:
            #此处写寻找标签逻辑
            touch_ui('选择标签男')

            touch_ui('确定')
            self.connect_to_special_panel('选择客户')
            sleep(0.5)
            touch_ui('全选客户',x=-25)
            sleep(0.5)
            touch_ui('确定')
        except Exception as e:
            self.log.error(f'\n\t —— some error occured when selected the customer,detil error info: ——\n\t {e}')

    def send_message_to_customer(self):
        '''
        send message to my customer.
        '''
        self.connect_to_special_panel(title='向我的客户发消息')
        try:
            touch_ui('发送')
        except Exception as e:
            self.log.error(f'\n\t —— some error occured when send msg to customer step1,detil error info: ——\n\t {e}')
        self.connect_to_special_panel(title='向我的客户发消息')
        try:
            touch_ui('确认发送')
        except:
            self.log.error(f'\n\t —— some error occured when send msg to customer,step2,detil error info: ——\n\t {e}')

    def test(self):
        '''
        test
        '''
        # self.connect_to_select_custom_panel()
        # self.connect_to_desktop()
        # touch_ui('全选客户',x=-25)
        print(self.check_window_exists(title='SOP消息'))
        # self.connect_to_special_panel(title='SOP消息')
        # shot('当前截屏')
        

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
        # self.search_target_tag()
        # self.send_message_to_customer()

        # self.test()

task = EveryDayTask()
task.run_task()
