__author__ = 'g'
import re


class PixivDownload:
    def __init__(self, opener, picid):
        """
        构造函数，根据图片ID下载P站图片
        :param opener: 登录器
        :param picid: 图片ID（字符串）
        :return:None
        """
        self.opener = opener
        self.url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(picid)
        self.id = picid
        self.opener.addheaders = [('Referer', self.url)]

    def start(self):
        """
        线程开始，下载图片
        :return:None
        """
        res = str(self.opener.open(self.url).read(), encoding='utf-8')
        pt = re.compile('data-src="(.+?)" class="original-image"')
        pdata = pt.findall(res)
        if len(pdata) == 0:
            print('pic not found')
            return
        print('downloading')
        f = open('/tmp/{1}.{0}'.format(pdata[0].split('.')[-1], self.id), 'wb')
        f.write(self.opener.open(pdata[0]).read())
        f.close()
        print('downloaded')
        return '/tmp/{1}.{0}'.format(pdata[0].split('.')[-1], self.id)

    def get_url(self):
        return self.url
