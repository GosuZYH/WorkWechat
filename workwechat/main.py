#!/usr/bin/python
# -*- coding: <encoding utf-8> -*-
import sys
import os
import json
import multiprocessing
import requests

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.password import rsa_encrypt
from ui.ui_main import MyMainWindow, MyLaunchPage
from pc_rpa.constants import pubkey
from m_rpa.constants import DATA_PATH, LOG_PATH, DB_PATH, UI_PATH


"""
    测试url：  'http://test.luoshuscrm.com/'
    正式url：  'https://web.luoshurobot.cn/'
"""
url_basis = 'https://web.luoshurobot.cn/'
url_login = url_basis + 'api/account/v1/login'
url_profile = url_basis + 'api/wecom/user/profile'


class Controller:
    def __init__(self):
        self.init_dir()  # 创建相应路径
        self.ui_main_window = MyMainWindow()
        self.ui_lauch = MyLaunchPage()
        self.ui_main_window.switch_ui_lauch.connect(self.show_ui_lauch)
        self.ui_lauch.switch_ui_main_window.connect(self.show_ui_main_window)

    def init_dir(self):
        '''
        make program data，log dir
        '''
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)

        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)

        if not os.path.exists(DB_PATH):
            os.mkdir(DB_PATH)

        if not os.path.exists(UI_PATH):
            os.mkdir(UI_PATH)

    def show_ui_main_window(self):
        self.ui_main_window.show()
        self.ui_lauch.close()

    def show_ui_lauch(self):
        account_ = self.ui_main_window.accountComboBox.currentText()
        password_ = self.ui_main_window.pwLineEdit.text()
        headers = {"account": account_, "password": password_}
        r = requests.post(url_login, json=headers)
        code_response = json.loads(r.text)["code"]
        if code_response == 200:
            # 如果“记住密码”，则存储如 sqlite
            if self.ui_main_window.remberPwcheckBox.isChecked():
                # 用户名、密码（加密后）写入数据库
                self.ui_main_window.query.exec(
                    "replace into information values('%s', '%s')" % (account_, rsa_encrypt(pubkey, password_)))
                # 用户名写入 Combo Box
                if account_ not in self.ui_main_window.get_all_combobox_items():
                    self.ui_main_window.accountComboBox.addItems([account_])

            self.ui_main_window.statusInfo.setText('')
            # Get 获取用户相关信息
            token = json.loads(r.text)["token"]
            headers = {'Authorization': 'Bearer ' + token}
            try:
                r = requests.get(url_profile, headers=headers)
                dict_r = json.loads(r.text)
                dict_data = dict_r['data']
                user_nickname = dict_data['name']
                user_name = dict_data['name']
                # 	# 判断企微是否在线
                qwx_status = '在线'
                # qwx_pid = get_WXWork_pid()
                # if qwx_pid:
                #     qwx_status = '企微在线'
                user_department = dict_data['departments']
                # 	# 赋值
                self.ui_lauch.qwxNameLabel.setText(user_name)
                self.ui_lauch.welcomeLabel.setText('欢迎使用洛书智能员工')
                self.ui_lauch.nicknameLabel.setText(user_nickname)
                self.ui_lauch.usernameLabel.setText(user_name)
                self.ui_lauch.qwxOnlineLabel.setText(qwx_status)
                self.ui_lauch.departmentLabel.setText(user_department)

                # 处理头像
                avatar_url = dict_data['avatar']
                try:
                    res = requests.get(avatar_url)
                    img = QImage.fromData(res.content)
                    img = img.scaled(self.ui_lauch.avatarLabel.width(),
                                     self.ui_lauch.avatarLabel.height(),
                                     Qt.KeepAspectRatio)
                    self.ui_lauch.avatarLabel.setPixmap(QPixmap.fromImage(img))
                except Exception as e:
                    pass
            except Exception as e:
                pass
            self.ui_main_window.close()
            self.ui_lauch.show()
        else:
            self.ui_main_window.statusInfo.setText('账号或者密码不正确')


if __name__ == "__main__":
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)

    controller = Controller()
    controller.ui_main_window.show()

    sys.exit(app.exec_())
