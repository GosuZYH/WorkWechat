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
        if self.check_window_exists(title='SOP消息'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='SOP消息'):
                if touch_ui('跳转到群发助手'):
                    sleep(0.5)
                    self.log.info('\n\t —— touch the sending helper button ——')
                    return True
                self.log.error('\n\t *** can not find the group sending helper! ***')
        return False

    def select_the_customer(self):
        '''
        after open the sending helper,select the customer tag.
        '''
        if self.check_window_exists(title='向我的客户发消息'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='向我的客户发消息'):
                if touch_ui('选择客户'):
                    sleep(0.5)
                    self.log.info('\n\t —— touch the select customer button ——')
                    return True
                self.log.error('\n\t *** can not find select customer button! ***')
        return False

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

    def search_target_tag(self):
        '''
        search target customer tag from the list.
        '''
        if not self.connect_to_desktop():
            return False
        if touch_ui('选择标签男'):
            sleep(0.5)
            self.log.info('\n\t —— touch the select tag. ——')
            if touch_ui('确定'):
                sleep(0.5)
                self.log.info('\n\t —— touch the confirm button. ——')
                if self.check_window_exists(title='选择客户'):
                    self.log.info('\n\t —— Target panel exists. ——')
                    if self.connect_to_special_panel(title='选择客户'):
                        sleep(0.5)
                        if touch_ui('全选客户',x=-25):
                            sleep(0.5)
                            self.log.info('\n\t —— touch the select all customer button. ——')
                            if touch_ui('确定'):
                                sleep(0.5)
                                self.log.info('\n\t —— touch the confirm button. ——')
                                return True
        self.log.error(f'\n\t *** some error occured when selected the customer ***')
        return False

    def send_message_to_customer(self):
        '''
        send message to my customer.
        '''
        if self.check_window_exists(title='向我的客户发消息'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='向我的客户发消息'):
                if touch_ui('发送'):
                    sleep(0.5)
                    self.log.info('\n\t —— Touch the send button. ——')
                    if touch_ui('确认发送'):
                        sleep(0.5)
                        self.log.info('\n\t —— Touch the Confirm-sending button. ——')
                        return True
        self.log.error(f'\n\t *** some error occured when send msg to customer ***')
        return False

    def test(self):
        '''
        test
        '''
        # touch_ui('全选客户',x=-25)
        # print(self.check_window_exists(title='SOP消息'))
        self.connect_to_special_panel(title='SOP消息')
        print(find_ui('选择客户'))
        # shot('当前截屏')

    def run_task(self):
        '''
        '''
        while not self.open_sending_helper():
            sleep(1)
            print('wait for 1s')

        while not self.select_the_customer():
            self.open_sending_helper()

        while not self.select_customer_tag():
            self.select_the_customer()

        while not self.search_target_tag():
            self.select_customer_tag()

        while not self.send_message_to_customer():
            self.search_target_tag()

        self.open_sending_helper()
        self.select_the_customer()
        self.select_customer_tag()
        self.search_target_tag()
        self.send_message_to_customer()

        # self.test()

task = EveryDayTask()
task.run_task()
