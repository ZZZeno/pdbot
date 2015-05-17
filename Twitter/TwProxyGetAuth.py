__author__ = 'g'

import json

import tweepy

from Twitter import TwProxyGetAuthFromUrl

import configparser


def init_oauth(username, password, consumer_key, consumer_secret):
    """
    获取twitter权限
    如果token内已有用户输入的用户名，则直接使用token文件记录的access_token进行认证
    否则使用Oauth代理认证
    :param username: Twitter用户名
    :param password: 密码
    :param consumer_key: Consumer Key
    :param consumer_secret: Consumer Secret
    :return:api
    """

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    database = list()
    try:
        f = open('tokens', 'r')
    except FileNotFoundError:
        f = open('tokens', 'w')
        json.dump(database, f)
        f.close()
        f = open('tokens', 'r')
    database = json.load(f)
    for user in database:
        if username in user:
            access_token = user[1]
            access_token_secret = user[2]
            break
    f.close()

    if len(access_token) <= 0:
        getua = TwProxyGetAuthFromUrl.UrlAuth(auth.get_authorization_url(), username, password)
        token = getua.get_auth()
        auth.get_access_token(token)
        database.append([username, auth.access_token, auth.access_token_secret])
        f = open('tokens', 'w')
        json.dump(database, f)
        f.close()
    else:
        auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    print('Auth succeeded')
    return api
