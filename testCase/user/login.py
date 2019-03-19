import unittest
import paramunittest
import readConfig as readConfig
from common import common_utils

from common.LogUtil import MyLog
from common.configHttp import ConfigHttp

login_xls = common_utils.get_xls("userCase.xlsx", "login")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, email, password, result, code, msg):
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
        self.email = str(email)
        self.password = str(password)
        self.result = str(result)
        self.code = str(code)
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
        self.logger.info("========"+self.case_name + "开始=======")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common_utils.get_url_from_xml('login')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # get visitor token
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")
        elif self.token == '1':
            token = None

        # set headers
        header = {"token": str(token)}
        configHttp.set_headers(header)
        self.logger.info("第二步：header==>" + str(header))

        # set params
        data = {"email": self.email, "password": self.password}
        configHttp.set_data(data)
        self.logger.info("第三步：参数==>" + str(data))

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
            localReadConfig.set_headers("TOKEN_U", "1212")
        else:
            pass
        self.logger.info("==============测试结束=============")
        self.log.build_case_line(self.case_name, self.info['code'],self.info['msg'])
        self.logger.info("tearDown")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        info1 = self.info
        self.logger.info("code==>"+info1['code'])
        self.logger.info("msg==>"+info1['msg'])
        self.logger.info("result==>"+info1['result'])

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            email = common_utils.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
        self.logger.info("checkResult")