# -*- encoding=utf8 -*-
__author__ = "zyh"
from time import sleep
from datetime import datetime, timedelta

from airtest.core.cv import Template
from airtest.core import api as air_api

from .base import Base,CvExercise
from .constants import *
from db.model import Soplog,SopTag
from db.manager import DbManager


class Sop(Base):
    def __init__(self, log, obj_dict):
        super().__init__(log, obj_dict)
        self.server = self.check_server()
        self.time_gap, self.time_flag= self.get_config_time()

    def init_attributes(self):
        self.start_time = datetime.now()
        self.copy_tag = None
        self.tag_time = None
        self.task_count = 0
        self.no_tag = 0
        self.no_customer = 0
        self.task_error = 0
        self.success_list = []
        self.no_tag_list = []
        self.no_customer_list = []

    def get_config_time(self):
        try:
            sopgapday = self.get_config_info('stop sending time', 'sopdaygap')
            stoptime = self.get_config_info('stop sending time', 'soptime')
            if '：' in stoptime:
                stoptime = stoptime.replace('：', ':')
        except:
            sopgapday = 1
            stoptime = '22:00'
            self.log.warning('\n\t —— config-sop时间未配置 —— ')
            self.alarm('',f'配置当中缺少sop时间配置')
        if not sopgapday.isdigit() or ':' not in stoptime:
            sopgapday = 1
            stoptime = '22:00'
            self.log.warning('\n\t —— config-sop时间格式配置错误 —— ')
            self.alarm('',f'配置时间格式错误')
        return int(sopgapday),stoptime

    def open_luoshu_SMR(self):
        '''
        open app'洛书SMR（-test）'
        '''
        error_times = 0
        while True:
            try:
                self.poco(name=self.V['TEXT'],text=self.server).wait_for_appearance(timeout=self.timeout)
                self.poco(name=self.V['TEXT'],text=self.server).click()
                air_api.sleep(0.2)
                break
            except Exception as e:
                if error_times > 2:
                    return False
                self.log.error(f'\n\t Search result Not found! {e}')
                if self.poco(name=self.V['CLEAR_TEXT']).exists():
                    self.log.info(f"\n\t —— Click Clear button. —— ")
                    self.poco(name=self.V['CLEAR_TEXT']).click()
                if self.poco(name=self.V['SEARCH']).exists():
                    self.log.info(f"\n\t —— Click search button. —— ")
                    self.poco(name=self.V['SEARCH']).click()
                    air_api.sleep(1)
                self.log.info(f"\n\t —— Input text :{self.server}. —— ")
                air_api.text(self.server)
                error_times += 1

        if self.poco(name=self.V['SMR_TITLE'],text=self.server).exists():
            self.log.info(f"\n\t —— Now at {self.server} panel. —— ")
            return True
        else:
            self.log.error(f'\n\t —— Not in {self.server} 页面! Current panel is:{self.dev.get_top_activity_name()} —— ')
            return False

    def find_pyq_customer_sop(self):
        '''
        find customer sop which task-type is pyq.
        '''
        error_times = 0
        while True:
            if error_times > 2: return
            try:
                self.poco(name=self.V['SOP']).wait_for_appearance(timeout=self.timeout*3)
                sop_msg = self.poco(name=self.V['SOP'])
                soplist = [i for i in sop_msg]
                is_friendcircle_sop = False
                for sop in soplist[::-1]:
                    rect, sop_info = sop.get_position(), sop.child()
                    if len(sop_info) > 3:  # 加载出来的完整sop(有三个以上ui的info)
                        for info in sop_info:
                            info_name,info_text = info.get_name(),info.get_text()
                            if  info_name == self.V['SOP_TYPE'] and '朋友圈' in info_text:
                                is_friendcircle_sop = True
                                self.copy_tag = info_text.split('：')[-1]   #标签
                                self.tag_time = self.time_judge(ui_text=info_text)  #时间判断
                                if self.judge_sop_status(info=info,rect=rect):
                                    break
                                else:
                                    return
                        if not is_friendcircle_sop:
                            self.delete_sop(rect)  # 删掉之后重新检测
                        break
            except Exception as e:
                self.log.error(f'\n\t —— SOP Not found! {e} —— ')
                error_times += 1

    def judge_sop_status(self, info, rect):
        '''
        judeg sop status and do next step.
        :return -> boolean
        if True: back to sop list and check status again.
        if False: end task3.
        '''
        if not self.tag_time: return False

        tag_status = self.check_from_db()
        if tag_status == 1:  # sop未执行
            res1 = self.click_sop(ui=info)
            if not res1:
                return False
            elif res1 == 'ok':  # 打开成功执行任务
                if self.do_pyq_sop():
                    return True
                else:
                    return False
            elif res1 == 'goback':
                return True
        elif tag_status == 2:
            res2 = self.click_sop(ui=info, reply=True)
            if not res2:
                return False
            elif res2 == 'ok' or res2 == 'goback':
                return True
        elif tag_status == 3:
            return self.delete_sop(rect)

    @DbManager.db_session
    def check_from_db(self, session):
        '''
        check the tag status from the db.
        '''
        result = session.query(Soplog).filter(Soplog.soptime == self.tag_time, Soplog.soptag == self.copy_tag).first()
        if result:
            return int(result.status)
        else:
            status = 1
            soplog = Soplog(soptime=self.tag_time, soptag=self.copy_tag, status=status)
            session.add(soplog)
            session.commit()
            return status

    @DbManager.db_session
    def update_sop_status(self, session, status):
        '''
        update sop to target status.
        '''
        result = session.query(Soplog).filter(Soplog.soptime == self.tag_time, Soplog.soptag == self.copy_tag).first()
        if result:
            result.status = status
        else:
            status = status
            soplog = Soplog(soptime=self.tag_time, soptag=self.copy_tag, status=status)
            session.add(soplog)
        session.commit()

    @DbManager.db_session
    def sop_no_tag(self, session):
        result = session.query(Soplog).filter(Soplog.soptime == self.tag_time, Soplog.soptag == self.copy_tag).first()
        if result:
            if result.notag is not None:
                return result.notag
        else:
            soplog = Soplog(soptime=self.tag_time, soptag=self.copy_tag, status=1)
            session.add(soplog)
            session.commit()
        return 0

    @DbManager.db_session
    def update_notag_times(self, session):
        result = session.query(Soplog).filter(Soplog.soptime == self.tag_time, Soplog.soptag == self.copy_tag).first()
        if result:
            if result.notag is not None:
                result.notag += 1
            else:
                result.notag = 1
        else:
            soplog = Soplog(soptime=self.tag_time, soptag=self.copy_tag, status=1, notag=1)
            session.add(soplog)
        session.commit()

    def time_judge(self,ui_text):
        sop_time = ui_text.split('\n')[0] + ui_text.split('\n')[3].split(':')[0][-2:] + ':' + ui_text.split('\n')[3].split(':')[1][0:2:1]
        sop_time = datetime.strptime(sop_time,'%Y年%m月%d日%H:%M')
        flag_time = (datetime.now() - timedelta(days=self.time_gap)).strftime('%Y年%m月%d日') + self.time_flag
        flag_time = datetime.strptime(flag_time,'%Y年%m月%d日%H:%M')
        self.log.info(f'\n\t —— 最新的朋友圈SOP发送时间点为:{sop_time} —— ')
        if not(sop_time >= flag_time):
            self.log.info(f'\n\t —— 已到SOP时间截至点:{flag_time},之前的任务将不会进行,结束任务.. —— ')
            return False
        else:
            return sop_time

    def click_sop(self, ui, reply=False):
        '''
        click in sop
        '''
        click_try = 0
        while True:     #判断点击sop之后是否有jsweb页面响应
            self.log.info(f'\n\t —— 点击进入一条SOP,标签为:{self.copy_tag},当前尝试次数为:{click_try} —— ')
            ui.click()
            click_try += 1
            sleep(1)
            try:
                activity_name = self.dev.get_top_activity_name()
                if activity_name == 'com.tencent.wework/.common.web.JsWebActivity':
                    break
            except:
                sleep(1)
            if click_try >= 3:
                self.log.info(f'\n\t —— 当前尝试三次未点击进入SOP,将进入下一任务 —— ')
                return False

        wait_time = 0  # 判断js页面加载完整性
        while True:
            try:
                self.screenshot_to_file()
                cv = CvExercise()
                ratio, pos_x, pos_y = cv.get_context_contour_w_h_ratio(SHARE_CONTOURS)
                self.log.info(f'\n\t —— 正在寻找分享ratio:{ratio} x:{pos_x} y:{pos_y} —— ')
                if ratio > 5:
                    air_api.touch((pos_x,pos_y))
                    break
                if wait_time > 50:
                    self.log.warning(f'\n\t —— loading SOP timeout by cv method. —— ')
                    break
                wait_time += 1
            except Exception as e:
                self.log.error(f'cv方法识别时出现错误:{e}')
                break

        try_times = 0  # 判断点击分享是否成功到发表页面
        while True:
            try:
                self.log.debug('\n\t —— 寻找"发表"元素 —— ')
                self.poco(name=self.V['PUBLISH'],text='发表').wait_for_appearance(timeout=self.timeout)
                if not reply: return 'ok'
                else: break
            except:
                if try_times < 1:   #第一次图像识别点击
                    try_times += 1
                    air_api.touch((int(0.5*self.x),int(0.96*self.y)))
                    self.log.debug(f'\n\t —— 第{try_times}次尝试坐标点击 —— ')
                elif try_times == 1:       # 第二次坐标点击
                    try:
                        try_times += 1
                        self.log.debug(f'\n\t —— 第{try_times}次尝试图片匹配点击 —— ')
                        air_api.touch(Template(UI_PATH+'\SHARE.png',threshold=0.8))
                    except Exception as e:
                        self.log.error(f'\n\t 尝试点击第{try_times}次失败:{e} —— ')
                elif try_times == 2:        #第三次cv识别
                    try_times += 1
                    try:
                        self.log.debug(f'\n\t —— 第{try_times}次尝试CV识别图片 —— ')
                        self.screenshot_to_file()
                        cv = CvExercise()
                        ratio, pos_x, pos_y = cv.get_context_contour_w_h_ratio(SHARE_CONTOURS)
                        if ratio > 5:
                            air_api.touch((pos_x,pos_y))
                    except Exception as e:
                        self.log.error(f'cv方法识别时出现错误:{e}')
                else:
                    self.log.debug(f'\n\t —— 加载SOP超时,{try_times}次尝试失败， —— ')
                    self.alarm(msg='SOP加载超时,点击分享失败')
                    return 'back'
        
        if not self.go_back(special_situation='web页面加载完成,点击回执',reply=reply): return False
        else: return 'ok'     
    
    def do_pyq_sop(self):
        '''
        Make sure click in republic panel.
        '''
        step1_error = 0
        while True:  # 1.点击可见的客户  公开
            try:
                self.poco(name=self.V['VISIBLE_0']).wait_for_appearance(timeout=self.timeout*2)
                self.poco(name=self.V['VISIBLE_0']).click()
                self.log.debug(f"\n\t —— 点击'可见的客户' —— ")
                break
            except Exception as e:
                if step1_error > 3:
                    return self.go_back(step=1, e=e, special_situation='没有可见的用户按钮')
                air_api.swipe([self.x * 0.5, self.y * 0.8], [self.x * 0.5, self.y * 0.3], duration=0.3, steps=5)
                self.log.debug(f"\n\t —— '可见的客户'找不到,向下滑动第{step1_error}次 —— ")
                step1_error += 1

        try:
            self.poco(name=self.V['VISIBLE_1']).wait_for_appearance(timeout=self.timeout*2)
            self.poco(name=self.V['VISIBLE_1']).click()
        except Exception as e:
            return self.go_back(step=2, e=e, special_situation='没有部分可见按钮')

        try:    # 3.进入选择标签页
            self.poco(name=self.V['SELECT_TAG']).wait_for_appearance(timeout=self.timeout*2)
            self.poco(name=self.V['SELECT_TAG']).click()
            self.log.debug(f"\n\t —— 点击'根据标签筛选' —— ")
            self.poco(name=self.V['TAG_TITLE'],text='标签筛选').wait_for_appearance(timeout=self.timeout*2)
            self.log.debug(f"\n\t —— 到达'标签筛选页' —— ")
        except Exception as e:
            return self.go_back(step=3, e=e, special_situation='没有根据标签筛选按钮')

        try:     # 4.选择客户标签
            page = 0
            # quickly turn to index page nearby.
            notag_times = self.sop_no_tag()
            page_index = self.check_tag_page(tag=self.copy_tag)
            if page_index and page_index > 3 and notag_times == 0:
                for i in range(page_index-2):
                    air_api.swipe([self.x * 0.5, self.y * 0.87], [self.x * 0.5, self.y * 0.05], duration=0.35, steps=7)
                    page += 1
                    
            jump_out_judge = 0       
            temp_tag = None
            find_flag = False
            # record every tag not in db.
            while True:
                freeze_poco = self.poco.freeze()
                for i in freeze_poco(name=self.V['PERSONAL_TAG']):
                    for x in i.child():
                        tag = x.get_name()
                        self.update_tag_db(tag=tag,page=page)
                        if tag == self.copy_tag:
                            find_flag = True
                if find_flag:
                    freeze_poco(text=self.copy_tag).click()
                    self.log.debug(f"\n\t —— 点击标签{self.copy_tag} —— ")
                    freeze_poco(name=self.V['CONFIRM_0'],text='确定').click()
                    self.log.debug(f"\n\t —— 点击'确定' —— ")
                    break
                else:
                    #filp to next page determine whether flip to the bottom
                    air_api.swipe([self.x * 0.5, self.y * 0.87], [self.x * 0.5, self.y * 0.05], duration=0.35, steps=7)
                    page += 1
                    current_tag = freeze_poco(name=self.V['PERSONAL_TAG']).child().get_text()   #当前页的标签名
                    if temp_tag == current_tag:
                        jump_out_judge += 1
                    else:
                        jump_out_judge = 0
                    temp_tag = freeze_poco(name=self.V['PERSONAL_TAG']).child().get_text()  #更新缓存标签名
                    if jump_out_judge >= 3:
                        if notag_times > 2:
                            self.update_sop_status(status=2)
                            return self.go_back(special_situation='连续三次没找到标签',reply=True)
                        else:
                            self.update_notag_times()
                        return self.go_back(special_situation=f'第{notag_times+1}次没找到标签')
        except Exception as e:
            return self.go_back(step=4,e=e,special_situation='确定按钮或者标签未显示,可能时网络原因')

        try:  # 5.点击全部客户
            self.poco(text='全部客户').wait_for_appearance(timeout=self.timeout*3)
            self.poco(text='全部客户').click()
            self.log.debug(f"\n\t —— 点击'全部客户' —— ")
        except Exception as e:
            self.update_sop_status(status=2)  # 对应的标签标记为ok状态，不再执行
            return self.go_back(special_situation='没有标签对应的客户', reply=True)

        try:        # 6.点击确定
            self.poco(name=self.V['CONFIRM_1']).wait_for_appearance(timeout=self.timeout*2)
            try_times = 0
            while True:
                if try_times > 3:
                    return self.go_back(special_situation='没有成功全选客户')
                if len(self.poco(name=self.V['CONFIRM_1']).get_text()) > 2:
                    self.poco(name=self.V['CONFIRM_1']).click()
                    break
                else:
                    self.poco(text='全部客户').click()
                    try_times += 1
            self.log.debug(f"\n\t —— 点击'确定(1)' —— ")
            self.poco(name=self.V['CONFIRM_2']).wait_for_appearance(timeout=self.timeout*2)
            self.poco(name=self.V['VISIBLE_1']).wait_for_appearance(timeout=self.timeout*2)
            if self.poco(name=self.V['VISIBLE_1']).offspring(name=self.V['SELECTED']).exists():     #确定已经勾选了部分可见
                self.poco(name=self.V['CONFIRM_2']).click()
                self.log.debug(f"\n\t —— 点击'确定(2)' —— ")
            else:
                return self.go_back(special_situation='没有成功选择到部分可见')
        except Exception as e:
            return self.go_back(step=6,e=e,special_situation='没有确定按钮')
        
        try:        # 7.点击发表
            self.poco(name=self.V['PUBLISH']).wait_for_appearance(timeout=self.timeout*2)
            self.poco(name=self.V['PUBLISH'],text='发表').click()
            self.update_sop_status(status=2)       #点击发表之后对应的标签
            self.log.debug(f"\n\t —— 点击'发表' —— ")
            self.success_list.append(self.copy_tag)
        except Exception as e:
            return self.go_back(step=7, e=e, special_situation='没有发表按钮')

        try:        # 8.等待进入朋友圈界面后返回
            self.poco(name=self.V['PYQ']).wait_for_appearance(timeout=self.timeout*2)
        except Exception as e:
            pass

        return self.go_back(special_situation='发表了SOP朋友圈', reply=True)

    @DbManager.db_session
    def update_tag_db(self,session,tag,page):
        '''
        search tag in db.
        '''
        result = session.query(SopTag).filter(SopTag.soptag==tag).first()
        if result:
            result.page = page
        else:
            result = SopTag(soptag=tag,page=page)
            session.add(result)
        session.commit()

    @DbManager.db_session
    def check_tag_page(self,session,tag):
        '''
        search tag in db.
        '''
        result = session.query(SopTag).filter(SopTag.soptag==tag).first()
        if result:
            return result.page
        else:
            return False

    def delete_sop(self,rect):
        '''
        delete the sop of pyq
        '''
        try_times = 0
        while not self.poco(name=self.V['TEXT'],text='删除').exists():
            self.log.debug(f"\n\t —— 长按SOP —— ")
            self.poco.long_click(pos=rect,duration=2)
            try:
                self.poco(name=self.V['TEXT'],text='删除').wait_for_appearance(timeout=self.timeout*2)
                self.poco(name=self.V['TEXT'],text='删除').click()
                self.log.debug(f"\n\t —— 点击'删除' —— ")
                self.poco(name=self.V['CONFIRM_3'],text='确定').wait_for_appearance(timeout=self.timeout*2)
                self.poco(name=self.V['CONFIRM_3'],text='确定').click()
                self.log.debug(f"\n\t —— 点击'确定' —— ")
                self.log.info(f'\n\t —— 删除一条SOP —— ')
                self.task_count += 1
                return True
            except Exception as e:
                self.log.warning(f'\n\t —— Can not delete the SOP msg.{e}.then try again,try times:{try_times}. —— ')
                try_times += 1
                if try_times > 3:
                    self.log.warning(f'\n\t —— Can not delete the SOP msg after {try_times} times try. —— ')
                    return False

    def go_back(self, step='', e='', special_situation='', reply=False):
        '''
        back to last panel.
        '''
        if special_situation:
            self.log.warn(f'\n\t —— {special_situation} —— ')
            if special_situation == '连续三次没找到标签':
                self.no_tag += 1
                self.no_tag_list.append(self.copy_tag)
            elif special_situation == '没有标签对应的客户':
                self.no_customer += 1
                self.no_customer_list.append(self.copy_tag)
        if step and e:
            self.log.error(f'\n\t —— 第{step}步出错:{e} —— ')
            self.task_error += 1
            
        self.log.warn(f'\n\t —— 返回到SOP chatlist —— ')
        timeout = 0
        while not self.poco(name=self.V['SOP']).exists():
            if timeout > 10:
                return False
            try:
                if reply:
                    self.click_reply()
                self.poco(name=self.V['BACK']).click()
                if self.poco(name=self.V['CONFIRM_4'],text='确定').exists():
                    self.poco(name=self.V['CONFIRM_4'],text='确定').click()
            except Exception as e:
                self.log.error(f"\n\t —— Go back error:{e} —— ")
                timeout += 1
        return True

    def click_reply(self):
        '''
        judge if back to jsweb,and click the reply button.
        '''
        if self.dev.get_top_activity_name() == 'com.tencent.wework/.common.web.JsWebActivity':
            try_times = 0
            while True:
                try:
                    self.log.debug("\n\t —— 点击'回执' —— ")
                    air_api.touch(Template(UI_PATH+'\REPLY.png',threshold=0.8))
                    sleep(1)
                except Exception as e:
                    air_api.touch((int(0.87*self.x),int(0.79*self.y)))
                    self.log.debug(f"\n\t —— 点击'回执'失败:{e},尝试坐标点击 —— ")
                try_times += 1
                try:
                    self.screenshot_to_file()
                    cv = CvExercise()
                    ratio, pos_x, pos_y = cv.get_context_contour_w_h_ratio(REPLY_CONTOURS)
                    if ratio > 2:
                        break
                    else:
                        air_api.touch((pos_x,pos_y))
                except Exception as e:
                    self.log.error(f'cv方法识别时出现错误:{e}')
                if try_times > 2:
                    break
            self.update_sop_status(status=3)

    def output_task_data(self):
        '''
        output pyq sop task data.
        '''
        use_time = (str(datetime.now() - self.start_time)[:-7]).split(':')
        msg = f'\t SOP朋友圈任务结束 \
            \n\t 任务用时: {use_time[0]}时{use_time[1]}分{use_time[2]}秒 \
            \n\t 总执行任务条数:{self.task_count} \
            \n\t 成功标签如下:{self.success_list}\
            \n\t 未找到标签的条数:{self.no_tag} \
            \n\t 未找到的标签如下:{self.no_tag_list} \
            \n\t 标签无对应客户条数:{self.no_customer} \
            \n\t 无客户的标签如下:{self.no_customer_list} \
            \n\t 任务进行出错数:{self.task_error}'
        self.log.info(f'{msg}' + '\n\t task-3 end..')
        if self.task_count > 0:
            self.report(msg)

    def check_server(self):
        '''
        check prod/test server from ini file.
        '''
        server = self.get_config_info('server', 'current_server')
        if not server or server == 'SMR-代开发-test':
            self.log.debug(f'\n\t —— Now at test server —— ')
            return 'SMR-代开发-test'
        self.log.debug(f'\n\t —— Now at prod server —— ')
        return server

    def test(self):
        '''
        test
        '''
        print("\n\t start test...")
        self.init_phone()
        self.init_wework()
        self.search_in_chat_panel(text=self.server)
        if not self.open_luoshu_SMR():
            return
        self.find_pyq_customer_sop()
        self.output_task_data()

    def run(self, *args, **kwargs):
        self.init_attributes()
        self.init_wework()
        self.search_in_chat_panel(text=self.server)
        if not self.open_luoshu_SMR():
            return
        self.find_pyq_customer_sop()
        self.output_task_data()

# if __name__ == "__main__":
#     r = Sop()
#     r.test()
