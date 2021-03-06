import json

import requests
import readConfig as readConfig
from common.LogUtil import  MyLog

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.path = None
        self.files = {}
        self.state = 0

    def set_url(self, path):
        """
        set url
        :param: interface url
        :return:
        """
        self.path=path
        self.url = scheme + '://' + host + "/"+path

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data
        # get authorization
        from common.head_config import HeadConfig
        timestamp = str(HeadConfig.get_timestamp())
        authorization = HeadConfig.get_authorization(self, "post", timestamp)
        # set headers
        header = {"Authorization": authorization,
                  "Terminal": "device_platform=android;app_version=v5.1.0;" +
                              "device_version=7.1.1;device_model=OPPO R11s",
                  "User-Agent": "python_request/OPPO/Android7.1.1/OPPO R11s/app_intversion102516"}
        self.set_headers(header)


    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params,
                                    timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params,
                                     data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data,
                                     files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data,
                                     timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


if __name__ == "__main__":
    print("ConfigHTTP")
