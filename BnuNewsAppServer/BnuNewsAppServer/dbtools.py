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
    #
    #==========================================================================
    def add_user(self, email, password, name, usertype, is_admin = 0):
        user = {'email':email,
                'password':password,
                'name': name,
                'usertype': usertype, 
                'is_admin': is_admin, }
        return self.get_collection('user').insert(user, safe=True)

    def check_user_exist_by_email(self, email):
        return self.get_collection('user')\
                 .find_one({'email': email, }) is not None

    def login(self, email, password):
        user = self.get_collection('user').find_one({'email': email, 
                                                     'password': password})
        if user is not None:
            return user['_id']
        else:
            return None
    
    def login_admin(self, email, password):
        pass
    
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
                    'video_target_url': video_target_url, }
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
        

        
        
        
        
        
        
        
        
        
    