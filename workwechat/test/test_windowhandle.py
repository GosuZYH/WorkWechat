#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import win32gui
from airtest.aircv import *

title='企业微信'    
handlers = []
win32gui.EnumWindows(lambda handle, param: param.append(handle), handlers)
time.sleep(0.1)
target_handlers = []
for handler in handlers:
    title = win32gui.GetWindowText(handler)
    print(title)
    print(handler)
    if title =='企业微信':
        print('OK')
        break