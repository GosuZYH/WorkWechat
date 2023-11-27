#!/usr/bin/python
# -*- coding: <encoding utf-8> -*-
from time import sleep
import multiprocessing

from PyQt5 import QtSql
from PyQt5.QtWidgets import QLineEdit, QShortcut, QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon, QMouseEvent, QKeySequence
from PyQt5 import QtCore, QtGui
from airtest.core.android.adb import ADB

from ui import UiMainWindow
from ui import UiLaunch
from ui.password import rsa_decrypt
from pc_rpa import RPAtask
from m_rpa import MRPAtask
from pc_rpa.constants import prikey
from m_rpa.constants import DB_PATH


class MyMainWindow(QMainWindow, UiMainWindow):
    switch_ui_lauch = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        # 开始即启动数据库
        self.create_db()
        # 实例化一个查询对象（必须放在 self.create_db() 之后）
        self.query = QtSql.QSqlQuery()
        # 创建一个数据库表
        self.query.exec_("create table information("
                         "name varchar(20) primary key, password varchar(100))")

        # 控件 Layout
        self.setupUi(self)
        # 	# 补充设置
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.remberPwcheckBox.setStyleSheet("QCheckBox::indicator"
                                            "{"
                                            "border: 1px solid rgb(217, 217, 217);"
                                            "border-radius: 3px;"
                                            "}"
                                            "QCheckBox::indicator:checked"
                                            "{"
                                            "background-color : rgb(13, 197, 166);"
                                            "}")
        self.setWindowIcon(QIcon(":/登录页面/logo.png"))
        # 事件 - 槽函数
        self.loginPushButton.clicked.connect(self.go_ui_lauch)
        self.loginPushButton.setShortcut(QtCore.Qt.Key_Return)

        self.minButton.clicked.connect(self.min_window)
        self.closeButton.clicked.connect(self.close_window)
        self.remberPwcheckBox.setEnabled(True)
        list_init = self.get_all_names_db()
        try:
            self.accountComboBox.activated.connect(self.choose_combo_item)
        except Exception:
            pass

        self.accountComboBox.addItems(list_init)
        self.accountComboBox.setEditText('')
        self.accountComboBox_all_items = list_init

        #    # 默认输入提示
        self.edit = QLineEdit(self)
        self.edit.setStyleSheet("background-color:rgb(242, 242, 242); border-radius:4px;")
        self.edit.setPlaceholderText('请输入账号')
        self.edit.textChanged.connect(self.show_password_when_typing)

        # LineEdit 初始化
        self.accountComboBox.setLineEdit(self.edit)
        self.pwLineEdit.setText('')

        QShortcut(QKeySequence(self.tr("Enter")), self, self.loginPushButton.click)

    def show_password_when_typing(self):
        if self.edit.text() in self.get_all_combobox_items():
            try:
                password = self.get_password_db(self.edit.text())
                if password:
                    self.pwLineEdit.setText(password)
            except Exception as e:
                pass

    def get_all_combobox_items(self):
        all_items = [self.accountComboBox.itemText(i) for i in range(
            self.accountComboBox.count())]
        return all_items

    def choose_combo_item(self):
        name = self.accountComboBox.currentText()
        try:
            password = self.get_password_db(name)
            if password:
                self.pwLineEdit.setText(password)
        except Exception as e:
            pass

    def get_all_names_db(self):
        q = self.query
        sql_code = 'select name from information'
        list_name = []
        if q.exec(sql_code):
            age_index = q.record().indexOf('name')
            while q.next():
                list_name.append(self.tr(q.value(age_index)))
        return list_name

    @staticmethod
    def get_password_db(name):
        q = QtSql.QSqlQuery()
        sql_code = 'select password from information where name=%s' % name
        if q.exec(sql_code):
            age_index = q.record().indexOf('password')
            password = None
            while q.next():
                password = q.value(age_index)
            return rsa_decrypt(prikey, password)
        else:
            return None

    def create_db(self):
        # 添加一个sqlite数据库连接并打开
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(DB_PATH + '\Info.db')
        db.open()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def go_ui_lauch(self):
        self.switch_ui_lauch.emit()

    def min_window(self):
        self.showMinimized()

    def close_window(self):
        self.close()
        adb = ADB()
        adb.kill_server()


class MyLaunchPage(QMainWindow, UiLaunch):
    switch_ui_main_window = QtCore.pyqtSignal()
    signal_start_smr_execute_phone = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyLaunchPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('洛书')
        self.setWindowIcon(QIcon(":/登录页面/logo.png"))
        self.BackToMainButton.clicked.connect(self.go_ui_main_window)

        self.StartSMRButton_Phone.clicked.connect(self.launch_fuc_phone)
        self.signal_start_smr_execute_phone.connect(self.slot_launch_fuc_phone)

        QShortcut(QKeySequence(self.tr("alt+W")), self, self.slot_launch_fuc_phone)

    # self.StartSMRButton.clicked.connect(self.launch_fuc)
    # self.signal_start_smr_execute.connect(self.slot_launch_fuc)

    # QShortcut(QKeySequence(self.tr("alt+Q")), self, self.slot_launch_fuc)

    def go_ui_main_window(self):
        self.switch_ui_main_window.emit()
        adb = ADB()
        adb.kill_server()

    def launch_fuc(self):
        self.signal_start_smr_execute.emit()

    @staticmethod
    def pctask(q):
        PCRPA = RPAtask()
        q.put(PCRPA.run_RPA())

    @staticmethod
    def mtask(q):
        MPRA = MRPAtask()
        if MPRA.is_connect:
            q.put_nowait('yes')
            q.put(MPRA.run())
        else:
            q.put_nowait('no')

    def launch_fuc_phone(self):
        self.signal_start_smr_execute_phone.emit()

    def slot_launch_fuc_phone(self):
        global p
        if self.StartSMRButton_Phone.text() == '执行器开启运行' or self.StartSMRButton_Phone.text() == '执行器开启运行(请连接设备！)':
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=self.mtask, name='mrpa', args=(q,))
            p.daemon = True  # 解决点击右上角关闭界面但子线程仍在运行
            p.start()
            times = 0
            while True:
                str = '正在连接到设备'
                for _ in range(4):
                    self.StartSMRButton_Phone.setText(str)
                    QApplication.processEvents()
                    str = str + '.'
                    sleep(0.5)
                times += 1
                if times > 5: break
            if q.get() == 'no':
                self.StartSMRButton_Phone.setText('执行器开启运行(请连接设备！)')
                QApplication.processEvents()
                p.kill()
            else:
                self.StartSMRButton_Phone.setText('执行器停止运行')
                QApplication.processEvents()
        else:
            self.StartSMRButton_Phone.setText('执行器开启运行')
            QApplication.processEvents()
            if p:
                p.kill()
                adb = ADB()
                adb.kill_server()

    def slot_launch_fuc(self):
        global p
        if self.StartSMRButton.text() == '开启运行':
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=self.pctask, name='pcrpa', args=(q,))
            p.daemon = True
            p.start()
            self.StartSMRButton.setText('停止运行')
        else:
            self.StartSMRButton.setText('开启运行')
            if p:
                p.kill()

    def launch_fuc_phone(self):
        self.signal_start_smr_execute_phone.emit()

    @staticmethod
    def show_message(msg=''):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        info.setWindowTitle('友情提示')
        info.setText(msg)
        info.setWindowIcon(QIcon(":/登录页面/logo.png"))
        info.addButton("知道了", QMessageBox.AcceptRole)
        info.exec_()

    def closeEvent(self, event):
        self.close()
        adb = ADB()
        adb.kill_server()
