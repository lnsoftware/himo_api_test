import logging
import time
from logs.logPath import log_path


class Logger(object):
    def __init__(self, logger, CmdLevel=logging.INFO, FileLevel=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)  # 设置日志默认级别为DEBUG
        # fmt = logging.Formatter('%(threadName)s - %(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')  # 设置日志输出格式
        fmt = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')  # 设置日志输出格式
        currTime = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))  # 格式化当前时间
        path = log_path() + '\\'  # 获取当前文件路径
        log_name = path + currTime + logger + '.log'  # 设置日志文件名称
        # log_name = path + currTime + '.log'  # 设置日志文件名称
        # 设置由文件输出
        fh = logging.FileHandler(log_name, encoding='utf-8')  # 采用utf-8字符集格式防止出现中文乱码
        fh.setFormatter(fmt)  # 设置日志输出格式
        fh.setLevel(FileLevel)  # 日志级别为INFO
        # 设置日志由控制台输出
        sh = logging.StreamHandler(log_name)
        sh.setFormatter(fmt)
        sh.setLevel(CmdLevel)
        self.logger.addHandler(fh)  # 添加handler

    def getlog(self):
        return self.logger
