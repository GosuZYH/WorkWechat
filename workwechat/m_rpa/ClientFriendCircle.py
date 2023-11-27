# -*- encoding=utf8 -*-
__author__ = "cyx"
from datetime import datetime, timedelta

from airtest.core import api as air_api

from .base import Base
from .constants import *


class ClientFriendCircle(Base):
    def __init__(self, log, obj_dict):
        super().__init__(log, obj_dict)
        self.time_gap, self.time_flag = self.get_config_time()

    def init_attributes(self):
        self.start_time = datetime.now()
        self.task_num = 0
        self.error_times = 0

    def get_config_time(self):
        try:
            customerfriendcircledaygap = self.get_config_info('stop sending time', 'customerfriendcircledaygap')
            customerfriendcircletime = self.get_config_info('stop sending time', 'customerfriendcircletime')
            if '：' in customerfriendcircletime:
                customerfriendcircletime = customerfriendcircletime.replace('：', ':')
        except:
            customerfriendcircledaygap = 1
            customerfriendcircletime = '22:00'
            self.log.warning('\n\t —— config-customerfriendcircle时间未配置 —— ')
            self.alarm('', f'配置当中缺少customerfriendcircle时间配置')
        if not customerfriendcircledaygap.isdigit() or ':' not in customerfriendcircletime:
            customerfriendcircledaygap = 1
            customerfriendcircletime = '22:00'
            self.log.warning('\n\t —— config-customerfriendcircle时间格式配置错误 —— ')
            self.alarm('', f'配置customerfriendcircle时间格式错误')
        return int(customerfriendcircledaygap), customerfriendcircletime

    def ctrl_operate(self, ctrl_obj, op_type='click', msg=""):
        # noinspection PyBroadException
        try:
            self.log.info(f"\n\t —— 开始 “{msg}” 任务 —— ")
            ctrl_obj.wait_for_appearance(timeout=self.timeout*3)
            if op_type == 'click':
                self.log.info(f"\n\t —— 点击{msg} —— ")
                ctrl_obj.click()
        except Exception as e:
            self.error_times += 1
            self.log.info(f"\n\t —— 客户朋友圈任务出错:{e},当前出错{self.error_times}次 —— ")
            self.run()

    def swipe_up_click(self):
        try:
            self.check_every_task()
            air_api.swipe([self.x * 0.5, self.y * 0.750], [self.x * 0.5, self.y * 0.2], duration=0.6, steps=8)
            self.all_task_judge()
        except Exception as e:
            self.log.info(f"\n\t —— 处理任务时出错:{e} —— ")
            self.num_all_ctrl_already_sends += 4

    def no_task_judge(self):
        try:
            self.poco(name=self.V['NO_CUSTOMER_PYQ'], text='可在这里接收企业的待发表任务等通知').wait_for_appearance(timeout=self.timeout*2)
            self.log.info("\n\t —— 当前界面没有任何客户朋友圈 —— ")
            return False
        except:
            return True

    def check_every_task(self):
        can_not_send = self.poco(text='查看完整指标')
        cancel = self.poco(text='取消')
        send_panel = self.poco(name=self.V['COMPANY_TASK'])
        for child in send_panel.child():
            if len(child.child().child()) > 2:
                ui_time = child.offspring(name=self.V['COMPANY_TASK_TIME'])
                if ui_time.exists():
                    tasktime = self.time_judge(task_time=ui_time.get_text())
                    if not tasktime:
                        self.num_all_ctrl_already_sends += 4
                    else:
                        ui_publish = child.offspring(name=self.V['PUBLISH_1'], text='发表')
                        if ui_publish.exists():
                            self.log.info(f'\n\t —— 当前页面的企业朋友圈任务时间为{tasktime},可发表 —— ')
                            ui_publish.click()
                            self.num_all_ctrl_already_sends = 0
                            if len(can_not_send) > 0:
                                cancel.click()
                                self.log.info("\n\t —— 发现无法发表更多客户朋友圈（指标影响） —— ")
                                self.num_all_ctrl_already_sends += 4
                            self.task_num += 1
                        else:
                            self.log.info(f'\n\t —— 当前页面的企业朋友圈任务时间为{tasktime},已发表 —— ')

    def all_task_judge(self):
        ctrl_already_sends = self.poco(name=self.V['PUBLISH_1'], text='已发表')
        ctrl_pre_sends = self.poco(name=self.V['PUBLISH_1'], text='发表')
        if len(ctrl_already_sends) > 0 and len(ctrl_pre_sends) == 0:
            self.log.info(f'\n\t —— 当前页面的企业朋友圈均已发表,num_all_ctrl_already_sends+1 —— ')
            self.num_all_ctrl_already_sends += 1
        elif len(ctrl_already_sends) == 0 and len(ctrl_pre_sends) == 0:
            self.log.info(f'\n\t —— 当前页面未找到发表/已发表,num_all_ctrl_already_sends+4 —— ')
            self.num_all_ctrl_already_sends += 4

    def time_judge(self, task_time):
        time_str = datetime.now().strftime('%Y年') + task_time
        tasktime = datetime.strptime(time_str, '%Y年%m月%d日 %H:%M')
        flag_time = (datetime.now() - timedelta(days=self.time_gap)).strftime('%Y年%m月%d日') + self.time_flag
        flag_time = datetime.strptime(flag_time, '%Y年%m月%d日%H:%M')
        if not (tasktime >= flag_time):
            self.log.info(f'\n\t —— 最新的企业朋友圈任务时间为{tasktime},已到达发送截至时间{flag_time} —— ')
            return False
        else:
            return tasktime

    def start_process(self):
        # 启动企微
        # self.init_phone()
        self.init_wework()

        # 点击“工作台”
        ctrl_work_platform = self.poco(name=self.V['WORKSTATION'], text='工作台')
        self.ctrl_operate(ctrl_work_platform, op_type='click', msg="工作台")

        # 点击“客户朋友圈”
        ctrl_client_friend_circle = self.poco(text='客户朋友圈')
        self.ctrl_operate(ctrl_client_friend_circle, op_type='click', msg="客户朋友圈")

        # 判断是否是新用户
        if self.poco(name=self.V['NEW_USER']).exists():
            self.log.info('\n\t —— 检测当前用户第一次打开客户朋友圈,点击"立即使用" —— ')
            self.poco(name=self.V['NEW_USER']).click()

        # 点击“右上角消息按钮”/wework 4.0.0的新消息红点
        try:
            self.poco(name=self.V['PYQ_MSG1']).wait_for_appearance(timeout=self.timeout)
            self.poco(name=self.V['PYQ_MSG1']).click()
            self.log.info(f'\n\t —— 点击右上角新消息红点 —— ')
        except Exception as e:
            self.log.warning(f'\n\t —— 当前未检测到新消息红点，{e} —— ')
            try:
                self.poco(name=self.V['PYQ_MSG']).wait_for_appearance(timeout=self.timeout)
                self.poco(name=self.V['PYQ_MSG']).click()
                self.log.info(f'\n\t —— 点击右上角选项 —— ')
                self.poco(name=self.V['COMPANY_NOTIFICATION'], text='企业通知').wait_for_appearance(timeout=self.timeout)
                self.poco(name=self.V['COMPANY_NOTIFICATION'], text='企业通知').click()
                self.log.info(f'\n\t —— 点击 企业通知 —— ')
            except Exception as e:
                self.log.warning(f'\n\t —— 当前未检测到右上角选项/企业通知,{e},任务结束 —— ')
                self.output_task_data()
                return True

        if not self.no_task_judge():
            self.output_task_data()
            return True

        # 处理“发送”消息
        self.num_all_ctrl_already_sends = 0
        while self.num_all_ctrl_already_sends < 4:
            self.swipe_up_click()

        self.log.info("\n\t —— 客户朋友圈任务所有“发表”处理完毕 √ —— ")
        self.output_task_data()
        return True

    def output_task_data(self):
        '''
        output pyq sop task data.
        '''
        use_time = (str(datetime.now() - self.start_time)[:-7]).split(':')
        msg = f'\t 群发企业消息任务结束 \
            \n\t 任务用时: {use_time[0]}时{use_time[1]}分{use_time[2]}秒 \
            \n\t 客户朋友圈任务执行数:{self.task_num} \
            \n\t 任务进行出错数:{self.error_times} '
        self.log.info(f'\n\t —— {msg} —— \n\t —— task-2 end... —— ')
        if self.task_num > 0:
            self.report(msg)

    def run(self):
        self.init_attributes()
        if self.error_times > 2:
            self.log.info("\n\t —— 客户朋友圈任务 中间环节出错超过2次...跳出，执行下一任务 —— ")
            self.output_task_data()
            return False
        else:
            self.log.info("\n\t —— 开始执行 客户朋友圈任务 —— ")
            return self.start_process()


if __name__ == "__main__":
    r = ClientFriendCircle()
    r.run()

