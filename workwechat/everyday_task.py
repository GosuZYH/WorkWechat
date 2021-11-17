# -*- encoding=utf8 -*-
import poco
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
            self.log.error('\n\tfirst函数执行出错'+str(e))
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
            self.log.error(e)
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
            text(str, search=True)
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
        except Exception as e:
            self.log.error('\n\t搜索"洛书SMR-test过程中出错"'+str(e))
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
            self.log.error('\n\tsecond函数出错'+str(e))
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
            self.log.error('判断当前页面是否是与洛书SMR-test聊天页面的过程中出错')
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
            self.log.error('到达消息最上方的过程中出错'+str(e))
            return False

    def get_sop_1v1_task_status(self):
        '''
        判断sop执行状态
        未执行返回True
        已执行返回delete
        报错返回False
        :return:
        '''
        try:
            count = 1
            while True:
                if self.H5_page_get_element(title='回执'):
                    self.log.info('\n\t当前sop1v1任务为可执行状态')
                    self.connect_to_special_panel('SOP消息')
                    return True
                elif self.H5_page_get_element(title='已回执'):
                    self.log.info('\n\t当前sop1v1任务为不可执行状态')
                    self.connect_to_special_panel('SOP消息')
                    self.log.info('\n\t关闭SOP消息页面')
                    self.send_keys('%{F4}')
                    return 'delete'
                else:
                    count+=1
                    sleep(2)
                    if count <=2:
                        self.log.info(f'\n\t获取任务状态失败尝试第{count}次寻找')
                        continue
                    else:
                        self.log.info(f'\n\t第{count}次获取任务状态失败退出')
                        return False
        except Exception as e:
            self.log.error('获取sop1v1任务状态的过程中出错'+str(e))
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
            self.log.error('删除任务的过程中出错'+str(e))
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
            self.log.error('点击聊天页面最顶端元素的过程中出错')
            return False

    def fourth(self):
        try:

            while True:
                # self.check_for_extra_windows()
                if self.third() == True:
                    # self.check_for_extra_windows()
                    if self.click_sop_1v1_task() == True:
                        if self.get_sop_1v1_task_status() == 'delete':
                            self.log.info('检测到当前任务已经做好,删除它')
                            if self.delete_sop_1v1_task():
                                self.log.info('删除已执行消息消息')
                                continue
                        elif self.get_sop_1v1_task_status() == True:
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
            self.log.error(''+str(e))
            return False

    def copy_sop_tag(self):
        '''
        every day 1V1 sending.
        * base on having openned the customer-sop.
        '''
        # if self.check_window_exists(title='SOP消息'):
        #     self.log.info('\n\t —— Target panel exists. ——')
        #     if self.connect_to_special_panel(title='SOP消息'):
        #         if touch_ui('点击复制2'):
        #             sleep(0.2)
        #             win32clipboard.OpenClipboard()
        #             copy_tag= win32clipboard.GetClipboardData()
        #             self.copy_tag = copy_tag.replace('_', ' ')
        #             win32clipboard.CloseClipboard()
        #             sleep(0.5)
        #             return True
        #         self.log.error('\n\t *** can not find the click-copy button! ***')
        # return False
        try:
            if self.connect_to_special_panel('SOP消息'):
                if self.H5_page_get_element(title='点击复制',click=True):
                    self.log.info('\n\t点击复制')
                    if self.connect_to_special_panel('SOP消息'):
                        return True
                    self.log.info('\n\t点击复制完链接窗口失败')
                    return False
                self.log.info('\n\t点击复制失败')
                return False
            self.log.info('\n\t点击复制前链接"SOP消息"窗口失败')
            return False
        except Exception as e:
            self.log.error('\n\t做点击复制的时候出错')

    def click_group_sending_helper(self):
        '''
        click the turn-to-sending-helper button
        '''
        # if self.check_window_exists(title='SOP消息'):
        #     self.log.info('\n\t —— Target panel exists. ——')
        #     if self.connect_to_special_panel(title='SOP消息'):
        #         if touch_ui('跳转到群发助手'):
        #             self.log.info('\n\t —— touch the sending-helper button ——')
        #             sleep(0.3)
        #             return True
        #         self.log.error('\n\t *** can not find the group sending helper! ***')
        # return False
        try:
            if self.connect_to_special_panel('SOP消息'):
                self.log.info('\n\t点击"跳转到群发助手"')
                if self.H5_page_get_element(title='跳转到群发助手',type='Button', click=True):
                    sleep(1)
                    self.log.info('\n\t链接"向我的客户发消息"窗口')
                    if self.connect_to_special_panel('向我的客户发消息'):
                        return True
                    self.log.info('\n\t点击"跳转到群发助手"完链接窗口失败')
                    return False
                self.log.info('\n\t点击"跳转到群发助手"失败')
                return False
            self.log.info('\n\t点击"跳转到群发助手"前链接"SOP消息"窗口失败')
            return False
        except Exception as e:
            self.log.error('\n\t做点击"跳转到群发助手"的时候出错'+str(e))

    def fifth(self):
        '''
        点击跳转 到群发助手
        :return:
        '''
        # if self.swip_sop1v1_windows():
        try:
            count=1
            while True:
                if count<=2:
                    if self.copy_sop_tag():
                        if self.click_group_sending_helper():
                            return True
                        else:
                            count+=1.
                            sleep(2)
                            self.log.info(f'\n\t第{count}次尝试去"向我的客户发消息页"')
                            continue
                    else:
                        count += 1
                        self.log.info(f'\n\t第{count}次尝试去"向我的客户发消息页"')
                        continue
                else:
                    self.log.info(f'\n\t{count}次尝试去"向我的客户发消息页失败,退出当前步骤"')
                    return False
        except Exception as e:
            self.log.error('\n\t执行第五个组合的时候出错'+str(e))
            return False

    def select_the_customer(self):
        '''
        after open the sending helper,select the customer tag.
        '''
        try:
            while self.check_window_exists(title='提示'):
                '''
                存在'提示'窗口,关掉它
                '''
                if self.connect_to_special_panel(title='提示'):
                    if exists_ui('新建'):
                        self.check_for_extra_windows(title='提示')

            while self.check_window_exists(title='选择客户'):
                '''
                存在'选择客户'窗口,关掉它
                '''
                if self.connect_to_special_panel(title='选择客户'):
                    if exists_ui('选择标签'):
                        self.check_for_extra_windows(title='选择客户')
            if self.check_window_exists(title='向我的客户发消息'):
                self.log.info('\n\t —— Target panel exists. ——')
                if self.connect_to_special_panel(title='向我的客户发消息'):
                    if touch_ui('选择客户'):
                        sleep(0.5)
                        self.log.info('\n\t —— touch the select customer button ——')
                        return True
                    self.log.error('\n\t *** can not find select customer button! ***')
            return False
        except Exception as e:
            self.log.error('\n\t页面"向我的客户发消息"操作出错'+str(e))
            return False

    def sixth(self):
        '''
        直达选择客户页面,中间出错就会返回上一步
        :return:
        '''
        try:
            count = 1
            while True:
                if count <= 2:
                    if self.fifth():
                        if self.select_the_customer():
                            return True
                        else:
                            count += 1
                            self.log.info(f'\n\t第{count}次尝试第6个组合')
                            sleep(2)
                            continue
                    else:
                        self.log.info(f'\n\t组合五出错,返回False')
                        return False
                else:
                    self.log.info(f'\n\t第{count}次尝试第6个组合错误,返回上一步')
                    return False

        except Exception as e:
            self.log.error('\n\t第六个组合执行出错')

    def select_customer_tag(self):
        '''
        select the customer tags.
        '''
        try:
            if self.check_window_exists(title='选择客户'):
                self.log.info('\n\t —— Target panel exists. ——')
                if exists_ui('选择标签'):
                    self.connect_to_special_panel('选择客户')
                    return True
                if self.connect_to_special_panel(title='选择客户'):
                    if touch_ui('不限标签'):
                        sleep(0.5)
                        self.log.info('\n\t —— touch the tag mini-menu ——')
                        return True
                    self.log.info('\n\t *** can not find select tag mini-menu! ***')
                    return False
                self.log.info('\n\t链接"选择客户"窗口时出错')
                return False
            self.log.info('\n\t"选择客户"窗口不存在')
            return False
        except Exception as e:
            self.log.error('\n\t点击选择标签的过程中出错'+str(e))
            return False

    def search_target_tag(self):
        '''
        search target customer tag from the list.
        '''
        try:
            while True:
                if not self.check_window_exists(title='选择客户'):
                    self.log.error('\n\t链接选择客户窗口的过程中出错')
                    return False
                self.connect_to_special_panel('选择客户')
                self.connect_to_desktop()
                pos = self.get_target_tag_position()
                # print('这是pos的结果'+type(pos))
                if pos:
                    self.log.info('\n\t —— Find target! Touch the Target tag. ——')
                    touch(pos)
                    sleep(0.5)
                    return True
                else:
                    shot('test1')
                    sleep(0.3)
                    self.log.info('\n\t —— can not find target tag in this page. ——')
                    self.connect_to_special_panel('选择客户')
                    if self.scroll_the_tag_panel():
                        sleep(0.3)
                        shot('test2')
                        with open('photos\\test1.png', 'rb') as test1:
                            res1 = test1.read()
                        with open('photos\\test2.png', 'rb') as test2:
                            res2 = test2.read()
                        sleep(0.3)
                        if res1 == res2:
                            self.log.info('\n\t没有找到符合的标签,准备返回删除')
                            if exists_ui('选择标签页'):
                                return 'delete'
                            self.log.info('\n\t对比结果之后发现当前没有选择标签页,重新对比')
                            continue
                        self.log.info('两次对比图片不一致,返回')
                        continue
                    self.log.info('\n\t鼠标滚轮出现问题')
                    return False
        except Exception as e:
            self.log.error('\n\t翻找标签页的过程中出错'+str(e))
            return False

    def seventh(self):
        try:
            count=1
            while True:
                if count<=2:
                    if self.select_customer_tag():
                        if self.search_target_tag() == True:
                            return True
                        elif self.search_target_tag() == 'delete':
                            return 'delete'
                        elif self.search_target_tag() == False:
                            count+=1
                            self.log.info(f'第七个组合尝试第{count}次')
                            sleep(2)
                            continue
                    return False
                else:
                    self.log.info(f'第七个组合尝试第{count}次失败,返回上一步')
                    return False
        except Exception as e:
            self.log.error('\n\t执行第七个组合的过程中出错'+str(e))
            return False

    def eighth(self):
        try:
            count=1
            while True:
                if count<=2:
                    if self.sixth():
                        if self.seventh() == True:
                            if self.select_all_customer():
                                if self.send_message_to_customer():
                                    if self.click_finish():
                                        return True
                                    count += 1
                                    sleep(2)
                                    continue
                                count += 1
                                sleep(2)
                                continue
                            sleep(2)
                            count += 1
                            continue
                        elif self.seventh() == 'delete':
                            return 'delete'
                        count+=1
                        sleep(2)
                        continue
                    return False
                return False
        except Exception as e:
            self.log.error('\n\t第八个组合出错'+str(e))

    def select_all_customer(self):
        '''
        select all customer.
        '''

        try:
            if self.connect_to_special_panel('选择客户'):
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
            else:
                return False
        except Exception as e:
            self.log.error('\n\t选择客户页面点击全选的过程中出错'+str(e))
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
                    if self.connect_to_special_panel('消息发送确认'):
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
        try:
            if self.connect_to_special_panel('选择客户'):
                if self.connect_to_desktop():
                    if  find_all_ui('选择标签'):
                        pos = find_all_ui('选择标签')[0]
                        print(pos)
                        for i in range(4):
                            self.mouse_scroll(x=pos[0],y=pos[1]+100,wheel_dist=-1)
                            self.mouse_scroll(x=0,y=0,wheel_dist=-1)
                            sleep(0.1)
                        if self.connect_to_special_panel('选择客户'):
                            self.log.info('\n\t鼠标滚动完成')
                            return True
                        else:
                            self.log.info('\n\t鼠标滚动完成,但是没有找到"选择客户的页面"')
                            return False
                    self.log.info('\n\t没有找到选择标签元素')
                    return False
                self.log.info('\n\t链接桌面失败')
                return False
            self.log.info('\n\t链接"选择客户页面失败"')
            return False
        except Exception as e:
            self.log.error('\n\t鼠标滚轮出错'+str(e))
            return False

    def click_finish(self):
        '''
        点击SOP消息页面的回执按钮
        :return:
        '''
        try:
            self.connect_to_special_panel('SOP消息')
            if self.H5_page_get_element(click=True):
                if self.connect_to_special_panel('SOP消息'):
                    self.send_keys('%{F4}')
                    return True
                return True
            elif self.H5_page_get_element(title='已回执'):
                if self.connect_to_special_panel('SOP消息'):
                    self.send_keys('%{F4}')
                    return True
                return True
            else:
                return False
        except Exception as e:
            self.log.error('\n\t点击回执按钮出错'+str(e))
            return False

    def execute_sop_task(self):

        while not self.copy_sop_tag():
            sleep(1)

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
                                    return True


        while not self.select_all_customer():
            self.search_target_tag()

        while not self.send_message_to_customer():
            self.select_all_customer()

        while not self.send_message_to_customer():
            if self.click_finish():
                return True

    def protect_workchat(self):
        while True:
            if self.check_window_exists('企业微信') == False:
                if self.get_WXWork_pid() == True:
                    self.start_WXWork()
                    sleep(2)
                    return True
                self.connect_to_special_panel('企业微信')
                return True


    def do_sop1v1_task(self):
        '''
        True:继续做任务
        stop:没有任务可以做
        :return:
        '''
        try:

            while True:
                if self.connect_to_workwechat():
                    if self.fourth() == True:
                        '''
                        这里开始做后续的任务
                        如果做完了任务,要将状态变为已执行
                        如果没有点击已执行:
                            可以直接调:self.delete_sop_1v1_task() -->删除最顶端的任务
                            之后无论返回什么:都continue跳过当前循环就好
                        '''
                        if self.eighth() == True:
                            if self.delete_sop_1v1_task():
                                continue
                        elif self.eighth() == 'delete':
                            if self.delete_sop_1v1_task():
                                continue
                        else:
                            continue
                    elif self.fourth() == 'stop':
                        return 'stop'
                    else:
                        return False
                else:
                    continue
        except Exception as e:
            self.log.info('做任务之前的任务出错' + str(e))
            return False

    def test(self):
        '''
        test
        '''
        # while True:
        # self.copy_sop_tag()
        #         print(1)
        #     else:
        #         break
        # print('跳出了循环')
        #
        # while not self.copy_sop_tag():
        #     sleep(1)
        #
        # while not self.click_group_sending_helper():
        #     self.copy_sop_tag()
        #
        # while not self.select_the_customer():
        #     self.click_group_sending_helper()
        #
        # while not self.select_customer_tag():
        #     self.select_the_customer()
        #
        # while not self.sixth():
        #     sleep(1)
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
        #
        # while not self.select_all_customer():
        #     self.search_target_tag()
        #
        # while not self.send_message_to_customer():
        #     self.select_all_customer()
        # 联调测试洛书
        # a = self.do_sop1v1_task()
        # print(a)
        # a = self.first()
        # a = self.second()
        # a = self.third()
        # a = self.fourth()
        # a = self.fifth()
        # a = self.sixth()
        # a = self.seventh()
        # a = self.eighth()
        ## 点击消息
        # a = self.find_the_chat()
        # print(a)

        ## 在列表中点击目标
        # a = self.click_luoshu_SMR_in_chat_list()
        # print(a)

        ## 搜索目标
        # a = self.search_the_SMR()
        # print(a)

        ## 对比截图
        # a = self.screenshot_of_contrast()
        # print(a)

        ## 是否在聊天页中
        # a = self.is_in_chat_list()
        # print(a)

        ## 检测并清除多余窗口,title为空时,检查content中列出的所有窗口,title值不空时,只检测title的窗口
        # a = self.check_for_extra_windows()
        # print(a)

        ## 获取sop1v1任务的状态,未做的返回True  已经做的返回 'delete'  没有任务返回  'stop'
        # a = self.get_sop_1v1_task_status()
        # print(a)

        ##删除最顶部的消息,删除成功返回True
        # a = self.delete_sop_1v1_task()

        ## 点击复制
        # a = self.copy_sop_tag()
        # print(a)

        # 点击跳转群发助手
        # a = self.click_group_sending_helper()
        # print(a)

        ## 在向我的客户发消息页面点击选择客户
        # a = self.select_the_customer()
        # print(a)

        # 在选择客户页面点击不限标签
        # a = self.select_customer_tag()
        # print(a)

        # ## 开始在下拉菜单中寻找目标
        # a = self.search_target_tag()
        # print(a)

        # 在选择客户页面点击全选并点击确认
        # a = self.select_all_customer()
        # print(a)

        # 点击发送确认
        # a = self.send_message_to_customer()
        # print(a)

        #鼠标混轮在选择标签页滚动
        # a = self.scroll_the_tag_panel()
        # print(a)

        #做完任务点击回执按钮
        # a = self.click_finish()
        # print(a)

        # a = self.protect_workchat()
        # print(a)

        # a = self.scroll_the_tag_panel()

        # a = self.select_customer_tag()
        # a = self.search_target_tag()
        # a = self.click_finish()
        # self.connect_to_special_panel('企业微信')
        # try:
        #     touch((2632,483))
        # except:洛书SMR-test
        #     sleep(20)
        # print(a)
        # self.connect_to_special_panel('企业微信')
        # print(exists_ui('选择标签'))



    def run_task(self):
        '''
        '''

        res = self.test()

if __name__ == '__main__':
    task = EveryDayTask()
    task.run_task()