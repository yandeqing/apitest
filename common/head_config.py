import codecs
import configparser
import os
import time

from common.LogUtil import MyLog
from common.MD5Util import MD5Util
from readConfig import ReadConfig

config = ReadConfig()
log = MyLog.get_log()


class HeadConfig:
    @staticmethod
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def get_requestParams(http, request_method):
        log.get_logger().info("get_requestParams start")
        if "get" == request_method or "delete" == request_method:
            params = "{}"
        else:
            params = http.data  # type:ConfigHttp
        log.get_logger().info("get_requestParams end" + str(params))
        return str(params)

    @staticmethod
    def get_authorization(http, request_method):
        log.get_logger().info("get_authorization start")
        token = config.get_headers("token")

        timestamp = str(HeadConfig.get_timestamp())
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
        developkey = "developkey=" + config.get_headers("develop_key") + ";"
        log.get_logger().info("get_authorization end")
        return timestampstr + oauth2Str + signatureStr + secret + once + developkey

    @staticmethod
    def create_signature(confighttp, timestamp, request_method):
        log.get_logger().info("create_signature start")
        content = HeadConfig.get_requestParams(confighttp, request_method)
        # type:ConfigHttp
        request_url = "request_url=" + confighttp.url + "&"
        contentstr = "content=" + content + "&"
        request_method = "request_method=" + request_method + "&"
        timestampstr = "timestamp=" + timestamp + "&"
        secret = config.get_headers("secret")
        if secret == '':
            secret = "secret=" + MD5Util.md5s(timestamp) + ";"
        else:
            secret = "secret=" + secret + ";"
        timestampstr_secret = request_url + contentstr + request_method + timestampstr + secret
        log.get_logger().info("create_signature end"+timestampstr_secret)
        return MD5Util.md5s(timestampstr_secret)
