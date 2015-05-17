__author__ = 'g'
import re


class RankList:
    def __init__(self, opener, baseurl):
        """
        :param opener:登录器
        :param baseurl:排行榜格式化字符串
        :return:None
        """
        self.baseurl = baseurl
        self.opener = opener

    def open_page(self, start_page, end_page, minfav):
        """
        打开排行榜，获取页面内图片ID
        :param start_page:开始页数
        :param end_page:终止页数
        :param minfav:收藏数阀值
        :return:图片ID列表
        """
        id_list = []
        pattern1 = re.compile('illust_id=(\d+)" class="bookmark-count _ui-tooltip" data-tooltip="(\d+).+?"><i class=')
        for i in range(start_page, end_page+1):
            response = self.opener.open(self.baseurl.format(i))
            if response.getcode() != 200:
                break
            res = str(response.read(), encoding='utf-8')
            print('page {0}'.format(i))
            data = pattern1.findall(res)
            for j in data:
                if int(j[1]) > minfav:
                    id_list.append(j)
        return id_list
