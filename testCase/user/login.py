import json
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
        config = ReadConfig()
        config.set_headers("token", '')
        config.set_headers("secret", '')

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
        self.logger.info("========开始执行" + self.case_name + "用例=======")
        config = ReadConfig()
        config.set_headers("token", '')
        config.set_headers("secret", '')

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common_utils.get_url_from_xml('login')
        configHttp.set_url(self.url)
        self.logger.info("step1：设置url  " + configHttp.url)

        # set params
        data = {"account": self.account, "password": self.password, "source": "app"}
        configHttp.set_data(data)
        self.logger.info("step2：设置参数==>" + json.dumps(data, ensure_ascii=False))

        # get authorization
        timestamp = str(HeadConfig.get_timestamp())
        authorization = HeadConfig.get_authorization(configHttp, self.method, timestamp)
        # set headers
        header = {"Authorization": authorization,
                  "Terminal": "device_platform=android;app_version=v5.1.0;" +
                              "device_version=7.1.1;device_model=OPPO R11s",
                  "User-Agent": "python_request/OPPO/Android7.1.1/OPPO R11s/app_intversion102516"}
        configHttp.set_headers(header)
        self.logger.info("step3：设置header==>" + json.dumps(header, ensure_ascii=False))
        # test interface
        if self.method == 'post':
            self.return_json = configHttp.postWithJson()
        elif self.method == 'get':
            self.return_json = configHttp.get()

        method = str(self.return_json.request)[int(str(self.return_json.request).find('[')) + 1:int(
            str(self.return_json.request).find(']'))]

        self.logger.info("step4：发送" + method + "请求方法：")
        # check result
        self.logger.info("step5：返回==>" + json.dumps(self.return_json.json(), ensure_ascii=False))
        self.checkResult()

    def tearDown(self):
        """
        执行测试代码后的数据存储
        :return:
        """
        info = self.info
        if info['code'] == 0:
            # set user token to config file
            config = ReadConfig()
            token = info['result']['token']
            secret = info['result']['secret']
            config.set_headers("token", token)
            config.set_headers("secret", secret)

            userlogin = common_utils.get_jsonfrom_file("../../userlogin.json")
            config.set_headers("token", userlogin['token'])
            config.set_headers("secret", userlogin['secret'])
            config.set_headers("uid", userlogin['uid'])

            self.logger.info("step7：执行完毕，保存下一步测试需要用到的数据")
        else:
            pass
        self.logger.info("========执行" + self.case_name + "用例结束=======")

    def checkResult(self):
        self.logger.info("step6：校验结果")
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        if self.code == '0':
            self.assertEqual(self.info['code'], self.code)
        else:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
