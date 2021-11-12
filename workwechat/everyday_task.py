# -*- encoding=utf8 -*- 
from airtest.core.api import *
from PIL import Image
import win32clipboard
from base import Base,exists_ui,touch_ui,find_ui,shot,show_ui
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
    
    def copy_sop_tag(self):
        '''
        every day 1V1 sending.
        * base on having openned the customer-sop.
        '''
        if self.check_window_exists(title='SOP消息'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='SOP消息'):
                if touch_ui('点击复制'):
                    sleep(0.2)
                    win32clipboard.OpenClipboard()
                    copy_tag= win32clipboard.GetClipboardData()
                    self.copy_tag = copy_tag.replace('_', ' ')
                    win32clipboard.CloseClipboard()
                    sleep(0.5)
                    return True
                self.log.error('\n\t *** can not find the click-copy button! ***')
        return False

    def click_group_sending_helper(self):
        '''
        click the turn-to-sending-helper button
        '''
        if self.check_window_exists(title='SOP消息'):
            self.log.info('\n\t —— Target panel exists. ——')
            if self.connect_to_special_panel(title='SOP消息'):
                if touch_ui('跳转到群发助手'):
                    self.log.info('\n\t —— touch the sending-helper button ——')
                    sleep(0.3)
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
        if self.check_window_exists(title='选择客户'):
            self.log.info('\n\t —— Target panel exists. ——')
            while True:
                if self.connect_to_special_panel('选择客户'):
                    self.connect_to_desktop()
                pos = self.get_target_tag_position()
                if pos:
                    self.log.info('\n\t —— Find target! Touch the Target tag. ——')
                    touch(pos)
                    sleep(0.5)
                    return True
                else:
                    shot('test1')
                    self.log.info('\n\t —— can not find target tag in this page. ——')
                    self.scroll_the_tag_panel()
                    shot('test2')
                    with open('photos\\test1.png', 'rb') as test1:
                        res1 = test1.read()
                    with open('photos\\test2.png', 'rb') as test2:
                        res2 = test2.read()
                    sleep(0.3)
                    if res1 == res2:
                        return False
        return False

    def select_all_customer(self):
        '''
        select all customer.
        '''
        if not self.connect_to_desktop():
            return False
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

    def scroll_the_tag_panel(self):
        '''
        scroll 1 page down in select tag panel.
        '''
        if not self.connect_to_desktop():
            return False
        # if touch_ui('选择标签'):
        #     self.log.info('\n\t —— Touch the Select tag text. ——')
        if  find_ui('选择标签'):
            pos = find_ui('选择标签')[0]
            for i in range(4):
                self.mouse_scroll(x=pos.get('result')[0],y=pos.get('result')[1]+100,wheel_dist=-1)
                sleep(0.3)
            return True

    def test(self):
        '''
        test
        '''
        while not self.copy_sop_tag():
            sleep(1)
            print('wait for 1s')

        while not self.click_group_sending_helper():
            self.copy_sop_tag()

        while not self.select_the_customer():
            self.click_group_sending_helper()

        while not self.select_customer_tag():
            self.select_the_customer()

        if not self.search_target_tag():
            if self.connect_to_special_panel('选择客户'):
                    self.connect_to_desktop()
                    touch_ui('取消1')
                    if self.connect_to_special_panel('选择客户'):
                        touch_ui('取消2')
                        if self.check_window_exists(title='向我的客户发消息'):
                            self.log.info('\n\t —— Target panel exists. ——')
                            if self.connect_to_special_panel(title='向我的客户发消息'):
                                touch_ui('关闭1')
                                if self.check_window_exists(title='SOP消息'):
                                    self.log.info('\n\t —— Target panel exists. ——')
                                    if self.connect_to_special_panel(title='SOP消息'):
                                        touch_ui('关闭2')
            return '该客户缺少标签'

        while not self.select_all_customer():
            self.search_target_tag()

        while not self.send_message_to_customer():
            self.select_all_customer()



        # self.connect_to_special_panel('SOP消息')
        # self.connect_to_desktop()
        # shot('test')
        # show_ui('test')


    def run_task(self):
        '''
        '''
        
        # self.open_sending_helper()
        # self.select_the_customer()
        # self.select_customer_tag()
        # self.search_target_tag()
        # self.send_message_to_customer()

        res = self.test()

if __name__ == '__main__':
    task = EveryDayTask()
    task.run_task()
