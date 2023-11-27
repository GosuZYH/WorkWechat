# -*- encoding=utf8 -*-
from .base import Base
from .everyweek_task import GroupSendingTask
from .constants import *


class RPAtask(Base):

    def __init__(self):
        self.init_dir()
        super().__init__()
        self.task = GroupSendingTask()
        
    def init_dir(self):
        '''
        make program data，log dir
        '''
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)

        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)
        
        if not os.path.exists(PHOTO_PATH):
            os.mkdir(PHOTO_PATH)

        if not os.path.exists(DB_PATH):
            os.mkdir(DB_PATH)

        if not os.path.exists(RSA_PATH):
            os.mkdir(RSA_PATH)

    def task_loop(self):
        '''
        loop doing task.
        '''
        task = GroupSendingTask()
        task.run_task()

    def pre_run_RPA(self):
        self.task.pre_run()
        
    def run_RPA(self):
        self.pre_run_RPA()
        self.task.run_task()
