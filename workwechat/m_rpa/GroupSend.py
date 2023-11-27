# -*- encoding=utf8 -*-
__author__ = "zyh"
import time
from time import sleep
from datetime import datetime

from .base import Base
from .constants import *


class GroupSend(Base):
    def __init__(self, log, obj_dict):
        super().__init__(log, obj_dict)
        
    def init_attributes(self):
        self.start_time = datetime.now()
        self.operate_num = 0
        self.task_error = 0

    def click_workbench(self):
        '''
        点击工作台
        :return:
        '''
        try:
            self.log.info('\n\t —— 初始化手机 —— ')
            self.init_phone()
            self.log.info("\n\t —— 'home'键返回主界面. —— ")
            self.home()
            self.init_wework()
            self.log.info('\n\t —— 点击工作台 —— ')
            self.poco(name=self.V['WORKSTATION'],text='工作台').click()
            return True
        except Exception as e:
            real_window = self.dev.get_top_activity_name()
            self.log.error(f'\n\t —— 点击"工作台"失败:{e} —— '
                           if real_window == MAIN_WINDOW else
                           f'\n\t —— 点击"工作台"失败{e}当前窗口不是目标窗口,而是是{real_window} —— ')

    def click_group_send(self):
        try:
            count = 1
            while count<=5:
                freeze_poco = self.poco.freeze()
                res = freeze_poco(text='群发助手').exists()
                if res:
                    self.log.info('\n\t —— 检测到群发助手,点击进入 —— ')
                    freeze_poco(text='群发助手').click()
                    return True
                else:
                    count += 1
                    self.log.info(f'\n\t —— 没有找到群发助手,向上滑,进行第{count}次寻找 —— ')
                    self.swipe([self.x * 0.5, self.y * 0.22], [self.x * 0.4, self.y * 0.88], duration=0.01, steps=9)
            self.log.error(f'\n\t —— 尝试查找群发助手{count}次未果 —— ')
            self.alarm('寻找群发助手按钮', msg=f'尝试查找群发助手{count}次未果')
            return False
        except Exception as e:
            real_window = self.dev.get_top_activity_name()
            self.log.error(f'\n\t —— 点击"群发助手"失败{e} —— '
                           if real_window == MAIN_WINDOW else
                           f'\n\t —— 点击"群发助手"失败{e}当前窗口不是目标窗口,而是是{real_window} —— ')
            self.alarm('点击群发助手', msg=str(e))

    def click_notifications(self):
        '''
        点击通知,有通知就点击,没有就返回False
        :return:
        '''
        # freeze_poco = self.poco.freeze()

        send_enter = self.poco(name=self.V['SEND_FLAG'])
        send_enter1 = self.poco(name=self.V['SEND_FLAG1'])

        try:
            send_enter1.wait_for_appearance(timeout=self.timeout)
            self.log.info('\n\t —— 在顶部检测到通知,点击进入 —— ')
            send_enter1.click()
            return True
        except:
            try:
                send_enter.wait_for_appearance(timeout=self.timeout)
                self.log.info('\n\t —— 在中间检测到通知,点击进入 —— ')
                send_enter.click()
                return True
            except:
                self.log.info('\n\t —— 没有检测到可以处理的任务,点击进入处理任务页面 —— ')
                return False


    def _dump_time(self,send_time):
        try:
            datetime.strptime(send_time,"%H:%M")
            return True
        except Exception as e:
            self.log.info(f'\n\t —— 非可执行任务{e} —— ')
            return False

    def _excute_time(self,time_str):
        '''
        默认值为today:执行今天的所有任务
        yestoday:执行今天加昨天的任务
        星期四:执行今天加星期四的任务(前提最新的一条星期四的任务与今天需要发送的任务消息是挨在一起的,或者点击去直接是星期四的消息,否则做不了,群发没有翻页操作)
        10:00:只执行今天上午十点之后的任务
        :param time_str:
        :return:
        '''
        execute_time = self.get_config_info('stop sending time', 'execute_time')
        try:
            if '：' in execute_time:
                execute_time = execute_time.replace('：', ':')
        except:
            pass
        if execute_time == 'today':
            if time_str == '刚刚' or '分钟前' in time_str or '上午' in time_str or '下午' in time_str or self._dump_time(time_str):
                self.log.info(f'\n\t —— 当前设置:只处理今天的任务 —— ')
                return '1'
        elif execute_time == 'yestoday':
            if time_str == '刚刚' or '分钟前' in time_str or '上午' in time_str or '下午' in time_str or '昨天' in time_str or self._dump_time(time_str):
                self.log.info(f'\n\t —— 当前设置:处理今天+昨天的任务 —— ')
                return '1'
        elif self._dump_time(execute_time):
            if '上午' in time_str or '下午' in time_str:
                self.log.error(f'\n\t —— 当前设置:只执行当天{execute_time}后的任务,出现未能识别的时间"{time_str}",请尽快将手机时间设置成24小时制 —— ')
                self.alarm(msg=f'检测到当前一对一私聊只执行当天{execute_time}后的任务,出现未能识别的时间"{time_str}",请尽快将手机时间设置成24小时制')
                return '2'
            else:
                time1 = datetime.strptime(execute_time, "%H:%M")
                time2 = datetime.strptime(time_str, "%H:%M")
                time3 = str(time2-time1)
                time_str_list = time3.split(':')
                if time2 > time1:
                    self.log.info(f'\n\t —— 当前设置:只处理今天{execute_time}后的任务 —— ')
                    return '1'
                elif len(time_str_list) == 3 and '分钟前' in time_str:
                    minute = (time_str.split('分'))[0]
                    if int(minute) < int(time_str_list[1]):
                        self.log.info(f'\n\t —— 当前设置:只处理今天{execute_time}后的任务 —— ')
                        return '1'
        else:
            if time_str == '刚刚' or '分钟前' in time_str or '上午' in time_str or '下午' in time_str or execute_time in time_str or self._dump_time(time_str):
                self.log.info(f'\n\t —— 当前设置:处理今天+{execute_time}的任务 —— ')
                return '1'

    def exception_handling(self):
        '''处理点击发送过程中遇到的一些问题'''
        page_name = self.dev.get_top_activity_name()
        if 'com.tencent.wework' in page_name:
            if page_name == GROUP_SEND_WINDOW:
                return True
            elif 'Image' in page_name:
                self.log.info(f'\n\t —— 由于页面卡顿打开了图片,关闭图片,建议调整配置文件中点击发送的间隔时间 —— ')
                self.touch_point(10,int(self.y*0.5))
            else:
                freeze_poco = self.poco.freeze()
                back_button = freeze_poco(name=self.V['BACK'])
                if back_button.exists():
                    self.log.info(f'\n\t —— 由于页面卡顿可能点进了消息详情页,返回任务处理页面,建议调整配置文件中点击发送的间隔时间 —— ')
                    back_button.click()
                    if self.dev.get_top_activity_name() == GROUP_SEND_WINDOW:
                        return True
                else:
                    self.dev.start_app(WEWORK_PKG)
                    if self.dev.get_top_activity_name() == GROUP_SEND_WINDOW:
                        return True
        else:
            self.log.info(f'\n\t —— 检测到当前页面非企微页面,启动企微 —— ')
            self.dev.start_app(WEWORK_PKG)
            sleep(0.5)
            activity_name = self.dev.get_top_activity_name()
            if activity_name == GROUP_SEND_WINDOW:
                self.log.info(f'\n\t —— 已经回到一对一任务的页面 —— ')
                return True
            else:
                self.log.info(f'\n\t —— 已经回到一对一任务的页面 —— ')
                return False



    def click_on_send(self):
        '''
        将当前页的所有元素信息拿到,分析符合发送条件的发送按钮个数,计算每个发送按钮到达顶部时的坐标,依次点击
        由于当前页面获取元素的速度特别慢,所以采取当前方案,之后若找到获取元素快的方法可优化以提高执行任务的效率
        :return:
        '''
        trytimes = 0   #出错重试最多次数
        maxtimes = 0  #每轮做任务最多次数限制
        every_task_wait_time = self.get_config_info('stop sending time','every_task_wait_time')
        try:
            every_task_wait_time = round(float(every_task_wait_time),2)
            if every_task_wait_time < 1:
                every_task_wait_time = 1
        except:
            every_task_wait_time = 1.3
            self.alarm(msg=f'获取点击发送按钮间隔时间出错,请检查配置表,现已设置为默认值:1.3s/次')

        self.start_time=datetime.now()
        while maxtimes<100 and trytimes <= 5:
            start_time = datetime.now()
            if not self.exception_handling():
                self.log.info(f'\n\t —— 处理异常情况出错,出错数+1 —— ')
                trytimes += 1
                wait_time = 3
                self.log.info(f'\n\t —— {wait_time}秒后继续 —— ')
                sleep(wait_time)
            try:
                self.log.info(f'\n\t —— 分析本页信息 —— ')
                freeze_poco = self.poco.freeze()   #冻结本页元素
                msg = freeze_poco(name=self.V['MSG_HEIGHT'])   #定义消息体name
                send_button = freeze_poco(name=self.V['SEND_BUTTON'])  #定义发送按钮name
                start1_time = freeze_poco(name=self.V['START_TIME'])   #定义任务执行时间name
                num = 0
                try:
                    for i in send_button:
                        '''判断当前页面发送按钮的个数'''
                        num+=1
                except:
                    if self.dev.get_top_activity_name() == WEWORK_PKG:
                        self.log.info(f'\n\t —— 当前页面没有任务需要处理 —— ')
                        return True
                    else:
                        self.log.info(f'\n\t —— 当前页面不是一对一任务处理页面 —— ')
                        trytimes+=1
                        continue
                self.log.info(f'\n\t —— 当前页面有{num}条消息需要处理 —— ')
                pos_list = []
                msg_bounds = msg.get_bounds()
                top_msg_distance = int(msg_bounds[0] * self.y)  # 顶部消息体距离顶部距离  消息体(文本+素材+查看全文)
                for i in range(num):
                    if i == 0:
                        self.log.info(f'\n\t —— 分析第{i+1}条消息 —— ')
                        time_str = start1_time[i].get_text()   #获取第一条消息的任务分配时间
                        if self._excute_time(time_str) == '1':
                            pos_x = send_button.get_position()   #  顶部消息的发送按钮坐标
                            self.log.info(f'\n\t —— 第{i+1}条任务可执行 —— ')
                            pos_list.append([int(self.x*0.5), int(self.y*pos_x[1])])  #将获取到的坐标信息放进坐标列表中
                        elif self._excute_time(time_str) == '2':
                            self.log.info(f'\n\t —— 检测到当前手机设备时间不是24小时制 —— ')
                            return True
                    else:
                        self.log.info(f'\n\t —— 分析第{i+1}条消息 —— ')
                        time_str = start1_time[i].get_text()   #获取后面消息的任务分配时间
                        if self._excute_time(time_str) == '1':
                            msg_size = msg[i].get_size()
                            msg_height = int(msg_size[1] * self.y)  # 第二个消息的高度
                            self.log.info(f'\n\t —— 第{i+1}条任务可执行 —— ')
                            #  计算该条消息到达顶部时,发送按钮的坐标,添加到坐标列表中
                            pos_list.append([int(self.x*0.5), top_msg_distance+msg_height+90])
                        elif self._excute_time(time_str) == '2':
                            self.log.info(f'\n\t —— 检测到当前手机设备时间不是24小时制 —— ')
                            return True
                task_num = len(pos_list)
                if task_num>0:   #pos_list中有值
                    time_wait = 0
                    for i in pos_list:
                        '''点击i坐标'''
                        self.log.info(f'\n\t —— 点击{i[0],i[1]} —— ')
                        self.touch_point(i[0],i[1])
                        time_wait += 1
                        maxtimes += 1
                        if task_num -time_wait != 0 :
                            '''执行完最后一条不等待'''
                            sleep(every_task_wait_time)
                        else:
                            sleep(0.5)
                        self.operate_num+=1
                        self.log.info(f'\n\t —— 本轮处理了{self.operate_num}条任务 —— ')
                else:
                    now_page = self.dev.get_top_activity_name()
                    if now_page == GROUP_SEND_WINDOW:
                        self.log.info(f'\n\t —— 当前页面没有任务需要处理 —— ')
                        self.log.info(f'\n\t —— 当前无符合条件的内容,跳出本轮任务,本轮公处理了{self.operate_num}条任务 —— ')
                        freeze_poco(name=self.V['BACK']).click()
                        return True
                    else:
                        self.log.info(f'\n\t —— 当前页面不是一对一任务处理页面 —— ')
                        trytimes+=1
                        continue



                # self.log.info(f'\n\t —— 遍历当前页面节点信息 —— ')
                # send_time = (self.poco(name=self.V['SENG_PAGE'])).offspring()
                # list = []
                # time = True
                # for ui in send_time:
                #     if ui.get_name() == self.V['START_TIME']:
                #         if time:
                #             self.log.info(f'\n\t —— 判断顶部任务的执行时间 —— ')
                #             time_str = ui.get_text()
                #             if self._excute_time(time_str) == '1':
                #                 self.log.info(f'\n\t —— 检测到一条{time_str}的任务 —— ')
                #                 list.append(time_str)
                #                 time = False
                #             elif self._excute_time(time_str) == '2':
                #                 self.log.info(f'\n\t —— 检测到当前手机设备时间不是24小时制 —— ')
                #                 return True
                #     if len(list) > 0:
                #         if ui.get_name() == self.V['SEND_BUTTON']:
                #             self.log.info(f'\n\t —— 存在可发送的任务准备点击发送 —— ')
                #             try:
                #                 pos = ui.get_position()
                #                 x = int(pos[0]*self.x)
                #                 y = int(pos[1]*self.y)
                #                 self.operate_num+=1
                #                 max_y = 1100
                #                 if y < max_y:
                #                     self.log.info(f'\n\t —— 获取发送按钮坐标为{x,y} —— ')
                #                     self.touch_point(x,y)
                #                     break
                #                 self.log.error(f'\n\t —— 检测到当前定位到的发送按钮的y坐标为{y}超过规定范围{max_y},退出本轮任务 —— ')
                #                 return True
                #             except Exception as e:
                #                 self.log.error(f'\n\t —— 存在可发送的任务,但是点击发送按钮出了问题 —— ')
                #                 self.alarm(photo_name='点击发送按钮', msg=f'存在可发送的任务,但是点击发送按钮出了问题\n{e}')
                #                 return True
                # trytimes = 0
                # if len(list) == 0:
                #     self.log.info(f'\n\t —— 当前页面检测不到可做的任务,一共发送了{self.operate_num}条群发任务,退出本轮任务 —— ' if self.operate_num != 0 else
                #                   f'\n\t —— 当前页面检测不到可做的任务,退出本轮任务 —— ')
                #     return True

            except Exception as e:
                trytimes +=1
                if trytimes == 5:
                    self.log.error(f'\n\t —— 当前页面尝试次数超过{trytimes}次,退出{e} —— ')
                    break
                if maxtimes >= 100:
                    self.log.info(f'\n\t —— 当前页面点击次数已达{self.operate_num}次,退出{e} —— ')
                    freeze_poco(name=self.V['BACK']).click()
                    break
            self.log.info(f'\n\t —— 当前页执行时间{datetime.now() - start_time} —— ')
            self.log.info(f'\n\t —— 总用时{datetime.now() - self.start_time} —— ')
        self.log.info(f'\n\t —— 当前页面检测不到当日的可发送消息,一共发送了{self.operate_num}条群发任务,退出 —— ')
        freeze_poco(name=self.V['BACK']).click()
        return True
                
    def output_task_data(self):
        '''
        output pyq sop task data.
        '''
        use_time = (str(datetime.now() - self.start_time)[:-7]).split(':')
        msg = f'\t 群发企业消息任务结束 \
            \n\t 任务用时: {use_time[0]}时{use_time[1]}分{use_time[2]}秒 \
            \n\t 群发企业消息操作数: {self.operate_num} \
            \n\t 任务进行出错数: {self.task_error} \
            '
        self.log.info(f'\n\t —— {msg}'+' —— \n\t —— task-1 end... —— ')
        # \n\t
        # 群发企业消息任务数: {self.task_num} \
        if self.operate_num > 0:
            self.report(msg)

    def test(self):
        '''
        test
        '''
        # print("start test...")
        self.log.error(f'\n\t —— {time.ctime()} —— \n\t —— 点击"工作台"失败 —— '
                       if 1 == 2 else
                       f'\n\t —— {time.ctime()} —— \n\t —— 点击"工作台"失败当前窗口不是目标窗口,而是是1 —— ')
        # while True:
            # time1 = random.uniform(1.00, 1.70)
            # print(round(time,2))
            # sleep(round(time1,2))
            # self.log.info(f' —— {time.ctime()}开始做群发任务 —— ')

        # self.init_wework()

    def run_task(self):
        '''执行群发任务'''
        try:
            self.log.info(f'\n\t —— 开始做群发任务 —— ')
            count = 1   #循环次数\总出错次数
            wait_time = 3   #进入下一次循环等待的秒数
            while count<=5:
                if count > 1:
                    super().__init__()
                if not self.click_workbench():  # 点击工作台
                    self.task_error += 1
                    count+=1    #记录总出错次数
                    self.log.info(f'\n\t —— 等待{wait_time}秒重新开始任务 —— ')
                    sleep(wait_time)   #等待10秒后进入下一次循环
                    continue
                if not self.click_group_send():     #点击群发助手
                    self.log.info(f'\n\t —— 点击"群发助手"失败,{wait_time}秒后重试 —— ')
                    self.task_error += 1
                    count += 1  # 记录总循环次数
                    sleep(wait_time)  # 等待10秒后进入下一次循环
                    continue
                if not self.click_notifications():   #点击需要处理的任务
                    self.log.info(f'\n\t —— 没有检测到通知,退出任务 —— ')
                    return
                if self.click_on_send():  #点击发送
                    self.log.info('\n\t —— 群发任务执行完毕,回到企微首页 —— ')
                    return
            self.log.info(f'\n\t —— 尝试{count}次执行群发任务没有结果,任务中断 —— ')
            return True
        except Exception as e:
            real_window = self.dev.get_top_activity_name()
            self.log.info(f'\n\t —— 执行群发任务出现错误{e}当前窗口不是目标窗口,而是是{real_window} —— ')
            return True

    def run(self, *args, **kwargs):
        self.init_attributes()
        self.run_task()
        self.output_task_data()


if __name__ == "__main__":
    r = GroupSend()
    r.test()
