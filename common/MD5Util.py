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
    print(MD5Util.md5s("request_url=client/search/bed&content={}&request_method=get&timestamp=1553134668&secret=96771f552ced7e3d54603d29cd266f9b;"))
    dt = '2019-01-01 10:40:30'
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    print(ts)
