# -*- encoding=utf8 -*- 
from airtest.core.api import *
import win32clipboard
from base import Base,exists_ui,touch_ui,find_ui,shot,show_ui,find_all_ui,touch_ui1
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot,assert_equal

from constants import WINDOW_LIST


class EveryDayTask(Base):
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

    def click_luoshu_SMR_in_chat_list(self):
        '''
        如果聊天列表中有洛书SMR-test
        直接点击
        :return:
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui('消息列表-洛书'):
                self.log.info('目标在列表中,直接点击')
                touch_ui('消息列表-洛书')
                return True
            else:
                return False
        except Exception as e:
            self.log.info(e)
            return False

    def search_the_SMR(self,str='洛书SMR-test'):
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
            self.log.info('input "洛书SMR-test"')
            text(str)
            self.connect_to_desktop()
            if exists_ui('查询结果-洛书'):
                self.log.info('找到查询结果')
                touch_ui('查询结果-洛书')
                if self.connect_to_special_panel('企业微信'):
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def second(self):
        try:
            if self.click_luoshu_SMR_in_chat_list() or self.search_the_SMR():
                return True
            while True:
                self.check_for_extra_windows(title='洛书SMR-test')
                if self.first() == True:
                    if self.click_luoshu_SMR_in_chat_list() or self.search_the_SMR() == True:
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
        确定当前在页面在洛书SMR-test对话框
        如果不在,执行self.search_the_SMR
        进入洛书SMR-test的聊天对话框并返回一个Trun
        如果没有进入到洛书SMR聊天框,则返回False
        :return:
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui('洛书SMR-test聊天窗口') or exists_ui('洛书SMR-test聊天窗口1'):
                self.log.info('当前在洛书聊天页面')
                sleep(2)
                touch_ui('聊天页笑脸', y=-10)
                return True
            else:
                return False
        except Exception as e:
            self.log.info('判断当前页面是否是与洛书SMR-test聊天页面的过程中出错')
            return False


    def screenshot_of_contrast(self):
        '''
        :return: True:翻到最上边  Stop:当前没有任务
        '''
        try:
            self.connect_to_special_panel('企业微信')
            if exists_ui('洛书SOP'):
                self.log.info('当前处在与洛书SMR-test的聊天记录页面')
                while True:
                    touch_ui('聊天页笑脸')
                    self.log.info('消息页置顶任务--准备在翻页前后截图做对比')
                    snapshot(filename='..\\photos\\test1.png')
                    keyevent('{PGUP 5}')   #向上翻5页
                    snapshot(filename='..\\photos\\test2.png')
                    self.log.info('消息页置顶任务--开始比对前后截图')
                    with open('photos\\test1.png', 'rb') as test1:
                        res1 = test1.read()
                    with open('photos\\test2.png', 'rb') as test2:
                        res2 = test2.read()
                    if res1 == res2:
                        self.log.info('前后对比结果一致')
                        return True
                    else:
                        self.log.info('前后对比结果不一致,继续翻页对比')
                        continue
            else:
                if exists_ui('洛书SMR-test聊天窗口') or exists_ui('洛书SMR-test聊天窗口1'):
                    return 'stop'
                else:
                    self.log.info('当前不在聊天页面')
                    return False
        except Exception as e:
            self.log.error('消息页置顶任务--对比翻页前后截图出错'+str(e))
            return False

    # 这里是1对1话术任务处理的第一阶段
    # def up_to_find(self):
    #     '''
    #     Scroll up on the message page
    #     如果两次截图的结果相等,则返回Turn 否则返回False
    #     :return:
    #     '''
    #     if touch_ui('聊天页笑脸') == False:
    #         self.log.info('\n\t没有检测到聊天页面,返回上一步')
    #         return False
    #     if self.is_in_chat_list() and self.screenshot_of_contrast():
    #         self.log.info('第一次判断正在sop一对一聊天页面中,返回True')
    #         return True
    #     if self.connect_to_workwechat() and self.is_in_chat_list():
    #         while self.connect_to_workwechat():
    #             self.log.info('开始判断是否是消息列表最顶端')
    #             if self.is_in_chat_list() and self.screenshot_of_contrast():
    #                 list = []
    #                 while True:
    #                     list.clear()  #清空列表,防止循环时存在其他元素
    #                     if self.is_in_chat_list():
    #                         try:
    #                             touch_ui('聊天页笑脸', y=-10)
    #                             for i in range(2):
    #                                 self.log.info('将对比结果放入list中')
    #                                 list.append(self.screenshot_of_contrast())
    #                             self.log.info(f'2次对比结果为{all(list)}')
    #                             if False in list:
    #                                 continue
    #                             else:
    #                                 self.log.info(f'2次对比结果为{all(list)},当前在最顶端')
    #                                 return True
    #                         except Exception as e:
    #                             self.log.error('进行多次对比截图时出错'+str(e))
    #                             return False
    #     else:
    #         return False

    def check_for_extra_windows(self,title=None):
        '''
        点击1v1任务之前确保无其他多余窗口存在
        有则杀死并返回True
        :return:
        '''
        try:
            self.connect_to_special_panel('企业微信')
            while True:
                if title is None:
                    self.log.info('清除多余窗口')
                    for i in WINDOW_LIST:
                        while self.connect_to_special_panel(i):
                            self.log.info(f'检测到额外的窗口{i},将要关掉她')
                            self.send_keys('%{F4}')
                    return True
                else:
                    if self.connect_to_special_panel(title):
                        self.log.info(f'检测到额外的窗口{title},将要关掉她')
                        self.send_keys('%{F4}')
                        return True
                    else:
                        return True
        except Exception as e:
            self.log.info('清除多余窗口的过程中出错')
            return False

    def third(self):
        '''
        返回值:
            True 可以继续任务
            stop:没有任务
        '''
        try:
        #     if self.screenshot_of_contrast() == True:
        #         return True
        #     elif self.screenshot_of_contrast() == 'stop':
        #         return 'stop'
            while True:
                if self.second() == True:
                    if self.is_in_chat_list() == True:
                        if self.screenshot_of_contrast() == True:
                            return True
                        elif self.screenshot_of_contrast() == 'stop':
                            self.log.info('没有任务,停止执行')
                            return 'stop'
                        else:
                            self.log.info('third执行第三步的时候出错')
                            continue
                    else:
                        self.log.info('third执行第二步的时候出错')
                        continue
                else:
                    self.log.info('third执行第一步的时候出错')
                    continue
        except Exception as e:
            self.log.info('到达消息最上方的过程中出错')
            return False

    def get_sop_1v1_task_status(self):
        '''
        判断sop执行状态
        未执行返回True
        已执行返回False
        :return:
        '''
        try:
            c = True
            conut = 0
            conut1=0
            while c:
                self.log.info('判断sop执行是否是已执行状态')
                if self.connect_to_special_panel('SOP消息'):
                    sleep(2)
                    self.connect_to_special_panel('SOP消息')
                    if exists_ui('已回执') and exists_ui('已回执按钮'):
                        self.log.info('关闭当前页面')
                        self.send_keys('%{F4}')
                        self.connect_to_workwechat()
                        self.log.info('当前框中的sop话术状态为已执行')
                        return 'delete'
                    self.log.info('判断sop执行是否是可执行状态')
                    self.connect_to_special_panel('SOP消息')
                    if not exists_ui('已回执') and exists_ui('已回执按钮'):
                        self.log.info('当前sop任务为未执行状态')
                        if self.connect_to_special_panel('SOP消息'):
                            self.log.info('当前任务为可执行状态')
                            return True
                    else:
                        self.log.info('没有识别到sop话术任务的状态,继续寻找')
                        conut+=1
                        if conut < 10:
                            self.log.info(f'尝试第{conut}次寻找状态')
                            sleep(1)
                            self.connect_to_special_panel('SOP消息')
                            continue
                        else:
                            self.log.info(f'尝试寻找{conut}次状态未果,退出寻找')
                            c = False
                            self.connect_to_special_panel('SOP消息')
                            self.send_keys('%{F4}')
                            return False
                else:
                    self.log.info('链接SOP消息框的过程中出错')
                    conut1 += 1
                    if conut1 < 10:
                        self.connect_to_special_panel('SOP消息')
                        self.log.info(f'尝试第{conut1}次链接SOP消息窗口')
                        sleep(1)
                        continue
                    else:
                        self.log.info(f'尝试寻找{conut1}次状态未果,退出寻找')
                        c = False
                        self.connect_to_special_panel('SOP消息')
                        self.send_keys('%{F4}')
                        return False
        except Exception as e:
            self.log.info('获取sop1v1任务状态的过程中出错'+str(e))
            return False

    def delete_sop_1v1_task(self):
        '''
        删除最顶部的任务
        :return:
        '''
        try:
            while True:
                if self.third():
                    self.log.info('当前在最顶端,准备删除任务')
                    if self.is_in_chat_list():
                        touch(find_all_ui('任务类型1v1')[0],right_click=True)
                        self.send_keys('{DOWN 6}')
                        self.send_keys('{ENTER}')
                        self.connect_to_special_panel('提示')
                        self.send_keys('{ENTER}')
                        return True
                    else:
                        continue
                else:
                    continue
        except Exception as e:
            self.log.info('删除任务的过程中出错'+str(e))
            return False

    def click_sop_1v1_task(self):
        '''
        :return:True False
        '''
        try:
            self.check_for_extra_windows()
            self.connect_to_workwechat()
            if touch(find_all_ui('任务类型1v1')[0]):
                sleep(2)
                if self.connect_to_special_panel('SOP消息'):
                    self.log.info('识别sop话术任务状态')
                    return True
                else:
                    self.log.info('链接窗口失败')
                    # 这里可能是断网,现在是跳过
                    # 之后可以做ping百度的操作,如果ping不同就做一个程序意外停止的弹框
                    return False
            else:
                return False
        except Exception as e:
            self.log.info('点击聊天页面最顶端元素的过程中出错')
            return False

    def fourth(self):
        try:
            while True:

                if self.third() == True:
                    if self.click_sop_1v1_task() == 'delete':
                        self.log.info('检测到当前任务已经做好,删除它')
                        if self.delete_sop_1v1_task():
                            self.log.info('fourth获取任务状态时时候出错')
                            if self.check_for_extra_windows():
                                continue
                        else:
                            continue
                    elif self.click_sop_1v1_task() == True:
                        if self.get_sop_1v1_task_status() == True:
                            return True
                        else:
                            self.log.info('fourth获取任务状态时时候出错')
                            if self.check_for_extra_windows():
                                continue
                    else:
                        self.log.info('点击聊天任务出错')
                        if self.check_for_extra_windows():
                            continue
                elif self.third() == 'stop':
                    return 'stop'
                else:
                    self.log.info('fourth执行第一步时候出错')
                    continue
        except Exception as e:
            self.log.info(''+str(e))
            return False

    #这里是1对1话术任务处理的第二阶段,确定当前页面是否有可以执行的1v1sop话术任务,如果有就返回True,如果没有就返回False
    def do_sop1v1_task(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        try:
            while True:
                if self.fourth() == True:
                    return True
                elif self.fourth() == 'stop':
                    return 'stop'
                else:
                    return False
        except Exception as e:
            self.log.info('做任务之前的任务出错'+str(e))
            return False
    
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
        while True:
            if self.copy_sop_tag():
                print(1)
            else:
                break
        print('跳出了循环')

        # while not self.click_group_sending_helper():
        #     self.copy_sop_tag()

        # while not self.select_the_customer():
        #     self.click_group_sending_helper()

        # while not self.select_customer_tag():
        #     self.select_the_customer()

        # if not self.search_target_tag():
        #     if self.connect_to_special_panel('选择客户'):
        #             self.connect_to_desktop()
        #             touch_ui('取消1')
        #             if self.connect_to_special_panel('选择客户'):
        #                 touch_ui('取消2')
        #                 if self.check_window_exists(title='向我的客户发消息'):
        #                     self.log.info('\n\t —— Target panel exists. ——')
        #                     if self.connect_to_special_panel(title='向我的客户发消息'):
        #                         touch_ui('关闭1')
        #                         if self.check_window_exists(title='SOP消息'):
        #                             self.log.info('\n\t —— Target panel exists. ——')
        #                             if self.connect_to_special_panel(title='SOP消息'):
        #                                 touch_ui('关闭2')
        #     return '该客户缺少标签'

        # while not self.select_all_customer():
        #     self.search_target_tag()

        # while not self.send_message_to_customer():
        #     self.select_all_customer()
        # a = self.do_sop1v1_task()
        # a = self.first()
        # a = self.second()
        # a = self.third()
        # a = self.fourth()
        # a = self.click_luoshu_SMR_in_chat_list()
        # a = self.search_the_SMR()
        # a = self.screenshot_of_contrast()
        # a = self.is_in_chat_list()
        # a = self.check_for_extra_windows()
        # a = self.get_sop_1v1_task_status()
        # a = self.delete_sop_1v1_task()
        # print(a)


    def run_task(self):
        '''
        '''

        res = self.test()

if __name__ == '__main__':
    task = EveryDayTask()
    task.run_task()
