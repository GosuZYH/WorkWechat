# -*- encoding=utf8 -*-
from airtest.core.api import *
import logging
from PIL import Image
from init_airtest import AirConn
from photos import Base,exists_ui,touch_ui,find_ui,find_all_ui,shot,open_WXWork_window
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
        如果当前是消息页,就返回Trun
        如果无法做操作就返回False
        '''
        if open_WXWork_window():
            try:
                self.connect_to_workwechat()
                if exists_ui('消息1_1') and exists_ui('消息1'):
                    self.connect_to_workwechat()
                    logger.info('当前页面是消息页面')
                    return True
                elif exists_ui('消息2'):
                    logger.info('点击消息按钮')
                    touch_ui('消息2')
                    self.connect_to_workwechat()
                    logger.info('当前为消息列表页')
                    return True
            except Exception as e:
                logger.error('进入消息列表页出错'+str(e))
                return False
        else:
            return False

    def search_the_SMR(self,str='洛书SMR-test'):
        '''
        search the str in chat-list.
        return Ture:已找到 False:未找到
        '''
        if self.connect_to_workwechat():
            pass
        else:
            self.find_the_chat()

        if self.find_the_chat() and exists_ui('洛书SMR-test聊天窗口'):
            '''
            判断当前聊天页面是否是洛书SMR-test页面
            如果是,直接返回True
            不是继续往下走
            '''
            try:
                self.connect_to_workwechat()
                logger.info('鼠标点击聊天记录页面')
                touch_ui('聊天页笑脸', y=-10)
                return True
            except Exception as e:
                logger.error('搜索洛书SMR-test之后没有连接到企微窗口或没有有点击到聊天页面')
                if self.find_the_chat():
                    return True
                else:
                    return False
        if self.find_the_chat():
            '''
            判断是否在消息列表页
            如果在就进行搜索操作
            '''
            self.connect_to_workwechat()
            if exists_ui('搜索框'):
                logger.info('点击放大镜')
                touch_ui('搜索框放大镜')
            if exists_ui('搜索框取消'):
                logger.info('检测到搜索框中有文字,点击清空搜索框')
                touch_ui('搜索框取消')
            sleep(0.2)
            logger.info('input "洛书SMR-test"')
            text(str)
            if exists_ui('查询结果-洛书'):
                logger.info('LuoShu-SMP mini program has been found and is ready to click on it')
                touch_ui('查询结果-洛书')
                try:
                    self.connect_to_workwechat()
                    logger.info('鼠标点击聊天记录页面')
                    touch_ui('聊天页笑脸', y=-10)
                    return True
                except Exception as e:
                    logger.error('搜索洛书SMR-test之后没有连接到企微窗口或没有有点击到聊天页面')
                    return False
            else:
                logger.error('can not find the LuoShu-SMR mini-program')
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
            if self.search_the_SMR():
                try:
                    self.connect_to_workwechat()
                    touch_ui('聊天页笑脸', y=-10)
                    return True
                except Exception as e:
                    logger.error('判断是否链接企微窗口或点击聊天页面的过程中出错'+str(e))
                    return False
            else:
                return False

    def up_to_find(self):
        '''
        Scroll up on the message page
        如果两次截图的结果相等,则返回Turn 否则返回False
        :return:
        '''
        if self.connect_to_workwechat():
            pass
        else:
            self.find_the_chat()
        if self.is_in_chat_list():
            try:
                logger.info('消息页置顶任务--开始做消息页置顶任务')
                logger.info('消息页置顶任务--开始连接企微窗口')
                self.connect_to_workwechat()
            except Exception as e:
                logger.error('消息页置顶任务--连接企微窗口失败'+str(e))
                return False
            try:
                logger.info('消息页置顶任务--鼠标点击聊天记录页面')
                touch_ui('聊天页笑脸', y=-10)
            except Exception as e:
                logger.error('消息页置顶任务--点击聊天页面出错'+str(e))
                return False
            while True:
                logger.info('开始判断是否是消息列表最顶端')
                logger.info('消息页置顶任务--开始连接企微窗口')
                self.connect_to_workwechat()
                logger.info('消息页置顶任务--鼠标点击聊天记录页面')
                touch_ui('聊天页笑脸', y=-10)
                try:
                    logger.info('消息页置顶任务--准备在翻页前后截图做对比')
                    snapshot(filename='test1.png')
                    keyevent('{PGUP 5}')
                    snapshot(filename='test2.png')
                except Exception as e:
                    logger.error('消息页置顶任务--执行截图或翻页时出错')
                    return False
                try:
                    logger.debug('消息页置顶任务--开始比对前后截图')
                    with open('log\\test1.png', 'rb') as test1:
                        res1 = test1.read()
                    with open('log\\test2.png', 'rb') as test2:
                        res2 = test2.read()
                except Exception as e:
                    logger.error('消息页置顶任务--对比翻页前后截图出错')
                    return False
                if self.is_in_chat_list() and res1 ==res2:
                    try:
                        self.connect_to_workwechat()
                        touch_ui('聊天页笑脸', y=-10)
                        return True
                    except Exception as e:
                        logger.error('判断是否链接企微窗口或点击聊天页面的过程中出错')
                        return False
        else:
            return False

    def message_page_at_the_top(self,num=10):
        '''
        判断当前是否在消息的最顶端,如果是就返回Ture
        num 传入一个int类型,表示判断当前页面就是置顶页面的次数
        '''
        if type(num) is int:
            pass
        else:
            logger.error('传入的参数非int类型')
            return False
        flag_list = []#定义一个空列表用来存放最后对比的所有结果
        c = True
        if self.up_to_find():
            while c:
                for i in range(num):
                    try:
                        logger.info(f'重复确认{num}次是否是消息最顶端')
                        logger.info('消息页置顶任务--开始连接企微窗口')
                        self.connect_to_workwechat()
                        logger.info('消息页置顶任务--鼠标点击聊天记录页面')
                        touch_ui('聊天页笑脸', y=-10)
                    except Exception as e:
                        logger.info('企微窗口未找到,跳出for循环')
                        break

                    try:
                        logger.info('消息页置顶任务--准备在翻页前后截图做对比')
                        snapshot(filename='test1.png')
                        keyevent('{PGUP}')
                        snapshot(filename='test2.png')
                        with open('log\\test1.png', 'rb') as test1:
                            res1 = test1.read()
                        with open('log\\test2.png', 'rb') as test2:
                            res2 = test2.read()
                            flag_list.append(res1 == res2)
                    except Exception as e:
                        logger.error('消息页置顶任务--确实当时是否为消息列表置顶时,截图对比出错'+str(e))
                        return False


                if all(flag_list) == True:
                    try:

                        logger.info('确认当前为最上边消息,并尝试连接企微窗口')
                        self.connect_to_workwechat()
                        logger.info('尝试用鼠标点击聊天记录页面')
                        touch_ui('聊天页笑脸', y=-10)
                        logger.info('确认当前企微页面没有被关闭,并且可以点击聊天页面,可以返回True')
                        return self.is_in_chat_list()
                    except Exception as e:
                        logger.error('返回True之前乜有连接到企微窗口或没有点击到聊天页面'+str(e))
                        return False
                c = self.is_in_chat_list()
        else:
            return False





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
        # self.connect_to_select_custom_panel()
        # self.connect_to_desktop()
        # touch_ui('全选客户',x=-25)
        self.connect_to_workwechat()
        sleep(3)
        shot('当前截屏')
        image = aircv.imread(filename='F:\\git\\WorkWechat\\test.air\\photos\\当前截屏.png')
        local = aircv.crop_image(image,(132,58,380,126))
        show_origin_size(local)
        touch(local)


    def run_task(self):
        '''
        '''

        # a = self.find_the_chat()  #--进入消息列表
        # a = self.search_the_SMR()  #--搜索洛书SMR-test
        # a = self.is_in_chat_list()  #判断是否在洛书SMR-test聊天页
        a = self.up_to_find()  #判断是否在洛书SMR-test聊天页的最顶端
        print(a)


        # print(self.message_page_at_the_top())
        # self.test()



task = EveryDayTask()
task.run_task()
