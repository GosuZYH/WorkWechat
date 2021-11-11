import logging
import os
from logging import handlers


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, level='info', when='D', backcount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        ROOT_DIR = os.path.expanduser("..")
        filename = os.path.join(ROOT_DIR, 'task.log')

        self.logger = logging.getLogger(filename)

        format_str = logging.Formatter(fmt)  # 日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 日志级别

        screen_out = logging.StreamHandler()  # 屏幕输出
        screen_out.setFormatter(format_str)  # 屏显格式

        file_out = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backcount,
                                                     encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        file_out.setFormatter(format_str)  # 设置文件里写入的格式

        self.logger.addHandler(screen_out)  # 把对象加到logger里
        self.logger.addHandler(file_out)
