__author__ = 'g'

import urllib.request
import urllib.parse
import http.cookiejar


def login_pixiv(username: str, password: str):
    """
    登录Pixiv.net
    :return: OpenerDirector
    """
    url = 'https://www.secure.pixiv.net/login.php'
    form_data = urllib.parse.urlencode({
        'mode': 'login',
        'pixiv_id': username,
        'pass': password,
        'skip': '1'
    }).encode('utf-8')
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    try:
        opener.open(url, form_data)
    except Exception as e:
        print(e)
        print('Network error.')
        exit(0)
    return opener
