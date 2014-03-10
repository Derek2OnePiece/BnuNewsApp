#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All comment operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json
import time

from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuNewsAppServer import dbtools
from BnuNewsAppServer import settings


db = dbtools.DB()


def add_comment_action(request):
    news_id = ObjectId(request.POST['news_id'])
    user_id = ObjectId(request.POST['user_id'])
    msg = request.POST['msg']

    res = {}
    if db.add_comment(news_id, user_id, msg) is not None:
        res['code'] = 0
        res['msg'] = r'评论成功'
    else:
        res['code'] = 0
        res['msg'] = r'评论失败'

    return HttpResponse(json.dumps(res), )

def get_comments_action(request):
    news_id = ObjectId(request.POST['news_id'])
    begin_timestamp = long(request.POST['timestamp'])
    k = int(request.POST['k'])
    
    if begin_timestamp == -1:
        begin_timestamp = time.time()

    raw_comment_list = \
        db.get_k_comments_by_timestamp_news_id(begin_timestamp, news_id, k)
    
    count = raw_comment_list.count()
    comment_list = []
    for raw_comment in raw_comment_list:
        user_id = raw_comment['user_id']
        user_info = db.get_user_info_by_id(user_id)
        if user_info is None:
            res = {'code': 1, 'msg': r'评论加载失败', }
            return HttpResponse(json.dumps(res), )
        
        if 'avater_sub_url' in user_info and \
          user_info['avater_sub_url'] is not None and \
          user_info['avater_sub_url'] != '':
            avater_url = os.path.join(settings.IMAGES_URL_PREFIX, 
                                      r'user_avatar',
                                      user_info['avater_sub_url'])
        else:
            avater_url = ''
        
        comment_list.append({'user_id': str(user_id),
                             'user_name': user_info['name'],
                             'news_id': str(raw_comment['news_id']),
                             'pub_timestamp': raw_comment['pub_timestamp'],
                             'avater_url': avater_url,
                             'msg': raw_comment['msg'], })
    
    res = {'code': 0,
           'count': count,
           'comment_list': comment_list, }    
        
    return HttpResponse(json.dumps(res), )

