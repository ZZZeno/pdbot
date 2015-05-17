__author__ = 'g'
import urllib.request
import urllib.parse
import re
import http.cookiejar

consumer_key = "SnhFgpGEAKCrE2JhaoCw"
consumer_secret = "4H2WJ3CyBOaWpOQv8xkvIekiCzCMSwjWPNLvKOpU"


class UrlAuth:
    def __init__(self, url, username, password):
        """
        构造函数
        :param url: 认证（登录）地址
        :param username: 用户名
        :param password: 密码
        :return:None
        """
        self.access_token = ""
        self.access_token_secret = ""
        self.url = url
        self.auth = None
        self.at = None
        self.ot = None
        self.data = None
        self.username = username
        self.password = password
        self.cookiejar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))

    def get_auth(self):
        """
        进行认证
        :return:获取的PIN码（字符串）
        """
        res = self.opener.open(self.url)
        resstr = str(res.read(), encoding='utf-8')
        at_pattern = re.compile('name="authenticity_token" type="hidden" value="(.*?)">')
        at_match = at_pattern.findall(resstr)
        self.at = at_match[0]
        ot_pattern = re.compile('name="oauth_token" type="hidden" value="(.*?)">')
        ot_match = ot_pattern.findall(resstr)
        self.ot = ot_match[0]
        self.data = urllib.parse.urlencode({
            'authenticity_token': self.at,
            'redirect_after_login': self.url,
            'oauth_token': self.ot,
            'session[username_or_email]': self.username,
            'session[password]': self.password,
        }).encode('utf-8')
        login_res = self.opener.open('https://api.twitter.com/oauth/authorize', self.data)
        login_res_str = str(login_res.read(), encoding='utf-8')
        pin_pattern = re.compile('<kbd aria-labelledby="code-desc"><code>(\d*?)</code></kbd>')
        pin_match = pin_pattern.findall(login_res_str)
        return pin_match[0]
