import unittest
import paramunittest
import readConfig as readConfig
from common import common_utils, configHttp
from common.LogUtil import MyLog

productInfo_xls = common_utils.get_xls("roomCase.xlsx", "getMyRoom")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*productInfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, case_name, method, token, goods_id, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param goods_id:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.goodsId = str(goods_id)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def testGetRoom(self):
        """
        test body
        :return:
        """
        # set uel
        self.url = common_utils.get_url_from_xml('productInfo')
        localConfigHttp.set_url(self.url)
        # set params
        if self.goodsId == '' or self.goodsId is None:
            params = None
        elif self.goodsId == 'null':
            params = {"goods_id": ""}
        else:
            params = {"goods_id": self.goodsId}
        localConfigHttp.set_params(params)
        # set headers
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")
        else:
            token = self.token
        headers = {"token": str(token)}
        localConfigHttp.set_headers(headers)
        # get http
        self.response = localConfigHttp.get()
        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        common_utils.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            goods_id = common_utils.get_value_from_return_json(self.info, "Product", "goods_id")
            self.assertEqual(goods_id, self.goodsId)
        if self.result == '1':
            self.assertEqual(self.info['code'], self.info['code'])
            self.assertEqual(self.info['msg'], self.msg)
