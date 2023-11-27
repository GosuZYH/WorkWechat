#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#==============================================================================
#     FileName: models.py
#      License: MIT
#   LastChange: 2021/7/15 15:34
#    CreatedAt: 2021/7/15 15:34
#==============================================================================
"""
from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.schema import ForeignKey

from .manager import DbManager

Base = declarative_base(bind=DbManager().gen_engine())


def init_db_data():
    Base.metadata.create_all()


class Soplog(Base):
    __tablename__ = 'soplog'
    __describe__ = 'sop发送记录表'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    soptime = Column(DateTime,default=None)
    soptag = Column(String,default=None)
    status = Column(Integer,default=None)      # 1.no republiced 2.not replied 3.replied 4.deleted
    notag = Column(Integer,default=None)

class SopTag(Base):
    __tablename__ = 'soptag'
    __describe__ = 'sop标签页码记录表'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    soptag = Column(String,default=None)
    page = Column(Integer,default=None)
