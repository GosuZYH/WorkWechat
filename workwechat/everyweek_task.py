# -*- encoding=utf8 -*-
import os
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

    def check_for_extra_windows(self,title=None):
        '''
        点击1v1任务之前确保无其他多余窗口存在
        有则杀死并返回True
        :return:
        '''
        try:
            while True:
                if title is None:
                    self.log.info('清除多余窗口')
                    for i in WINDOW_LIST:
                        while self.check_window_exists(title=i):
                            self.connect_to_special_panel(i)
                            self.log.info(f'检测到额外的窗口{i},将要关掉她')
                            self.send_keys('%{F4}')
                    self.log.info(f'检测完成')
                    return True
                else:
                    if self.check_window_exists(title=title):
                        self.connect_to_special_panel(title)
                        self.log.info(f'检测到额外的窗口{title},将要关掉她')
                        self.send_keys('%{F4}')
                        return True
                    else:
                        return True
        except Exception as e:
            self.log.error('清除多余窗口的过程中出错'+str(e))
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
                    return 'success'
                self.log.info('没有在消息列表中找到消息,停止任务')
                return 'stop'
            else:
                return False
        except Exception as e:
            self.log.info(f'判断当前页面是否是"客户联系"聊天页面的过程中出错:{e}')
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
                    if self.is_in_chat_list() == 'success':
                        print('当前消息页有消息')
                        return 'success'
                    elif self.is_in_chat_list() == 'stop':
                        return 'stop'
                    else:
                        continue
                else:
                    continue
        except Exception as e:
            self.log.info('到达消息最上方的过程中出错')
            return False

    def get_last_time_page(self):
        while True:
            if self.connect_to_special_panel('企业微信'):
                if exists_ui(r"every_week_task\昨天",threshold=0.9,rgb=True) or exists_ui(r"every_week_task\星期",threshold=0.9,rgb=True):
                    return True
                else:
                    keyevent('{PGUP}')
                    continue
                    # pass

    def click_chat_task(self,coordinates):
        '''
        点击聊天页任务
        coordinates:传入一个坐标(x,y)
        :return:
        '''
        try:
            while True:
                if touch(coordinates):
                    sleep(0.5)
                    if self.check_window_exists('发送企业消息'):
                        return True
                    else:
                        continue
                return False
        except Exception as e:
            self.log.error(f'\n\t点击任务出错{e}')
            return False

    def roll_mouse_pgup(self):
        try:
            while True:
                self.connect_to_special_panel('企业微信')
                self.connect_to_desktop()
                self.log.info('获取顶部y轴坐标')
                res1 = find_all_ui(r'every_week_task\客户联系')  #客户联系的y轴坐标
                self.log.info('获取元素坐标')
                res2 = find_all_ui(r'every_week_task\客户联系聊天页面消息箭头')
                list = []
                for i in res2:
                    list.append(i[1])
                res3 = min(list)-res1[0][1]
                self.log.info(f'最上边目标的y轴坐标为{min(list)},与顶部的坐标距离为{res3}')
                if 50 < res3 < 160:
                    self.log.info('最顶端的目标距离在50-150像素之间')
                    return True
                else:
                    self.log.info('最顶端的目标距离没有在50-150像素之间,向上滚动鼠标')
                    self.mouse_scroll(x=int(res1[0][0]), y=int(res1[0][1])+100, wheel_dist=1)
        except Exception as e:
            self.log.error(f'鼠标滑动过程中出错{e}')
            return False

    def roll_mouse_pgdn(self):
        try:
            while True:
                self.connect_to_special_panel('企业微信')
                self.connect_to_desktop()
                self.log.info('获取顶部y轴坐标')
                res1 = find_all_ui(r'every_week_task\客户联系')  #客户联系的y轴坐标
                self.log.info('获取元素坐标')
                res2 = find_all_ui(r'every_week_task\客户联系聊天页面消息箭头')
                # print(res2)
                if len(res2)<=3:
                    list = []
                    for i in res2:
                        list.append(i[1])
                    res3 = max(list)-res1[0][1]
                    self.log.info(f'顶部y轴坐标为{res1[0][1]},最下边目标的y轴坐标为{max(list)},与顶部的坐标距离为{res3}')
                    if 440 < res3 < 550:
                        self.log.info('最底端的目标距离在440-550像素之间')
                        self.connect_to_special_panel('企业微信')
                        return True
                    else:
                        self.log.info('最顶端的目标距离没有在50-150像素之间,向上滚动鼠标')
                        self.mouse_scroll(x=int(res1[0][0]), y=int(res1[0][1])+100, wheel_dist=-1)
                else:
                    self.log.info('当前页面有四个元素,向下滚动')
                    self.mouse_scroll(x=int(res1[0][0]), y=int(res1[0][1]) + 100, wheel_dist=-1)
                # else:
                #     #这里是将窗口调至最小的操作,还没做,需要的时候再说
                #     self.log.info('企微窗口过大,请放置最小')
                #     self.connect_to_special_panel('企业微信')
                #     snapshot(file_name=r'..\photos\every_week_task\企微窗口.png')
                #     self.connect_to_desktop()
                #     res = exists(Template(r'..\photos\every_week_task\企微窗口.png'))
                #     return 'max'

        except Exception as e:
            self.log.error(f'鼠标滑动过程中出错{e}')
            return False

    def get_chat_page_coordinates(self):
        '''
        获取当前页面的目标元素坐标
        返回一个列表:[(x1,y1),(x2,y2)]
        :return:
        '''
        try:
            if self.connect_to_special_panel('企业微信'):
                if self.roll_mouse_pgdn():
                    return find_all_ui(r'every_week_task\客户联系聊天页面消息箭头',reverse=True)
        except Exception as e:
            self.log.error(f'\n\t获取聊天页面目标坐标时出错{e}')
            return False

    def screenshot_of_contrast(self):
        self.connect_to_special_panel('企业微信')
        snapshot(filename='..\\photos\\test1.png')
        keyevent('{PGUP}')
        snapshot(filename='..\\photos\\test2.png')
        self.log.info('判断是否到最顶部')
        with open('photos\\test1.png', 'rb') as test1:
            res1 = test1.read()
        with open('photos\\test2.png', 'rb') as test2:
            res2 = test2.read()
        return res1 == res2

    def do_task(self):
        '''
        点击发送按钮,有就点击-退出,没有就直接退出
        :return:
        '''
        try:
            if self.connect_to_special_panel('发送企业消息'):
                if exists_ui(r'every_week_task\发送',rgb=True):
                    click = touch_ui(r'every_week_task\发送',rgb=True)
                    if click == True:
                        self.log.info('点击发送按钮')
                        sleep(0.3)
                        self.log.info('关闭窗口')
                        self.check_for_extra_windows(title='发送企业消息')
                        return 'send'
            self.log.info('关闭窗口')
            self.check_for_extra_windows(title='发送企业消息')
            return 'no_send'
        except Exception as e:
            self.log.error(f'处理任务的时候出错{e}')
            return False

    def do_every_week_task(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        try:
            c = True
            sum = 0
            while c:
                if sum == 0:
                    if self.third() == 'success':
                        if self.get_last_time_page():
                            while True:
                                if self.roll_mouse():
                                    coordinate = self.get_chat_page_coordinates()
                                    for i in coordinate:
                                        self.connect_to_special_panel('企业微信')
                                        self.click_chat_task((i[0]+100,i[1]))
                                        self.do_task()
                                        self.connect_to_special_panel('企业微信')
                                    snapshot(filename='..\\photos\\test1.png')
                                    keyevent('{PGDN}')
                                    snapshot(filename='..\\photos\\test2.png')
                                    self.log.info('判断是否到最底部')
                                    with open('photos\\test1.png', 'rb') as test1:
                                        res1 = test1.read()
                                    with open('photos\\test2.png', 'rb') as test2:
                                        res2 = test2.read()
                                    if res1 == res2:
                                        self.log.info('前后对比结果一致')
                                        sum+=1
                                        break
                    elif self.third() == 'stop':
                        return 'stop'
                else:
                    return 'stop'
        except Exception as e:
            self.log.info('做任务之前的任务出错'+str(e))
            return False

    def do_every_week_task1(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        try:
            if self.third() == 'success':
                keyevent('{END}')
                sum = 1
                while True:
                    if sum < 10:        # 连续出现10次已发送状态就判断为当前任务已经做完
                        if self.roll_mouse_pgdn():      # 鼠标调整合适位置
                            coordinates = self.get_chat_page_coordinates()
                            for i in coordinates:
                                '''
                                开始做当前页面的任务
                                '''
                                self.connect_to_special_panel('企业微信')
                                self.click_chat_task((i[0]+130,i[1]))  #这里x轴坐标向后
                                if self.do_task() == 'send':
                                    sum = 1  #点击发送成功将sum重新置为1
                                    # print('++++++++++++'+str(sum)+'++++++++++++++')
                                elif self.do_task() == 'no_send':
                                    sum+=1   #没有点击发送将sum+1当sum大于规定数字之后跳出任务
                                    # print('++++++++++++'+str(sum)+'++++++++++++++')
                            if self.screenshot_of_contrast():
                                self.log.info('停止任务,已经处理至最顶端的任务')
                                return 'stop'
                    else:
                        self.log.info(f'向上超过{sum}条任务都已经处理过,停止任务')
                        return 'stop'
            elif self.third() == 'stop':
                self.log.info('没有任务')
                return 'stop'
        except Exception as e:
            self.log.info('做任务之前的任务出错'+str(e))
            return False

    def test(self):
        '''
        test
        '''
        # a = self.do_every_week_task()
        a = self.do_every_week_task1()
        # a = self.is_in_chat_list()
        # a = self.first()
        # a = self.second()
        # a = self.third()
        # a = self.fourth()
        # a = self.fifth()
        # a = self.sixth()
        # a = self.get_last_time_page()
        # a = self.do_task()
        # a = self.roll_mouse_pgdn()
        # print(a)
        # self.connect_to_special_panel('企业微信')
        # snapshot(filename=r'企微窗口.png')
        # self.connect_to_desktop()
        # res = exists(Template(r'企微窗口.png'))
        # print(res)

        # a = self.get_chat_page_coordinates()
        # self.click_chat_task(a[0])
        # b = self.do_task()
        # b = a[1][1]-a[0][1]
        # c = a[2][1] - a[1][1]
        print(a)
        # print(b)
        # print(c)

    def run_task(self):
        '''
        '''

        res = self.test()

if __name__ == '__main__':
    task = EveryWeekTask()
    task.run_task()
    # task.connect_to_special_panel('企业微信')
    # touch_ui(r'every_week_task\聊天页空白处', y=-10)