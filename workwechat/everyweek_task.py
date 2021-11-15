# -*- encoding=utf8 -*-
import poco
from airtest.core.api import *
import win32clipboard
from base import Base,exists_ui,touch_ui,find_ui,shot,show_ui,find_all_ui,touch_ui1
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot,assert_equal

from constants import WINDOW_LIST


class EveryWeekTask(Base):
    def __init__(self):
        super().__init__()

    def find_the_chat(self):
        '''
        turn to the chat panel.
        如果当前是消息页,就返回Trun
        如果无法做操作就返回False
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui('消息1_1') and exists_ui('消息1'):
                self.log.info('当前在消息列表页')
                self.connect_to_special_panel('企业微信')
                return True
            elif exists_ui('消息2'):
                self.log.info('点击消息按钮')
                touch_ui('消息2')
                if self.connect_to_workwechat():
                    self.log.info('当前页面是消息页面')
                    return True
                else:
                    return False
        except Exception as e:
            self.log.error('进入消息列表页出错'+str(e))
            return False

    def first(self):
        try:
            if self.find_the_chat():
                return True
            else:
                while True:
                    if self.connect_to_workwechat() == True:
                        if  self.find_the_chat() == True:
                            return True
                        else:
                            self.log.info('first执行第二步的时候出错')
                            continue
                    else:
                        self.log.info('first执行第一步的时候出错')
                        continue
        except Exception as e:
            self.log.info('\n\tfirst函数执行出错'+str(e))
            return False

    def click_customer_contact_in_chat_list(self):
        '''
        如果聊天列表中有'客户联系'
        直接点击
        :return:
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui(r'every_week_task\消息列表-客户联系'):
                self.log.info('目标在列表中,直接点击')
                touch_ui(r'every_week_task\消息列表-客户联系')
                return True
            else:
                return False
        except Exception as e:
            self.log.info(e)
            return False

    def search_the_customer_contact(self,str='客户联系'):
        '''
        search the str in chat-list.
        return Ture:已找到 False:未找到
        '''
        try:

            self.connect_to_special_panel('企业微信')
            self.log.info('点击放大镜')
            touch_ui('搜索框放大镜')
            if exists_ui('搜索框取消'):
                self.log.info('检测到搜索框中有文字,点击清空搜索框')
                touch_ui('搜索框取消')
            self.log.info('input "客户联系"')
            text(str, search=True)
            self.connect_to_desktop()
            if exists_ui(r'every_week_task\查询结果-客户联系'):
                self.log.info('找到查询结果')
                touch_ui(r'every_week_task\查询结果-客户联系')
                if self.connect_to_special_panel('企业微信'):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.log.info(e)
            return False

    def second(self):
        try:
            if self.click_customer_contact_in_chat_list() or self.search_the_customer_contact():
                return True
            while True:
                self.check_for_extra_windows(title='客户联系')
                if self.first() == True:
                    if self.click_customer_contact_in_chat_list() or self.search_the_customer_contact() == True:
                        return True
                    else:
                        self.log.info('second执行第二步的时候出错')
                        continue
                else:
                    self.log.info('second执行第一步的时候出错')
                    continue
        except Exception as e:
            self.log.info('\n\tsecond函数出错'+str(e))
            return False

    def is_in_chat_list(self):
        '''
        确定当前在页面在"客户联系"对话框
        进入"客户联系"的聊天对话框并返回一个Trun
        如果没有进入到"客户联系"聊天框,则返回False
        :return:
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui(r'every_week_task\客户联系聊天窗口') and exists_ui(r'消息1_1'):
                self.log.info('当前在"客户联系"聊天页面')
                sleep(2)
                touch_ui(r'every_week_task\聊天页空白处', y=-10)
                if exists_ui(r'every_week_task\客户联系聊天页面消息箭头') == True:
                    keyevent('{END}')
                    return True
                elif exists_ui(r'every_week_task\客户联系聊天页面消息箭头') == False:
                    return 'stop'
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.log.info('判断当前页面是否是"客户联系"聊天页面的过程中出错')
            return False

    def third(self):
        '''
        返回值:
            True 可以继续任务
            stop:没有任务
        '''
        try:
            while True:
                if self.second() == True:
                    if self.is_in_chat_list() == True:
                        print('当前消息页有消息')
                        return True
                    elif self.is_in_chat_list() == 'stop':
                        return 'stop'
                    else:
                        continue
                else:
                    continue
        except Exception as e:
            self.log.info('到达消息最上方的过程中出错')
            return False

    def do_every_week_task(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        try:
            while True:
                if self.third() == True:
                    pass
                    continue
                elif self.third() == 'stop':
                    return 'stop'
                else:
                    return False
        except Exception as e:
            self.log.info('做任务之前的任务出错'+str(e))
            return False

    def test(self):
        '''
        test
        '''
        a = self.do_every_week_task()
        # a = self.first()
        # a = self.second()
        # a = self.third()
        # a = self.fourth()
        # a = self.fifth()
        # a = self.sixth()
        # a = self.click_luoshu_SMR_in_chat_list()
        # a = self.search_the_SMR()
        # a = self.swip_sop1v1_windows()
        # a = self.screenshot_of_contrast()
        # a = self.is_in_chat_list()
        # a = self.check_for_extra_windows()
        # a = self.get_sop_1v1_task_status()
        # a = self.delete_sop_1v1_task()
        # a = self.select_the_customer()
        # a = self.search_target_tag()
        print(a)

    def run_task(self):
        '''
        '''

        res = self.test()

if __name__ == '__main__':
    task = EveryWeekTask()
    task.run_task()
    # task.connect_to_special_panel('企业微信')
    # touch_ui(r'every_week_task\聊天页空白处', y=-10)