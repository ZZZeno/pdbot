__author__ = 'g'
import re
import time
import urllib.request


def open_page(opener: urllib.request.OpenerDirector, base_url: str,
              start_page: int, end_page: int, min_fav: int, delay: int):
    """
    打开排行榜，获取页面内收藏数大于阀值的图片ID所构成的列表
    :param base_url: 排行榜地址（页面参数格式化）
    :return: 元素为[图片ID,收藏数]的列表
    """
    id_list = []
    pattern1 = re.compile('illust_id=(\d+)" class="bookmark-count _ui-tooltip" data-tooltip="(\d+).+?"><i class=')
    for i in range(start_page, end_page+1):
        response = opener.open(base_url.format(i))
        if response.getcode() != 200:
            break
        res = str(response.read(), encoding='utf-8')
        print('page {0}'.format(i))
        data = pattern1.findall(res)
        for j in data:
            if int(j[1]) > min_fav:
                id_list.append(j)
        time.sleep(delay)
    return id_list
