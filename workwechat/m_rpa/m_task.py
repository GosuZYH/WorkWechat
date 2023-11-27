# -*- encoding=utf8 -*-
import datetime
from time import sleep

from airtest.core import api as air_api

from .base import Base
from .SopFriendCricle import Sop
from .ClientFriendCircle import ClientFriendCircle
from .GroupSend import GroupSend
from .DeviceMonitor import Monitor


class MRPAtask(Base):

    def __init__(self):
        self.init_ui()
        self.init_db()
        super().__init__()

    def task_loop(self):
        '''ClientFriendCircle
        loop doing task.
        '''
        self.count = 0
        task1 = GroupSend(self.log,self.obj_dict)
        task2 = ClientFriendCircle(self.log,self.obj_dict)
        task3 = Sop(self.log,self.obj_dict)
        while True:
            start_time = datetime.datetime.now()
            try:
                self.log.info(f'\n\t —— Start task-1 —— ')
                task1.run()
            except Exception as e:
                self.log.warn(f'\n\t —— task-1 occured error:{e} —— ')
            try:
                self.log.info(f'\n\t —— Start task-2 —— ')
                task2.run()
            except Exception as e:
                self.log.warn(f'\n\t —— task-2 occured error:{e} —— ')
            try:
                self.log.info(f'\n\t —— Start task-3 —— ')
                task3.run()
            except Exception as e:
                self.log.warn(f'\n\t —— task-3 occured error:{e} —— ')
            try:
                self.clear_wework_cache()
                self.task_statistics(start_time=start_time)
            except Exception as e:
                self.log.error(f'\n\t —— 主任务之外的错误:{e} —— ')

    def first_task(self):
        if self.V is None:
            self.V = self.get_version()
            self.obj_dict['V'] = self.V
        if self.timeout is None:
            self.timeout = self.get_timeout_config()
            self.obj_dict['timeout'] = self.timeout
        if self.user_name is None:
            self.user_name = self.get_user_name()
            self.obj_dict['user_name'] = self.user_name

    def task_statistics(self,start_time):
        '''
        statistic task speed.
        '''
        self.count += 1
        self.log.info(f'执行第{self.count}轮任务')
        end_time = datetime.datetime.now()
        res_time = datetime.datetime.strptime(str(end_time - start_time)[:-7], '%H:%M:%S')
        date = datetime.datetime.strptime('0:00:40', '%H:%M:%S')
        if res_time < date and self.count % 1500 == 0 and self.count != 0 :
            self.alarm(msg=f'当前设备已断开连接/宕机')
            self.log.error(f'发现每轮任务执行的时间为{str(res_time)[-8:]}过快,请检查手机执行情况,每个任务已经循环了{self.count}轮')
    
    def run(self, *args, **kwargs):
        try:
            self.first_task()
        except Exception as e:
            self.log.error(f'\n\t —— 获取用户名和配置项时出现错误:{e} —— ')
        M = Monitor(self.log,self.obj_dict)
        M.run()
        self.task_loop()

    def run_special(self):
        task2 = ClientFriendCircle(self.log,self.obj_dict)
        task2.init_wework()
        self.log.info(f'\n\t —— Start task-2 ——')
        task2.run()

    def run_swipe(self):
        air_api.swipe([self.x * 0.5, self.y * 0.80], [self.x * 0.5, self.y * 0.15], duration=0.6, steps=8)
        print(1111)
        self.run_special()

if __name__ == "__main__":
    r = MRPAtask()
    r.run()
