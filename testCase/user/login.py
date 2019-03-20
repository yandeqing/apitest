import unittest
import paramunittest

from common import common_utils
from common.LogUtil import MyLog
from common.configHttp import ConfigHttp
from common.head_config import HeadConfig
from readConfig import ReadConfig

login_xls = common_utils.get_xls("userCase.xlsx", "login")
configHttp = ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, account, password, result, code, msg):
        """
        setParameters
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param password:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.account = str(account)
        self.password = str(password)
        self.result = str(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.logger.info("========" + self.case_name + "开始=======")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common_utils.get_url_from_xml('login')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + configHttp.url)


        # set params
        data = {"account": self.account, "password": self.password, "source": "app"}
        configHttp.set_data(data)
        self.logger.info("第二步：参数==>" + str(data))

        # get authorization
        authorization = HeadConfig.get_authorization(configHttp, self.method)
        # set headers
        header = {"Authorization": authorization,
                  "Terminal": "device_platform=android;app_version=v5.1.0;" +
                              "device_version=7.1.1;device_model=OPPO R11s",
                  "User-Agent": "python_request/OPPO/Android7.1.1/OPPO R11s/app_intversion102516"}
        configHttp.set_headers(header)
        self.logger.info("第三步：header==>" + str(header))

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('[')) + 1:int(
            str(self.return_json.request).find(']'))]
        self.logger.info("第四步：发送" + method + "请求方法：")
        # check result
        self.logger.info("第五步：返回==>" + str(self.return_json.json()))
        self.checkResult()

    def tearDown(self):
        """
        执行测试代码后的数据存储
        :return:
        """
        info = self.info
        if info['code'] == 0:
            # set user token to config file
            config = ReadConfig.Config()
            config.set_headers("TOKEN_U", "1212")
        else:
            pass
        # self.log.build_case_line(self.case_name, self.info['code'],self.info['msg'])
        self.logger.info("tearDown end")
        self.logger.info("==============测试结束=============")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.logger.info("checkResult start")
        self.info = self.return_json.json()
        if self.code == '0':
            self.assertEqual(self.info['code'], self.code)
        else:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
        self.logger.info("checkResult end")
