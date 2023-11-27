import os
import sys
import site
import uuid
import configparser
# 生成ConfigParser对象
config = configparser.ConfigParser()
# 读取配置文件
filename = r'config\config.ini'
config.read(filename, encoding='gbk')

def set_config(env):
    if env == '1':
        config.set('robot', 'api', 'https://oapi.dingtalk.com/robot/send?access_token=d75d46bd7fc71e16cea996c55a7ad7b360889e9e2ad13b4b0801e95c2d4a9c73')
        config.set('robot', 'alarm_api', 'https://oapi.dingtalk.com/robot/send?access_token=fab23a991f3380eb228c98851ddc37623cdf998a20f59f1ac2d798a8b3828747')
        config.set('server', 'current_server', 'SMR-代开发-test')
    else:
        config.set('robot', 'api','https://oapi.dingtalk.com/robot/send?access_token=66d3ecb14759ade5f861540310f327512cbe7ac5fbbd5205cb2ea0cfc13f3927')
        config.set('robot', 'alarm_api','https://oapi.dingtalk.com/robot/send?access_token=bb57903a51a93489081bcce9b03689277b7594bb264780a2bf448ced0c5b6153')
        config.set('server', 'current_server', '洛书SMR')
    config.write(open(filename, 'w'))

env = str(input('请选择环境,如果是正式服直接按回车,如果是测试服请输入"1"然后按回车'))
set_config(env)

print("Please input your version-name(Pressing enter appends the UUID):")
version_name = sys.stdin.readline().strip()
if version_name == '':
    version_name = uuid.uuid4()

dirname = os.path.split(os.path.abspath(sys.argv[0]))

cv2_path = site.getsitepackages()[1] + r'\cv2;.\cv2'
airtest_path = site.getsitepackages()[1] + r'\airtest;.\airtest'
poco_path = site.getsitepackages()[1] + r'\poco;.\poco'
config_path = os.path.join(os.getcwd(), 'config' + r';.\config')
dist_path = r'packaging\dist'
build_path = r'packaging\build'
spec_path = r'packaging\spec'
tools_path = r'packaging\tools'
ico_path = dirname[0] + r'\packaging\assets\appx128.ico'

cmd = 'pyinstaller --onedir --clean --noconfirm --noconsole --noupx \
--add-data %s \
--add-data %s \
--add-data %s \
--add-data %s \
--distpath %s \
--workpath %s \
--specpath %s \
--upx-dir %s \
--name SMR_RPA-%s \
--icon %s main.py' %(
    cv2_path,
    airtest_path,
    poco_path,
    config_path,
    dist_path,
    build_path,
    spec_path,
    tools_path,
    version_name,
    ico_path)

# --onedir/onefile  程序文件夹/单exe形式
# print(cmd)
os.system(cmd)
config.set('robot', 'api', 'https://oapi.dingtalk.com/robot/send?access_token=d75d46bd7fc71e16cea996c55a7ad7b360889e9e2ad13b4b0801e95c2d4a9c73')
config.set('robot', 'alarm_api', 'https://oapi.dingtalk.com/robot/send?access_token=fab23a991f3380eb228c98851ddc37623cdf998a20f59f1ac2d798a8b3828747')
config.set('server', 'current_server', 'SMR-代开发-test')

