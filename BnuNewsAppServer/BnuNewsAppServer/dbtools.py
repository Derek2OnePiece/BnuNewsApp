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

from bson.objectid import ObjectId


class DB:
    _server_address = "115.28.130.170"
    _port = 27017
    _db_name = "server"

    def __init__(self, address=_server_address, port=_port):
        self.connection = pymongo.Connection(address, port)
        # self.setup_index()

    #===============================================================================
    # base operations
    #===============================================================================
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
        self.get_collection('pubchat').ensure_index([('project_id', 1),
                                                     ('timestamp',
                                                      pymongo.DESCENDING)])
        self.get_collection('todo').ensure_index([('project_id', 1),
                                                  ('pid', 1)])
        self.get_collection('page').ensure_index([('project_id', 1),
                                                  ('user_id', 1),
                                                  ('url', 1)])
        self.get_collection('page').ensure_index([('project_id', 1),
                                                  ('url', 1)], unique=True)
        self.get_collection('tag').ensure_index([('projcet_id', 1), ('user_id', 1),('page_id',1),
                                                   ('tag', 1)], unique=True)
    '''
    #===============================================================================
    # user operations
    #===============================================================================
    def add_user(self, email, password, name, usertype):
        """
        user_id should be a valid email address
        """
        user = {
                'email':email,
                'password':password,
                'name': name,
                'usertype': usertype,
               }
        return self.get_collection('user').insert(user, safe=True)

    def login(self, email, password):
        user = self.get_collection('user').find_one({'email': email, 
                                                     'password': password})
        if user is not None:
            return user['_id']
        else:
            return None
