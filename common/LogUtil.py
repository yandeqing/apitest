import json
import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading

localReadConfig = readConfig.ReadConfig()




class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # defined config
        logging.basicConfig(
            format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger()

        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name + " - Code:" + code + " - msg:" + msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log



class LogUtil:
    @staticmethod
    def debug(msg):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.debug(msg)

    @staticmethod
    def info(msg):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info(msg)
    @staticmethod
    def info_jsonformat(msg):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info(json.dumps(msg, ensure_ascii=False,indent=4))



if __name__ == "__main__":
    LogUtil.debug("test debug")
    LogUtil.info("test info")
