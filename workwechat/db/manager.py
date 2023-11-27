#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import functools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .constants import DB_PATH


class DbManager:
    __instance = None
    __engine = None

    def __new__(cls, *args, **kwargs):
        
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def db_session(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with DbManager().session as s:
                return func(self, session=s, *args, **kwargs)

        return wrapper

    @staticmethod
    def gen_engine():
        PATH = os.path.join(DB_PATH, "weworktask" + ".db")
        if not DbManager.__engine:
            engine = create_engine(
                "sqlite:///%s" % PATH,
                connect_args={'check_same_thread': False}, echo=True)
            DbManager.__engine = engine
        return DbManager.__engine

    @property
    def session(self):
        DbManager.gen_engine()
        s = sessionmaker(bind=DbManager.__engine)
        return s()

if __name__ == '__main__':
    pass