__author__ = 'g'
import re
import threading
import urllib.request


class AsyncDownload(threading.Thread):
    def __init__(self, i, ext, link, page, baseurl):
        """
        D站图片下载进程
        :param i: 图片ID
        :param ext:图片后缀名
        :param link:图片相对路径
        :param page:页数
        :param baseurl:上级地址
        :return:None
        """
        threading.Thread.__init__(self)
        self.i = i
        self.ext = ext
        self.link = link
        self.page = page
        self.baseurl = baseurl

    def run(self):
        """
        开始下载图片
        :return:None
        """
        f = open('data/kancolle/page{2}-{0}.{1}'.format(self.i, self.ext, self.page), 'wb')
        f.write(urllib.request.urlopen(self.baseurl+self.link).read())
        f.close()
        print('{0}.{1} on page {2} downloaded'.format(self.i, self.ext, self.page))


def getpage(pageurl, baseurl, page):
    """
    打开页面，下载页面内分数大于阀值的图片
    :param pageurl: 页面地址格式化字符串
    :param baseurl: 站点地址
    :param page: 页数
    :return:None
    """
    resstr = urllib.request.urlopen(pageurl).read().decode()
    pscore = re.compile('data-score="(\d+)"')
    mscore = pscore.findall(resstr)
    pext = re.compile('data-file-ext="(.+)"')
    mext = pext.findall(resstr)
    pdata = re.compile('data-file-url="(.+)"')
    mdata = pdata.findall(resstr)
    dl = []
    for i, score, ext, link in zip(range(1, len(mscore)), mscore, mext, mdata):
        if int(score) >= 10:
            dl.append(AsyncDownload(i, ext, link, page,  baseurl))
    for i in dl:
        i.start()
        print('downloading {0}.{1} on page {2}'.format(i.i, i.ext, i.page))
    for i in dl:
        i.join()

if __name__ == '__main__':
    url = 'https://danbooru.donmai.us/posts?page={0}&tags=kancolle'
    burl = 'https://danbooru.donmai.us'
    for x in range(1, 21):
        getpage(url.format(x), burl, x)
