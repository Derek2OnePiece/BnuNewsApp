#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All news operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json
import time

from datetime import datetime
from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuNewsAppServer import dbtools
from BnuNewsAppServer import settings


db = dbtools.DB()


def add_news_action(request):
    title = request.POST['title']
    body = request.POST['body']
    author = request.POST['author']


    """
    user_id = db.add_user(email, password, name, usertype)
    
    res = {}
    res['userid'] = str(user_id)
    res['username'] = email
    res['usertype'] = usertype
    res['name'] = name
    
    if user_id is not None:
        res['code'] = 0
        res['msg'] = r'注册成功'

    else:
        res['code'] = 1
        res['msg'] = r'注册失败'
        
    return HttpResponse(json.dumps(res), )
    """

def list_news_action(request):
    req_timestamp = long(request.POST['timestamp'])
    module_id = request.POST['module']
    k = int(request.POST['k'])
    
    if req_timestamp == -1:
        start_timestamp = time.time()
    else:
        start_timestamp = req_timestamp
    
    raw_news_list = \
      db.get_k_news_by_timestamp_pub_status_module(start_timestamp, 
                                                   module_id, 
                                                   pub_status = 1, 
                                                   k = k)
    count = raw_news_list.count()
    news_list = []
    for raw_news in raw_news_list:
        inner_pic_url = os.path.join(settings.IMAGES_URL_PREFIX, 
                                     r'news',
                                     raw_news['inner_pic_sub_url'])
        news_list.append({'news_id': str(raw_news['_id']),
                          'news_type': raw_news['news_type'],
                          'title': raw_news['title'],
                          'abstract': raw_news['abstract'],
                          'module': raw_news['module'],
                          'pub_timestamp': raw_news['pub_timestamp'],
                          'inner_pic_sub_url': inner_pic_url,
                          'video_target_url': raw_news['video_target_url'], })
    
    res = {}
    res['code'] = 0
    res['msg'] = r'加载成功'
    res['count'] = count
    res['list'] = news_list
    return HttpResponse(json.dumps(res), )

def get_news_detail_action(request):
    raw_news_id = request.POST['news_id']
    news_id = ObjectId(raw_news_id)
    
    raw_news_detail = db.get_news_detail_by_id(news_id)
    
    res = {}
    
    if raw_news_detail is not None:
        res['code'] = 0
        res['msg'] = r'news detail'
        res['news_id'] = str(raw_news_detail['_id'])
        res['title'] = raw_news_detail['title']
        res['abstract'] = raw_news_detail['abstract']
        res['body'] = raw_news_detail['body']
        res['author'] = raw_news_detail['author']
        res['module'] = raw_news_detail['module']
        res['pub_timestamp'] = raw_news_detail['pub_timestamp']
        res['inner_pic_sub_url'] = os.path.join(
          settings.IMAGES_URL_PREFIX, r'news', 
          raw_news_detail['inner_pic_sub_url'])
        res['video_target_url'] = raw_news_detail['video_target_url']
        res['comment_cout'] = 10
    else:
        res['code'] = 1
        res['msg'] = r'获取页面详情失败'
    return HttpResponse(json.dumps(res), )
        
        
    
    
    
    
    
    

        
    


