# -*- encoding=utf8 -*-
from airtest.core.api import touch, swipe, text, sleep
from .base import Screen_dict
import configparser

from .base import Base
from .constants import WINDOW_LIST


class GroupSendingTask(Base):
    """
    群发企业消息给客户.
    """

    def __init__(self):
        super().__init__()
        self.if_news = False
        self.manager_panel = False
        self.touch_type = None
        self.sleep_time = 120
        self.x = None
        self.y = None

    def init_workwechat(self,is_direct_jump=False):
        """
        Do some init task.
        """
        try:
            self.kill_target_windows(target_title=WINDOW_LIST)
            self.connect_to_special_panel('企业微信')
            self.adjust_workwechat_window(is_direct_jump=is_direct_jump)
            self.log.debug('\n\t —— Init Workwechat Success! ——')
        except Exception as e:
            self.log.error(f'[启动微信 init_workwechat 出错] some error occured when init workwechat,detil info: \n\t *{e}')

    def adjust_workwechat_window(self, is_direct_jump=False):
        """
        Adjust the workwechat panel size to minimum .
        """
        h_0, w_0, top_left_x, top_left_y = 0, 0, 5, 5
        self.log.debug(f'\n\t —— 开始调整企微窗体大小及位置 ——')
        while True:
            # 为求稳妥，默认将窗体调整成正常状态下的最下尺寸
            hwin = self.connect_window_before_shot('企业微信')
            print('\t\t\t hwin.class_name() = ', hwin.class_name())

            h, w = hwin.client_rects()[0].right, hwin.client_rects()[0].bottom
            self.log.debug(f'\n\t —— 当前顶部窗口为{hwin.class_name()},大小为{h}x{w},屏幕缩放比例为{self.scale} ——')
            if hwin.class_name() == 'WeWorkWindow':
                self.move_window_to(hwin, top_left_x, top_left_y)
                x_distance = min(Screen_dict['wide'], 1000)
                y_distance = min(Screen_dict['high'], 1000)
                swipe((top_left_x, top_left_y), (top_left_x + x_distance, top_left_y + y_distance))
                h_0, w_0 = h, w
            elif hwin.class_name() == 'Tencent.WXWork.WediskHostWindow':
                return self.init_workwechat()
            else:
                self.log.warning(f'\n\t —— 当前有遮挡企微的其他窗口,尝试关闭 ——')
                self.send_keys('%{F4}')
                continue
            if is_direct_jump:
                break
            elif h_0 == h and w_0 == w:
                break
        self.x, self.y = h, w

    def check_task_status(self):
        """
        check if have new sending task.
        """
        self.if_news = False
        self.manager_panel = False
        self.touch_type = None
        while True:
            res = self.check_window_status()
            if res == 1:
                return
            elif res == 2:
                break
            elif res == 3:
                self.turn_to_group_sending_helper()
                self.log.debug("\n\t —— 7.open'待发送的企业消息'panel ——")
                if self.if_news:
                    self.log.debug('\n\t **当前已经点击了-负责人-坐标**')
                    touch((0.51 * self.x, 0.487 * self.y))
                    self.touch_type = 2
                    continue
                if not self.manager_panel:
                    self.log.debug('\n\t **当前已经点击了-非负责人-坐标**')
                    touch((0.51 * self.x, 0.455 * self.y))
                    self.touch_type = 1
                else:
                    self.log.debug('\n\t **当前已经点击了-负责人-坐标**')
                    touch((0.51 * self.x, 0.487 * self.y))
                    self.touch_type = 2
        self.do_sending_task()

    def check_window_status(self):
        """
        check if the target window have been openned,if exists,directly doing task.
        """
        hwin = self.connect_window_before_shot(title='企业微信')
        self.log.debug(f'\n\t —— 当前顶部窗口为{hwin.class_name()},大小为{hwin.client_rects()[0].right}x{hwin.client_rects()[0].bottom},屏幕缩放比例为{self.scale} ——')
        if hwin.class_name() == 'CrmGroupSendMsgTobeSentWindow':
            self.log.debug('\n\t **检测到当前已在待发送界面**')
            if self.touch_type == 1:
                self.manager_panel = False
            elif self.touch_type == 2:
                self.manager_panel = True
            return 2
        else:
            self.log.debug('\n\t **检测到当前不在待发送界面**')
            if self.touch_type == 1:
                self.if_news = True
            elif self.touch_type == 2:
                self.log.debug('\n\t **检测到当前没有新的待发消息**')
                return 1
            return 3

    def turn_to_group_sending_helper(self):
        """
        Open the group sending helper application.
        """
        try:
            self.log.debug("\n\t Start Open The GroupSending-Helper Now.. ——")
            self.log.debug("\n\t —— 1.click'工作台'button ——")
            touch((28 * self.scale, 252 * self.scale))
            self.log.debug("\n\t —— 2.click'工作台'text ——")
            touch((96 * self.scale, 28 * self.scale))
            self.log.debug("\n\t —— 3.click'搜索框' ——")
            touch((160 * self.scale, 70 * self.scale))
            self.log.debug("\n\t —— 4.clear'搜索框' ——")
            self.send_keys('{ENTER 2}')
            self.log.debug("\n\t —— 5.input'群发助手' ——")
            text('群发助手')
            self.log.debug("\n\t —— wait for 1 second ——")
            sleep(0.5)
            self.log.debug("\n\t —— 6.Keyboard for 'Enter' ——")
            self.send_keys('{ENTER}')
            return True
        except Exception as e:
            self.log.error(f'进入群发助手出错{e}')
            return False

    def do_sending_task(self):
        """
        开始做发送操作
        """
        error_time = 0
        while True:
            if error_time > 3:
                break
            hwin = self.loop_sending()
            try:
                if hwin.class_name() == 'ToastWindow':
                    self.log.debug(f'\n\t —— 当前顶部窗口为{hwin.class_name()},大小为{hwin.client_rects()[0].right}x{hwin.client_rects()[0].bottom},屏幕缩放比例为{self.scale} ——')
                else:
                    break
                error_time = 0
            except Exception as e:
                self.log.error(f'hwin error:{e}')
                error_time += 1
        self.log.debug('\n\t —— 检测到当前发送界面已无待发送消息！——')

    def loop_sending(self):
        self.connect_to_special_panel('企业微信')
        touch((0.488*self.x,0.357*self.y))
        # self.save_db_log()
        self.log.info(f'\n\t —— 已发送一次群发消息 ——')
        sleep(0.7)
        return self.connect_window_before_shot(title='企业微信')

    def end_workwechat(self):
        """
        task end.
        """
        self.log.debug('\n\t ***** Task End *****')
        try:
            self.kill_target_windows(target_title=WINDOW_LIST)
            if self.check_window_status() == 2:
                self.send_keys('%{F4}')
            # self.clear_photo()  #12.20暂时取消删除图片日志
        except Exception as e:
            self.log.error(f'[结束]{e}')

    def wait_time(self):
        """
        get wait time from db or set default.
        """
        config = configparser.ConfigParser()
        config.read('config/config.ini', encoding='utf-8')
        sleep_time = config.getint('time', 'waitTime')
        if not sleep_time:
            sleep_time = 120
        self.log.debug(f'\n\t —— Wait For {sleep_time} Seconds... ——')
        sleep(sleep_time)

    def pre_run(self):
        self.log.info('\n\t *** INITIATE PC RPA ***')
        self.init_workwechat()

    def run_task(self):
        self.log.info('\n\t *** START PC RPA ***')
        # self.init_workwechat(is_direct_jump=True)
        while True:
            try:
                self.dingtalk_robot(time=self.sleep_time)
            except Exception as e:
                self.log.error(f'some error occured when send dingtalk msg:{e}')
            self.kill_target_windows(target_title=WINDOW_LIST)
            self.check_task_status()
            self.end_workwechat()
            self.wait_time()
            self.connect_to_special_panel('企业微信')
