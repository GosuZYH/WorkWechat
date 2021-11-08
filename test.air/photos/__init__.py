# -*- encoding=utf8 -*-
__author__ = "26579"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Windows:///67706",])


# script content
print("start...")
touch(Template(r"tpl1636363446580.png", record_pos=(-0.297, -0.099), resolution=(848, 650)))
touch(Template(r"tpl1636364477995.png", record_pos=(-0.318, -0.335), resolution=(848, 650)))



# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
