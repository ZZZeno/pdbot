__author__ = 'g'

import urllib.request
import urllib.parse
import http.cookiejar


class LoginPixiv:
    def __init__(self, username, password):
        """
        构造函数
        :param username:用户名
        :param password: 密码
        :return:构造登录器
        """
        self.url = 'https://www.secure.pixiv.net/login.php'
        self.data = urllib.parse.urlencode({
            'mode': 'login',
            'pixiv_id': username,
            'pass': password,
            'skip': '1'
        }).encode('utf-8')
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.opener.open(self.url, self.data)

    def get_cookie_jar(self):
        """
        获取登录成功后的cookie
        :return:
        """
        return self.cj

    def get_opener(self):
        """
        获取登录器
        :return:登录器
        """
        return self.opener
