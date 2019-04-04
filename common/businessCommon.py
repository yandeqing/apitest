import json

import readConfig as readConfig
from common import common_utils
from common.LogUtil import LogUtil
from common.configHttp import ConfigHttp

localReadConfig = readConfig.ReadConfig()
localConfigHttp = ConfigHttp()
localLogin_xls = common_utils.get_xls("userCase.xlsx", "login")


# login
def loginBiz():
    """
    login
    :return: token
    """
    # set url
    url = common_utils.get_url_from_xml('login')
    localConfigHttp.set_url(url)
    config = readConfig.ReadConfig()
    config.set_headers("token", '')
    config.set_headers("secret", '')
    # set params
    account = localLogin_xls[4][3]
    password = localLogin_xls[4][4]
    data = {"account": account, "password": password, "source": "app"}
    localConfigHttp.set_data(data)
    LogUtil.info("step2：设置参数==>" + json.dumps(data, ensure_ascii=False))

    # login
    response = localConfigHttp.postWithJson().json()

    LogUtil.info_jsonformat(response)
    token = common_utils.get_value_from_return_json(response, "result", "token")
    secret = common_utils.get_value_from_return_json(response, "result", "secret")
    config.set_headers("token", token)
    config.set_headers("secret", secret)


# login
def loginCient():
    """
    login
    :return: token
    """
    # login
    response = common_utils.get_jsonfrom_file("../userlogin.json")
    LogUtil.info_jsonformat(response)
    token = response["token"]
    secret = response["secret"]
    uid = response["uid"]
    LogUtil.info(token)
    LogUtil.info(secret)
    config = readConfig.ReadConfig()
    config.set_headers("token", token)
    config.set_headers("secret", secret)
    config.set_headers("uid", uid)


# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = common_utils.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header
    header = {'token': token}
    localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()


# login
def getMyRoom():
    """
    login
    :return: token
    """
    # set url
    url = common_utils.get_url_from_xml('get_my_room')
    if "{uid}" in url:
        config = readConfig.ReadConfig()
        uid = config.get_headers('uid')
        if uid is None:
            url = url.replace("{uid}", "")
        else:
            url = url.replace("{uid}", uid)
    LogUtil.info(url)
    localConfigHttp.set_url(url)


if __name__ == '__main__':
    loginCient()
    getMyRoom()
