# -*- encoding=utf8 -*-
__author__ = "26579"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Windows:///",])


# script content
print("start...")
touch(Template(r"tpl1636621188099.png", record_pos=(0.189, -0.097), resolution=(1920, 1080)))


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)