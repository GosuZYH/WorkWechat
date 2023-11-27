'''
这里是python获取当前复制内容的四种最优方法 by zyh
'''

import win32clipboard
'''
set clipboard data
'''
# win32clipboard.OpenClipboard()
# win32clipboard.EmptyClipboard()
# win32clipboard.SetClipboardText('testing 123')
# win32clipboard.CloseClipboard()

'''
方法1
get clipboard data
'''
import win32clipboard
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
print("方法1：",data)

'''
方法2
'''
from tkinter import Tk
print('方法2：',Tk().clipboard_get())

'''
方法3
下面的代码用空格替换剪贴板中的所有换行符，然后删除所有双空格，最后将内容保存回剪贴板
'''
import win32clipboard
win32clipboard.OpenClipboard()
c = win32clipboard.GetClipboardData()
win32clipboard.EmptyClipboard()
c = c.replace('\n', ' ')
c = c.replace('\r', ' ')
while c.find(' ') != -1:
    c = c.replace(' ', ' ')
win32clipboard.SetClipboardText(c)
win32clipboard.CloseClipboard()
print('方法3：',c)

'''
方法4
# 先pip install pyperclip
'''
import pyperclip
# pyperclip.copy(s)
s = pyperclip.paste()
print('方法4：',s)