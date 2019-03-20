import hashlib
import time


class MD5Util:

    @staticmethod
    def md5s(strs):
        m = hashlib.md5()
        m.update(strs.encode("utf8"))
        return m.hexdigest()


if __name__ == '__main__':
    print(int(time.time()))
    print(MD5Util.md5s("34038092649035HOUSEPHP58"))
    dt = '2019-01-01 10:40:30'
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    print(ts)
