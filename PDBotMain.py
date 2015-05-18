__author__ = 'g'
import random
import time
import tweepy
import urllib.parse
import configparser
from Pixiv import PixivLogin, PixivPicDownloader, PixivRankedPicID
from Twitter import TwProxyGetAuth
import json


def get_pixiv_opener(pixiv_username, pixiv_password):
    """
    获取pixiv登录器
    :param pixiv_username: pixiv用户名
    :param pixiv_password: 密码
    :return:urllib.opener
    """
    p_login = PixivLogin.LoginPixiv(pixiv_username, pixiv_password)
    pixiv_opener = p_login.get_opener()
    return pixiv_opener


def get_pivix_list(pixiv_opener, tag: str, start_page: int, end_page: int, min_fav: int, delay: int):
    """
    获取图片ID列表
    :param pixiv_opener: opener
    :param tag: 标签
    :param start_page: 开始页数
    :param end_page: 终止页数
    :param min_fav: 收藏数阀值
    :param delay: 页面间处理延时
    :return:图片ID列表
    """
    tag = urllib.parse.quote(tag)
    rank_list = PixivRankedPicID.RankList(pixiv_opener, 'http://www.pixiv.net/search.php?s_mode=s_tag_full&'
                                                        'word='+tag+'&order=date_d&p={0}')
    pixiv_id_list = rank_list.open_page(start_page, end_page, min_fav, delay)
    return pixiv_id_list


def pick_a_pic_from_pixiv(twitter_api: tweepy.API, id_list):
    """
    从P战选取一张图片
    :param twitter_api:Twitter API
    :param id_list: 图片ID列表
    :return:是否成功发送tweet
    """
    history = []
    try:
        f = open('pixiv_history', 'r')
    except FileNotFoundError:
        f = open('pixiv_history', 'w')
        json.dump(history, f)
        f.close()
        f = open('pixiv_history', 'r')
    history = json.load(f)
    f.close()
    pick = random.randint(0, len(id_list) - 1)
    while id_list[pick][0] in history:
        id_list.remove(id_list[pick])
        f = open('pixiv_list', 'w')
        json.dump(id_list, f)
        f.close()
        if len(id_list) == 0:
            print('Pictures all sent!')
            exit(0)
        pick = random.randint(0, len(id_list) - 1)
    print(id_list[pick])
    dl = PixivPicDownloader.PixivDownload(p_opener, id_list[pick][0])
    history.append(id_list[pick][0])
    id_list.remove(id_list[pick])
    f = open('pixiv_history', 'w')
    json.dump(history, f)
    f.close()
    file_name = dl.start()
    print(file_name)
    if file_name is not None:
        twitter_api.update_with_media(filename=file_name, status=dl.get_url())
        print('tweet sent!')
        print(time.time())
        return True
    else:
        return False


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
username = config['TWITTER']['USERNAME']
password = config['TWITTER']['PASSWORD']
ck = config['TWITTER']['CONSUMER_KEY']
cs = config['TWITTER']['CONSUMER_SECRET']
p_username = config['PIXIV']['USERNAME']
p_password = config['PIXIV']['PASSWORD']
p_tag = config['PIXIV']['TAG']
p_start_page = int(config['PIXIV']['START_PAGE'])
p_end_page = int(config['PIXIV']['END_PAGE'])
p_min_fav = int(config['PIXIV']['MIN_FAV'])
p_delay_time = int(config['PIXIV']['DELAY'])
sleep_time = int(config['GENERAL']['SLEEP_TIME'])
api = TwProxyGetAuth.init_oauth(username, password, ck, cs)
p_opener = get_pixiv_opener(p_username, p_password)
p_id_list = []
try:
    f_list = open('pixiv_list', 'r')
except FileNotFoundError:
    f_list = open('pixiv_list', 'w')
    json.dump(p_id_list, f_list)
    f_list.close()
    f_list = open('pixiv_list', 'r')
p_id_list = json.load(f_list)
f_list.close()
if len(p_id_list) < 5:
    p_id_list = get_pivix_list(p_opener, p_tag, p_start_page, p_end_page, p_min_fav, p_delay_time)
    f_list = open('pixiv_list', 'w')
    json.dump(p_id_list, f_list)
    f_list.close()
while len(p_id_list) > 0:
    while not pick_a_pic_from_pixiv(api, p_id_list):
        pass
    time.sleep(sleep_time)
