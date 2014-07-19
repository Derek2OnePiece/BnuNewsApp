#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All mongodb operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import pymongo
import time

from datetime import datetime
from bson.objectid import ObjectId


class DB:
    _server_address = "115.28.130.170"
    _port = 27017
    _db_name = "server"

    def __init__(self, address=_server_address, port=_port):
        self.connection = pymongo.Connection(address, port)
        # self.setup_index()

    #==========================================================================
    # base operations
    #==========================================================================
    def get_db(self, name=_db_name):
        return self.connection[name]

    def get_collection(self, name):
        return self.get_db()[name]
    '''
    def setup_index(self):
        """
        ensure index according to data model
        should be called only once before any of the methods is invoked
        """
        self.get_collection('query').ensure_index([('project_id', 1),
                                                     ('user_id', 1),
                                                     ('timestamp',
                                                      pymongo.DESCENDING)])
        self.get_collection('query').ensure_index([('projcet_id', 1), ('user_id', 1),
                                                   ('keyword', 1)], unique=True)
        self.get_collection('notification').ensure_index([('project_id', 1),
                                                          ('user_id', 1),
                                                          ('type', 1),
                                                          ('recommend_help_type', 1),
                                                          ('timestamp',
                                                           pymongo.DESCENDING)])
    '''
    #==========================================================================
    # user operations
    #
    #    _id
    #    email           || int       ||
    #    password        || int       ||
    #    name            || string    || 昵称
    #    user_type       || string    || 0-学生；1-校友；2-教师
    #    is_admin        || int       || 默认0；0-普通用户；1-管理员
    #    avater_sub_url  || string    || 头像文件相对路径
    #    phone           || string    ||
    #    sid             || string    || 学号 or 教师号
    #    gender          || int       || 默认0；0-male；1-female
    #    signature       || string    || 个性签名
    #    reg_timestamp   || long      || 注册时间
    #
    #==========================================================================
    
    # TODO
    # store password encoded
    def add_user(self, 
                 email, 
                 password, 
                 name, 
                 user_type, 
                 is_admin = 0,
                 avatar_sub_url = r'', 
                 phone = r'', 
                 sid = r'',
                 gender = 0, 
                 signature = r''):
        user = {'email':email,
                'password':password,
                'name': name,
                'user_type': user_type, 
                'is_admin': is_admin, 
                'avatar_sub_url': avatar_sub_url, 
                'phone': phone,
                'sid': sid,
                'gender': gender,
                'signature': signature,
                 'reg_timestamp':  long(time.time()), }
        return self.get_collection('user').insert(user)

    def check_user_exist_by_email(self, email):
        return self.get_collection('user')\
                 .find_one({'email': email}) is not None

    def login(self, email, password):
        return self.get_collection('user').find_one({'email': email, 
                                                     'password': password})
    
    def login_admin(self, email, password):
        return self.get_collection('user').find_one({'email': email,
                                                     'password': password,
                                                     'is_admin': 1})
    
    def get_user_info_by_id(self, user_id):
        return self.get_collection('user').find_one({'_id': user_id})
    
    def update_user_profile(self, user_id, name, user_type, avatar_sub_url, 
                            phone, sid, gender, signature):
        return self.get_collection('user')\
            .update({'_id': user_id},
                    {'$set': {'name': name,
                              'user_type': user_type,
                              'avatar_sub_url': avatar_sub_url,
                              'phone': phone,
                              'sid': sid,
                              'gender': gender,
                              'signature': signature }})
    
    #==========================================================================
    # news operations
    #
    #    _id
    #    news_type                || int       || 0-article；1-video
    #    title                    || string    ||
    #    abstract                 || string    || 摘要 less than 20 words
    #    author                   || string    || 用于显示的作者
    #    module                   || int       || 版块id > 0
    #    created_timestamp        || long      || 
    #    last_modify_timestamp    || long      ||
    #    pub_timestamp            || long      ||
    #    pub_status               || int       || 默认0；0-未发布； 1-发布
    #    is_delete                || int       || 默认0；0-不删除； 1-删除
    #    delete_timestamp         || long      ||
    #    body                     || string    || 
    #    inner_pic_sub_url        || string    || 文章配图的链接地址
    #    video_target_url         || string    ||
    #
    #==========================================================================
    def admin_add_news(self, 
                       news_type, 
                       title, 
                       abstract,
                       author,
                       module, 
                       pub_status = 0, 
                       is_delete = 0,
                       body = r'',
                       inner_pic_sub_url = r'',
                       video_target_url = r''):   
        timestamp = long(time.time())
        raw_news = {'news_type': news_type,
                    'title': title,
                    'abstract': abstract,
                    'author': author,
                    'module': module,
                    'created_timestamp': timestamp,
                    'last_modify_timestamp': timestamp, 
                    'pub_timestamp': None,
                    'pub_status': pub_status,
                    'is_delete': is_delete,
                    'delete_timestamp': None,
                    'body': body,
                    'inner_pic_sub_url': inner_pic_sub_url,
                    'video_target_url': video_target_url, }
        return self.get_collection('news').insert(raw_news)
    
    def admin_get_news_info_by_id(self, news_id):
        return self.get_collection('news').find_one({'_id': news_id})
    
    def admin_update_news_detail(self, ):
        pass
    
    def admin_update_pub_status(self, news_id, pub_status):
        timestamp = long(time.time())
        return self.get_collection('news')\
            .update({'_id': news_id},
                    {'$set': {'pub_status': pub_status,
                              'pub_timestamp': timestamp,
                              'last_modify_timestamp': timestamp, }})
    
    def admin_delete_news(self, news_id):
        timestamp = long(time.time())
        return self.get_collection('news')\
            .update({'_id': news_id},
                    {'$set': {'pub_status': 0,
                              'is_delete': 1,
                              'delete_timestamp': timestamp,
                              'last_modify_timestamp': timestamp, }})
    
    def admin_get_k_news_by_is_delete(self, start, k):
        return self.get_collection('news')\
                 .find({'is_delete': 0})\
                 .sort('last_modify_timestamp', pymongo.DESCENDING)\
                 .skip(start).limit(k)
    
    def get_k_news_by_timestamp_pub_status_module(self, cur_timestamp,
                                                  module, pub_status, k = 5):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'module': module,
                        'pub_timestamp': {'$lte': cur_timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .limit(k)
    
    def get_k_news_by_timestamp_pub_status(self, cur_timestamp, 
                                           pub_status, k = 1):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'pub_timestamp': {'$gte': cur_timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .limit(k)
                 
    def get_news_count_by_timestamp_module(self, timestamp, module):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'module': module,
                        'pub_timestamp': {'$gte': timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .count()
                 
    def get_news_detail_by_id(self, news_id):
        return self.get_collection('news').find_one({'_id': news_id})
      
    #==========================================================================
    # comment operations
    #
    #    _id                
    #    user_id            || ObjectId      || 发布者id
    #    news_id            || ObjectId      || 关联的新闻id
    #    pub_timestamp      || long          || 发布时间
    #    msg                || string        ||
    #
    #==========================================================================
    def add_comment(self, 
                    news_id, 
                    user_id, 
                    msg):
        comment = {'user_id': user_id,
                   'news_id': news_id,
                   'pub_timestamp': long(time.time()),
                   'msg': msg, }
        return self.get_collection('comments').insert(comment)
    
    def get_k_comments_by_timestamp_news_id(self, begin_timestamp, news_id, k):
        return self.get_collection('comments')\
            .find({'news_id': news_id,
                   'pub_timestamp': {'$lte': begin_timestamp}})\
            .sort('pub_timestamp', pymongo.DESCENDING).limit(k)
    
    def get_comment_count_by_news_id(self, news_id):
        return self.get_collection('comments')\
                 .find({'news_id': news_id})\
                 .count()

        
        
        
        
        
        
        
        
        
    