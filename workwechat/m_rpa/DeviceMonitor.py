__author__ = "zyh"
import time
import win32gui
from datetime import datetime
from threading import Thread

from .base import Base
from .constants import *

class Monitor(Base):
    def __init__(self, log, obj_dict):
        super().__init__(log, obj_dict)
        self.check_interval = None
        self.message_interval = None
        self.error_occured = 0
        self.message_dict = {}
        self.log.info('\n\t### 执行器手动开启运作 ###')

    def get_interval_seconds(self):
        try:
            self.check_interval = self.get_config_info(key='monitor',value='monitor_interval')
            self.message_interval = self.get_config_info(key='monitor',value='message_interval')
        except Exception as e:
            self.log.error(f'\n\t### get monitor interval config error:{e}###')
            self.check_interval = 10
            self.message_interval = 10800

    def stop_monitor(self):
        '''
        企微监控
        '''
        try:
            try:
                now_activity_name = self.dev.get_top_activity_name()
                self.log.info(f'\n\t ### monitor running... now activity is:{now_activity_name} ###')       
            except Exception as e:
                self.error_occured += 1
                self.log.error(f'\n\t ### monitor running... activity get error:{e} ###')

            if self.poco(name=self.V['SKIP']).exists():     #首次使用的按钮监控
                self.poco(name=self.V['SKIP']).click()

            if self.poco(name='android:id/alertTitle',text='企业微信没有响应').exists():    # 无响应窗口
                self.poco(name='android:id/aerr_wait').click()
                self.send_dingding_msg(monitor_type='stop_monitor',msg='企业微信没有响应（已尝试点击等待）')

            if self.poco(name='android:id/message',text='企业微信无响应。要将其关闭吗？').exists():    # 无响应窗口2
                self.poco(name='android:id/button2',text='等待').click()
                self.send_dingding_msg(monitor_type='stop_monitor',msg='企业微信没有响应（已尝试点击等待）')

            if now_activity_name == 'com.tencent.wework/.login.controller.LoginWxAuthActivity':     # 账号异地登陆
                self.log.warning('### 企业微信账号已在其他手机登录（RPA模拟器端已下线 ###')
                self.send_dingding_msg(monitor_type='login_out',msg='企业微信账号已在其他手机登录（RPA模拟器端已下线）')

            self.error_occured = 0
        except Exception as e:
            self.error_occured += 1
            self.log.error(f'\n\t ### monitor Unresponsive error:{e} ###')
            self.send_dingding_msg(monitor_type='Unresponsive',msg=f'企业微信未响应检测线程出错(可能连接出错)\n Trace Back Error:{e}')

    def process_monitor(self):
        '''
        模拟器进程监控
        '''
        try:
            handlers = []
            win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
            time.sleep(0.1)
            for handler in handlers:
                title = win32gui.GetWindowText(handler)
                if self.hwin_title in title:
                    self.log.info(f'\n\t ### monitor running...&& simulator {self.hwin_title} is active ###')
                    return
            self.log.error(f'\n\t### monitor process not found! 模拟器宕机 ###')
            self.send_dingding_msg(monitor_type='process_monitor',msg='模拟器进程未检测到,模拟器宕机')
        except Exception as e:
            self.log.error(f'\n\t### monitor process check error:\n {e} ###')

    def solve_error(self):
        '''
        连续出错的处理
        '''
        if self.error_occured > 5:
            self.log.error(f'\n\t ### Wework is Unresponsive ###')
            self.send_dingding_msg(monitor_type='continuous_error',msg='企业微信连续监测到五次以上错误(已尝试重启)')
            try:
                self.dev.stop_app(WEWORK_PKG)
                time.sleep(2)
                self.dev.start_app(WEWORK_PKG)
            except:
                pass
            time.sleep(20)

    def monitor_test(self):
        '''for test'''
        self.get_interval_seconds()
        while True:
            self.process_monitor()      # 模拟器找不到
            self.stop_monitor()
            time.sleep(int(self.check_interval))
            self.solve_error()

    def send_dingding_msg(self, monitor_type, msg=''):
        '''
        钉钉警报发送
        param: monitor_type: 发送警报类型(同一类型的警报单独计算频率,默认3h才会发送下一次)
        '''
        send_time = self.message_dict.get(monitor_type,None)
        do_send = True
        if send_time:
            seconds = (datetime.now() - send_time).total_seconds()
            if int(seconds) < int(self.message_interval):
                do_send = False
        if do_send:
            self.alarm(msg=msg)
            self.message_dict[monitor_type] = datetime.now()

    def run(self):
        self.log.info('\n\t### 守护线程开始 ###')
        monitor = Thread(target=self.monitor_test)
        monitor.daemon = True
        monitor.start()