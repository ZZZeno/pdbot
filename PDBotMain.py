__author__ = 'g'
import random
import tweepy
import urllib.parse
import urllib.request
import configparser
from Pixiv import PixivLogin, PixivPicDownloader, PixivRankedPicID
from Twitter import TwProxyGetAuth
import json
import time


def pick_a_pic_from_pixiv(twitter_api: tweepy.API, id_list):
    """
    从P战选取一张图片
    :param twitter_api:Twitter API
    :param id_list: 图片ID列表
    :return:是否成功发送tweet
    """
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
    history.append(id_list[pick][0])
    id_list.remove(id_list[pick])
    f = open('pixiv_history', 'w')
    json.dump(history, f)
    f.close()
    file_name = PixivPicDownloader.download_from_url(p_opener, id_list[pick][0])
    print(file_name)
    if file_name is not None:
        try:
            twitter_api.update_with_media(filename=file_name,
                                          status=PixivPicDownloader.transform_id_to_url(id_list[pick][0]))
        except tweepy.TweepError as e:
            print(e.reason)
            return False
        print('tweet sent!')
        return True
    else:
        return False


def check_pixiv_list(opener: urllib.request.OpenerDirector, tag: str,
                     start_page: int, end_page: int, fav: int, delay: int):
    f_list = open('pixiv_list', 'r')
    id_list = json.load(f_list)
    f_list.close()
    if len(id_list) < 5:
        id_list = PixivRankedPicID.open_page(opener, 'http://www.pixiv.net/search.php?s_mode=s_tag_full&'
                                                     'word='+tag+'&order=date_d&p={0}',
                                             start_page, end_page, fav, delay)
        f_list = open('pixiv_list', 'w')
        json.dump(id_list, f_list)
        f_list.close()
    return id_list


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
username = config['TWITTER']['USERNAME']
password = config['TWITTER']['PASSWORD']
ck = config['TWITTER']['CONSUMER_KEY']
cs = config['TWITTER']['CONSUMER_SECRET']
p_username = config['PIXIV']['USERNAME']
p_password = config['PIXIV']['PASSWORD']
p_tag = urllib.parse.quote(config['PIXIV']['TAG'])
p_start_page = int(config['PIXIV']['START_PAGE'])
p_end_page = int(config['PIXIV']['END_PAGE'])
p_min_fav = int(config['PIXIV']['MIN_FAV'])
p_delay_time = int(config['PIXIV']['DELAY'])
sleep_time = int(config['GENERAL']['SLEEP_TIME'])
api = TwProxyGetAuth.init_oauth(username, password, ck, cs)
p_opener = PixivLogin.login_pixiv(p_username, p_password)
p_id_list = check_pixiv_list(p_opener, p_tag, p_start_page, p_end_page, p_min_fav, p_delay_time)
while 1:
    while not pick_a_pic_from_pixiv(api, p_id_list):
        pass
    p_id_list = check_pixiv_list(p_opener, p_tag, p_start_page, p_end_page, p_min_fav, p_delay_time)
    time.sleep(sleep_time)
