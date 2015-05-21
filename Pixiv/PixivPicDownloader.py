__author__ = 'g'
import re
import urllib.request


def transform_id_to_url(pic_id: str):
    """
    将图片ID转化为图片页面网址
    :return: 图片页面网址
    """
    return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(pic_id)


def download_from_url(opener: urllib.request.OpenerDirector, pic_id: str):
    """
    从图片页面获取图片源地址并下载至/tmp目录
    :return: 下载完成的图片路径
    """
    url = transform_id_to_url(pic_id)
    opener.addheaders = [('Referer', url)]
    try:
        res = str(opener.open(url).read(), encoding='utf-8')
    except Exception as e:
        print(e)
        return None
    pt = re.compile('data-src="(.+?)" class="original-image"')
    pdata = pt.findall(res)
    if len(pdata) == 0:
        print('pic not found')
        return
    print('downloading')
    try:
        pic_data = opener.open(pdata[0]).read()
    except Exception as e:
        print(e)
        print('Cannot download this picture!')
        return None
    f = open('/tmp/{1}.{0}'.format(pdata[0].split('.')[-1], pic_id), 'wb')
    f.write(pic_data)
    f.close()
    print('downloaded')
    return '/tmp/{1}.{0}'.format(pdata[0].split('.')[-1], pic_id)
