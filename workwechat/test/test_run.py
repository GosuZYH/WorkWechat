from subprocess import Popen
import os
import sys

name_script = "../workwechat/main.py"

# os.system('python %s'% name_script)
p = Popen("python %s" % name_script)