# -*- encoding=utf8 -*-
import win32gui
from airtest.core.api import *
from PIL import Image
from base import Base,exists_ui,touch_ui,find_ui,shot,find_all_ui
from airtest.aircv import *
from airtest.core.api import Template, exists, touch, auto_setup, connect_device,snapshot#,assert_equalre

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
        if exists_ui('消息1_1') and exists_ui('消息1'):
            self.log.info('当前在消息列表页')
            return True
        if self.connect_to_workwechat():
            try:
                if exists_ui('消息1_1') and exists_ui('消息1'):
                    if  self.connect_to_workwechat():
                        self.log.info('当前页面是消息页面')
                        return True
                    else:
                        return False
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
        else:
            return False

    def click_luoshu_SMR_in_chat_list(self):
        '''
        如果聊天列表中有洛书SMR-test
        直接点击
        :return:
        '''
        if self.check_for_extra_windows(title='洛书SMR-test'):

            if self.find_the_chat():
                if exists_ui('消息列表-洛书'):
                    self.log.info('目标在列表中,直接点击')
                    touch_ui('消息列表-洛书')
                    return True
                else:
                    return False
            else:
                return False

    def search_the_SMR(self,str='洛书SMR-test'):
        '''
        search the str in chat-list.
        return Ture:已找到 False:未找到
        '''
        self.check_for_extra_windows(title='洛书SMR-test')
        if exists_ui('洛书SMR-test聊天窗口') or self.click_luoshu_SMR_in_chat_list():
            self.log.info('当前在聊天窗口')
            return True
        # if self.find_the_chat() and exists_ui('洛书SMR-test聊天窗口'):
        #     '''
        #     判断当前聊天页面是否是洛书SMR-test页面
        #     如果是,直接返回True
        #     不是继续往下走
        #     '''
        #     try:
        #         self.log.info('鼠标点击聊天记录页面')
        #         touch_ui('聊天页笑脸', y=-10)
        #         if self.connect_to_workwechat():
        #             self.log.info('当前页面是消息页面')
        #             return True
        #         else:
        #             return False
        #     except Exception as e:
        #         self.log.error('搜索洛书SMR-test之后没有连接到企微窗口或没有有点击到聊天页面')
        #         if self.find_the_chat():
        #             return True
        #         else:
        #             return False
        if self.connect_to_workwechat() and self.find_the_chat():
            '''
            判断是否在消息列表页
            如果在就进行搜索操作
            '''
            if exists_ui('搜索框'):
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
                try:
                    if self.connect_to_workwechat():
                        self.log.info('当前页面是消息页面')
                        return True
                    else:
                        return False
                except Exception as e:
                    self.log.error('搜索洛书SMR-test之后没有连接到企微窗口或没有有点击到聊天页面'+e)
                    self.log.error(e)
                    return False
            else:
                self.log.error('can not find the LuoShu-SMR mini-program')
            return False
        else:
            return False

    def is_in_chat_list(self):
        '''
        确定当前在页面在洛书SMR-test对话框
        如果不在,执行self.search_the_SMR
        进入洛书SMR-test的聊天对话框并返回一个Trun
        如果没有进入到洛书SMR聊天框,则返回False
        :return:
        '''
        while True:
            if exists_ui('当前在与洛书SMR-test的聊天页面') and self.search_the_SMR():
                self.log.info('当前在洛书聊天页面')
                return True
            while True:
                if self.search_the_SMR():
                    try:
                        if self.connect_to_workwechat():
                            self.log.info('当前在与洛书SMR-test的聊天页面')
                            touch_ui('聊天页笑脸', y=-10)
                            return True
                        else:
                            return False

                    except Exception as e:
                        self.log.error('判断是否链接企微窗口或点击聊天页面的过程中出错'+str(e))
                        return False
                else:
                    return False

    def screenshot_of_contrast(self):
        '''
        在翻页前后进行两次截图
        然后对比截图的二进制文件
        如果一样返回True
        否则返回False
        :return:
        '''
        try:
            self.log.info('消息页置顶任务--准备在翻页前后截图做对比')
            snapshot(filename='test1.png')
            keyevent('{PGUP 2}')
            snapshot(filename='test2.png')
        except Exception as e:
            self.log.error('消息页置顶任务--执行截图或翻页时出错'+str(e))
            return False
        try:
            self.log.info('消息页置顶任务--开始比对前后截图')
            with open('log\\test1.png', 'rb') as test1:
                res1 = test1.read()
            with open('log\\test2.png', 'rb') as test2:
                res2 = test2.read()
            return res1 == res2
        except Exception as e:
            self.log.error('消息页置顶任务--对比翻页前后截图出错'+str(e))
            return False

    # 这里是1对1话术任务处理的第一阶段
    def up_to_find(self):
        '''
        Scroll up on the message page
        如果两次截图的结果相等,则返回Turn 否则返回False
        :return:
        '''
        if self.is_in_chat_list() and self.screenshot_of_contrast():
            self.log.info('第一次判断正在sop一对一聊天页面中,返回True')
            return True
        if self.connect_to_workwechat() and self.is_in_chat_list():
            while self.connect_to_workwechat():
                self.log.info('开始判断是否是消息列表最顶端')
                if self.is_in_chat_list() and self.screenshot_of_contrast():
                    list = []
                    while True:
                        if self.is_in_chat_list():
                            try:
                                touch_ui('聊天页笑脸', y=-10)
                                for i in range(2):
                                    self.log.info('将对比结果放入list中')
                                    list.append(self.screenshot_of_contrast())
                                self.log.info(f'2次对比结果为{all(list)}')
                                if all(list) == True:
                                    self.log.info(f'2次对比结果为{all(list)},当前在最顶端')
                                    return True
                            except Exception as e:
                                self.log.error('进行多次对比截图时出错'+str(e))
                                return False
        else:
            return False

    def check_for_extra_windows(self,title=None):
        '''
        点击1v1任务之前确保无其他多余窗口存在
        有则杀死并返回True
        :return:
        '''
        while True:
            if title is None:
                self.log.info('清除多余窗口')
                res = self.check_window_exists(all=True) & WINDOW_LIST
                print(self.check_window_exists(all=True))
                if len(res)==0:
                    self.log.info('没有检测到多余窗口,退出检测')
                    return True
                else:
                    for i in res:
                        self.log.info(f'检测到额外的窗口{i},将要关掉她')
                        self.connect_to_special_panel(i)
                        sleep(0.5)
                        self.send_keys('%{F4}')
                        self.log.info(f'窗口{i}已被关闭')
                    self.log.info('再次检测是否有同名的窗口')
                    if len(res) == 0:
                        self.log.info('没有同名窗口,窗口清除完毕,退出检测')
                        return True
                    else:
                        self.log.info('检测到同名窗口,准备再次清理')
                        continue
            else:
                self.log.info(f'检测到额外的窗口{title}')
                set = {title}
                res = self.check_window_exists(all=True) & set
                if len(res) > 0:
                    for i in res:
                        self.log.info(f'检测到额外的窗口{i},将要关掉她')
                        self.connect_to_special_panel(i)
                        sleep(0.5)
                        self.send_keys('%{F4}')
                        self.log.info(f'窗口{i}已被关闭')
                    return True
                else:
                    self.log.info(f'没有检测到独立的{title}窗口')
                    return True

    def get_sop_1v1_task_status(self):
        '''
        判断sop执行状态
        未执行返回True
        已执行返回False
        :return:
        '''
        c = True
        conut = 0
        while c:
            self.log.info('判断sop执行是否是已执行状态')
            if self.connect_to_special_panel('SOP消息'):
                self.connect_to_desktop()
                if exists_ui('已回执') and exists_ui('已回执按钮'):
                    self.log.info('当前框中的sop话术状态为已执行')
                    self.log.info('关闭当前页面')
                    self.send_keys('%{F4}')
                    self.connect_to_workwechat()
                    return 'delete'
                self.log.info('判断sop执行是否是可执行状态')
                self.connect_to_desktop()
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
                        continue
                    else:
                        self.log.info(f'尝试寻找{conut}次状态未果,退出寻找')
                        c = False
                        self.send_keys('%{F4}')
                        self.connect_to_workwechat()
                        return False
            else:
                self.log.info('链接sop消息窗口失败')
                return False

    def delete_sop_1v1_task(self):
        '''
        删除最顶部的任务
        :return:
        '''
        if self.is_in_chat_list():
            while True:
                if self.up_to_find():
                    self.log.info('当前在最顶端,准备删除任务')
                    print(find_all_ui('任务类型1v1'))
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

        else:
            return False

    def click_sop_1v1_task(self):
        '''
        四个返回值
        关闭当前所有存在的点开sop之后的窗口,并点击窗口最上边一条1v1sop话术任务,如果打开了sop消息弹框,则返回True,
        否则返回 False,但是如果没有检测到消息,则返回字符串 stop ,表示当前没有可以执行的任务,delete:表示要删除当前任务
        :return:True False stop delete
        '''
        self.log.info('准备进入1v1sop任务框')
        if exists_ui('任务类型1v1') == False and self.is_in_chat_list():
            self.log.info('当前页面没有消息,没有任务可以做,停止任务')
            return 'stop'
        while True:
            if self.up_to_find() and self.check_for_extra_windows() and self.connect_to_workwechat() and exists_ui('任务类型1v1'):
                self.log.info('当前页面存在消息,准备做任务')
                while True:
                    self.log.info('点击sop话术任务')
                    self.connect_to_workwechat()
                    if touch(find_all_ui('任务类型1v1')[0]):
                        sleep(2)
                        if self.connect_to_special_panel('SOP消息'):
                            self.log.info('识别sop话术任务状态')
                            return self.get_sop_1v1_task_status()
                        else:
                            self.log.info('链接窗口失败')
                            # 这里可能是断网,现在是跳过
                            # 之后可以做ping百度的操作,如果ping不同就做一个程序意外停止的弹框
                            continue
                    else:
                        return False


    #这里是1对1话术任务处理的第二阶段,确定当前页面是否有可以执行的1v1sop话术任务,如果有就返回True,如果没有就返回False
    def do_sop1v1_task(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        while True:
            if self.is_in_chat_list():
                if self.click_sop_1v1_task() == True:
                    self.log.info('当前sop1v1话术任务处于未做状态')
                    self.connect_to_special_panel('SOP消息')
                    return True
                elif self.click_sop_1v1_task() == 'delete':
                    self.delete_sop_1v1_task()
                    continue
                elif self.click_sop_1v1_task() == 'stop':
                    self.log.info('当前无任务')
                    return 'stop'
                elif self.click_sop_1v1_task() == False:
                    self.log.info('操作出错,初始化,回到列表顶端')
                    self.is_in_chat_list()
                    self.up_to_find()
                    continue

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

    def scroll_the_tag_panel(self):
        '''
        scroll 1 page down in select tag panel.
        '''
        if not self.connect_to_desktop():
            return False
        if touch_ui('选择标签',y=35):
            self.log.info('\n\t —— Touch the Select tag text. ——')
            pos = find_ui('选择标签')[0]
            print(pos)
            for i in range(4):
                self.mouse_scroll(x=pos.get('result')[0],y=pos.get('result')[1]+35,wheel_dist=-1)
            return True
            # self.mouse_scroll()

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

        print(self.scroll_the_tag_panel())

        # while not self.search_target_tag():
        #     self.select_customer_tag()

        # while not self.send_message_to_customer():
        #     self.search_target_tag()

        # self.open_sending_helper()
        # self.select_the_customer()
        # self.select_customer_tag()
        # self.search_target_tag()
        # self.send_message_to_customer()
        # a = self.find_the_chat()  #--进入消息列表
        # a = self.click_luoshu_SMR_in_chat_list()
        # a = self.search_the_SMR()  #--搜索洛书SMR-test
        # a = self.is_in_chat_list()  #判断是否在洛书SMR-test聊天页
        # a = self.up_to_find()  #判断是否在洛书SMR-test聊天页的最顶端
        # a = self.check_for_extra_windows()  #检测多余窗口
        # a = self.click_sop_1v1_task()  #点击1v1sop话术消息
        # a = self.get_sop_1v1_task_status()  #判断当前1v1sop话术消息是否是的状态
        # self.check_for_extra_windows(title='洛书SMR-test')  #关掉独立聊天窗口
        # for i in range(10):
        #     a = self.delete_sop_1v1_task()   #删除最顶端任务
        a = self.do_sop1v1_task()

        print(a)

        # a = self.connect_to_special_panel('已回执')
        #
        # b = self.connect_to_special_panel('回执')
        #
        # print(a)
        # print(b)
        # self.connect_to_special_panel('SOP消息')
        # self.connect_to_desktop()
        # self.connect_to_special_panel('SOP消息')
        # self.connect_to_desktop()
        # print(exists_ui('已回执'))


        # self.test()
if __name__ == '__main__':
    task = EveryDayTask()
    task.run_task()

