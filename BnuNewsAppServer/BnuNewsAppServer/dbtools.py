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
    #    email
    #    password
    #    name
    #    user_type
    #    is_admin               || 默认0
    #    avater_sub_url         ||
    #    phone
    #    sid
    #    gender                 || 0: male
    #    signature
    #
    #
    #==========================================================================
    def add_user(self, email, password, name, user_type, is_admin = 0):
        user = {'email':email,
                'password':password,
                'name': name,
                'user_type': user_type, 
                'is_admin': is_admin, 
                'avater_sub_url': None, 
                'phone': '',
                'sid': '',
                'gender': 0,
                'signature': '', }
        return self.get_collection('user').insert(user, safe=True)

    def check_user_exist_by_email(self, email):
        return self.get_collection('user')\
                 .find_one({'email': email}) is not None

    def login(self, email, password):
        return self.get_collection('user').find_one({'email': email, 
                                                     'password': password})

    
    def login_admin(self, email, password):
        pass
    
    def get_user_info_by_id(self, user_id):
        return self.get_collection('user').find_one({'_id': user_id})
    
    def update_user_profile(self, user_id, avater_sub_url = r'0.jpeg', 
                            phone = '', sid = '', gender = 0, signature = ''):
        return self.get_collection('user')\
            .update({'_id': user_id},
                    {'$set': {'avater_sub_url': avater_sub_url,
                              'phone': phone,
                              'sid': sid,
                              'gender': gender,
                              'signature': signature}})
    
    #==========================================================================
    # news operations
    #
    #    _id
    #    news_type                ||   0：article 1：video
    #    title
    #    abstract                 ||   摘要 less than 20 words
    #    body
    #    author
    #    module                   ||   模块
    #    created_timestamp        ||
    #    last_modify_timestamp    ||
    #    pub_timestamp
    #    pub_status               ||   0：发布； 1：未发布
    #    inner_pic_sub_url
    #    is_delete                ||   0: 不删除； 1：删除
    #    video_target_url         ||
    #    comments
    #        user_id              ||
    #        msg                  ||
    #        submit_timestamp     ||
    #
    #==========================================================================
    def add_news(self, news_type, title, abstract, body, author,
                 module, pub_status = 0, is_delete = 0,
                 inner_pic_sub_url = None,
                 video_target_url = None):
        # timestamp = datetime.now()   
        timestamp = long(time.time())
        raw_news = {'news_type': news_type,
                    'title': title,
                    'abstract': abstract,
                    'body': body,
                    'author': author,
                    'module': module,
                    'created_timestamp': timestamp,
                    'last_modify_timestamp': timestamp, 
                    'pub_timestamp': timestamp,
                    'pub_status': pub_status,
                    'is_delete': is_delete,
                    'inner_pic_sub_url': inner_pic_sub_url,
                    'video_target_url': video_target_url, 
                    'comments': [], }
        return self.get_collection('news').insert(raw_news)
    
    def update_pub_timestamp(self,):
        pass
    
    def update_pub_status(self, ):
        pass
    
    def update_is_delete_status(self,):
        pass
    
    def update_inner_pic_sub_url(self,):
        pass
    
    def get_k_news_by_timestamp_pub_status_module(self, cur_timestamp,
                                                        module, 
                                                        pub_status = 1,
                                                        k = 5):
        return self.get_collection('news')\
                 .find({'pub_status': 1,
                        'pub_timestamp': {'$lte': cur_timestamp}})\
                 .sort('pub_timestamp', pymongo.DESCENDING)\
                 .limit(k)
    
    def get_news_detail_by_id(self, news_id):
        return self.get_collection('news').find_one({'_id': news_id})
    
    """
    def get_comments_by_news_id(self, news_id):
        raw_news =  self.get_collection('news').find_one({'_id': news_id})
        if raw_news is not None:
            return raw_news['comments']
        else:
            return None
    
    def add_comment(self, news_id, user_id, msg):
        exist = self.get_collection('news').find_one({'_id': news_id}) != None
        if exist:
            return self.get_collection('news')\
            .update({'_id': news_id},
                    {'$push': {'comments': {'user_id': user_id, 'msg': msg}}})
        else:
            return False
    """    
    #==========================================================================
    # comment operations
    #
    #    _id                      ||
    #    user_id                  ||
    #    news_id                  ||
    #    pub_timestamp            ||
    #    msg                      ||
    #
    #==========================================================================
    def add_comment(self, news_id, user_id, msg):
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

        
        
        
        
        
        
        
        
        
    