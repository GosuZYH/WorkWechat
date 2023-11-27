import os
import re
import datetime
import logging

from pc_rpa.constants import *

try:
    import codecs
except ImportError:
    codecs = None


class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, level='info', when='D', backcount=3):
        filename = os.path.join(LOG_PATH, 'smr.log')
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.level_relations.get(level))  # 日志级别

        fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        format_str = logging.Formatter(fmt)  # 日志格式

        screen_out = logging.StreamHandler()  # 屏幕输出
        screen_out.setFormatter(format_str)  # 屏显格式

        file_out = MultiprocessHandler(filename=filename, when=when, backupCount=backcount,
                                       encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        file_out.setFormatter(format_str)  # 设置文件里写入的格式

        self.logger.addHandler(screen_out)  # 把对象加到logger里
        self.logger.addHandler(file_out)

        # self.logger.removeHandler(screen_out)
        # self.logger.removeHandler(file_out)

        screen_out.close()
        file_out.close


class MultiprocessHandler(logging.FileHandler):
    """支持多进程的TimedRotatingFileHandler"""

    def __init__(self, filename, when='D', backupCount=5, encoding=None, delay=False):
        """filename 日志文件名,when 时间间隔的单位,backupCount 保留文件个数
        delay 是否开启 OutSteam缓存
            True 表示开启缓存，OutStream输出到缓存，待缓存区满后，刷新缓存区，并输出缓存数据到文件。
            False表示不缓存，OutStrea直接输出到文件"""
        self.backupCount = backupCount
        # 关于获取当日时间的准备工作
        self.when = when.upper()
        # 正则匹配 年-月-日
        self.extMath = r"^\d{4}-\d{2}-\d{2}"
        self.when_dict = {
            'S': "%Y-%m-%d-%H-%M-%S",
            'M': "%Y-%m-%d-%H-%M",
            'H': "%Y-%m-%d-%H",
            'D': "%Y-%m-%d"
        }
        #   # 日志文件日期后缀
        self.time_suffix = datetime.datetime.now().strftime(self.when_dict.get(when))  # datetime.datetime.strptime(str(datetime.datetime.now()), self.when_dict.get(when))
        if not self.time_suffix:
            raise ValueError(u"指定的日期间隔单位无效: %s" % self.when)
        # 获得文件夹路径
        self._dir = os.path.dirname(filename)
        self._base_part = os.path.basename(filename)
        self._base_name, self._base_suffix = self._base_part.split('.')
        self.filePath = os.path.join(self._dir, self._base_name + '_' + self.time_suffix + '.' + self._base_suffix)
        try:
            if not os.path.exists(self._dir):
                os.makedirs(self._dir)
        except Exception:
            print(u"创建文件夹失败")
            print(u"文件夹路径：" + self.filePath)
            pass
        if codecs is None:
            encoding = None
        logging.FileHandler.__init__(self, self.filePath, 'a+', encoding, delay)
        self.getFilesToDelete()

    def shouldChangeFileToWrite(self):
        """更改日志写入目的写入文件
        :return True 表示已更改，False 表示未更改"""
        # 以当前时间获得新日志文件路径
        _filePath = os.path.join(self._dir, self._base_name + '_' + self.time_suffix + '.' + self._base_suffix)
        if _filePath != self.filePath:
            self.filePath = _filePath
            return True
        return False

    def doChangeFile(self):
        """输出信息到日志文件，并删除多于保留个数的所有日志文件"""
        # 日志文件的绝对路径
        self.baseFilename = os.path.abspath(self.filePath)
        if self.stream:
            self.stream.close()
            self.stream = None
        if not self.delay:
            self.stream = self._open()
        if self.backupCount > 0:
            print('删除日志')
            for s in self.getFilesToDelete():
                print(s)
                os.remove(s)

    def getFilesToDelete(self):
        """获得过期需要删除的日志文件"""
        fileNames = os.listdir(self._dir)
        list_keep = []
        for fileName in fileNames:
            _rst = fileName.rsplit('.')
            if isinstance(_rst, list) and len(_rst) > 1:
                _name = _rst[-2]
                _pre = _name[:4]
                _date = _name[-10:]
                if _pre == 'smr_' and re.compile(self.extMath).match(_date):
                    list_keep.append(fileName)
        list_keep.sort(reverse=True)

        if len(list_keep) < self.backupCount:
            list_keep = []
        else:
            list_keep = list_keep[:self.backupCount]
        list_remove = [os.path.join(self._dir, x) for x in fileNames if (x not in list_keep)]
        return list_remove

    def emit(self, record):
        """发送一个日志记录
        覆盖FileHandler中的emit方法，logging会自动调用此方法"""
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
