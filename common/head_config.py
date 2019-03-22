import json
import time

from common.LogUtil import MyLog
from common.MD5Util import MD5Util
from common.configHttp import ConfigHttp
from readConfig import ReadConfig


log = MyLog.get_log()


class HeadConfig:
    @staticmethod
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def get_requestParams(http, request_method):
        if "get" == request_method or "delete" == request_method:
            params = "{}"
        else:
            params = json.dumps(http.data)  # type:ConfigHttp
        return params

    @staticmethod
    def get_authorization(http, request_method, timestamp):
        config = ReadConfig()
        token = config.get_headers("token")
        timestampstr = "timestamp=" + timestamp + ";"
        if token == '':
            oauth2Str = "oauth2=" + MD5Util.md5s(timestamp) + ";"
        else:
            oauth2Str = "oauth2=" + token + ";"
        signatureStr = "signature=" + HeadConfig.create_signature(http, timestamp,
                                                                  request_method) + ";"
        if token == '':
            secret = "secret=" + MD5Util.md5s(timestamp) + ";"
        else:
            secret = ""
        once = "once=" + MD5Util.md5s(config.get_headers("client_key")) + timestamp + ";"
        developkey = "developkey=" + config.get_headers("develop_key")
        return timestampstr + oauth2Str + signatureStr + secret + once + developkey

    @staticmethod
    def create_signature(confighttp, timestamp, request_method):

        content = HeadConfig.get_requestParams(confighttp, request_method)
        # type:ConfigHttp
        request_url = "request_url=" + confighttp.path + "&"
        contentstr = "content=" + content + "&"
        request_method = "request_method=" + request_method + "&"
        timestampstr = "timestamp=" + timestamp + "&"
        config = ReadConfig()
        secret = config.get_headers("secret")
        if secret == '':
            secret = "secret=" + MD5Util.md5s(timestamp)
        else:
            secret = "secret=" + secret
        timestampstr_secret = request_url + contentstr + request_method + timestampstr + secret
        return MD5Util.md5s(timestampstr_secret)


if __name__ == '__main__':
    configHttp = ConfigHttp()
    configHttp.set_url("biz/users/login")
    configHttp.set_data({"account": "benlee7@qq.com", "password": "123456", "source": "app"})
    timestamp = "1553137347"
    authorization = HeadConfig.get_authorization(configHttp, "post", timestamp)
    print(authorization)
