#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All news operations for backend
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json
import time
import Image

from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuNewsAppServer import dbtools
from BnuNewsAppServer import settings


db = dbtools.DB()

def admin_add_news_action(request):
    news_type = int(request.POST['news_type'])
    title = request.POST['title']
    abstract = request.POST['abstract']
    author = request.POST['author']
    module = int(request.POST['module'])
    
    if 'body' in request.POST and request.POST['body'] != r'':
        body = request.POST['body']
    else:
        body = r''
    # end if
    
    if 'video_target_url' in request.POST \
      and request.POST['video_target_url'] != r'':
        video_target_url = request.POST['video_target_url']
    else:
        video_target_url = r''
    # end if
    
    # inner picture upload
    if 'inner_pic' in request.FILES:
        reqfile = request.FILES['inner_pic']
        image = Image.open(reqfile)
        # image.thumbnail((128,128),Image.ANTIALIAS)
        inner_pic_sub_url = '%s.jpeg' % str(long(time.time()))
        inner_pic_path = os.path.join(settings.IMAGES_PATH,
                                      r'news',
                                      inner_pic_sub_url)
        image.save(inner_pic_path, "jpeg")
    else:
        inner_pic_sub_url = r''
    # end if
    
    news_id = db.admin_add_news(news_type = news_type, 
                                title = title, 
                                abstract = abstract,  
                                author = author, 
                                module = module, 
                                pub_status = 0, 
                                is_delete = 0, 
                                body = body,
                                inner_pic_sub_url = inner_pic_sub_url, 
                                video_target_url = video_target_url)
    res = {}
    if news_id is not None:
        res['code'] = 0
        res['msg'] = r'后台添加新闻成功'
        res['news_id'] = str(news_id)
    else:
        res['code'] = 0
        res['msg'] = r'后台添加新闻失败'
    return HttpResponse(json.dumps(res), )

def admin_get_news_detail_action(request):
    news_id = ObjectId(str(request.GET['news_id']))
    news_detail = db.get_news_detail_by_id(news_id)
    res = {}
    
    if news_detail is not None:
        res['code'] = 0
        res['msg'] = r'获取新闻详情成功'
        res['news_id'] = str(news_detail['_id'])
        res['news_type'] = news_detail['news_type']
        res['title'] = news_detail['title']
        res['abstract'] = news_detail['abstract']
        res['author'] = news_detail['author']
        res['module'] = news_detail['module']
        res['created_timestamp'] = news_detail['created_timestamp']
        res['last_modify_timestamp'] = news_detail['last_modify_timestamp']
        res['pub_timestamp'] = news_detail['pub_timestamp']
        res['pub_status'] = news_detail['pub_status']
        res['body'] = news_detail['body']
        res['video_target_url'] = news_detail['video_target_url']
        if news_detail['inner_pic_sub_url'] != r'':
            res['inner_pic_url'] = \
              os.path.join(settings.IMAGES_URL_PREFIX, r'news',
                           news_detail['inner_pic_sub_url'])
        else:
            res['inner_pic_url'] = r''
    else:
        res['code'] = 1
        res['msg'] = r'获取新闻详情失败'
    
    return HttpResponse(json.dumps(res), )
    

def admin_update_news_action(request):
    news_id = ObjectId(request.POST['news_id'])
    cur_news_detail = db.get_news_detail_by_id(news_id)
    # news_type
    if 'news_type' in request.POST and request.POST['news_type'] is not None:
        news_type = int(request.POST['news_type'])
    else:
        news_type = cur_news_detail['news_type']
    
    # title
    if 'title' in request.POST and request.POST['title'] != '':
        title = request.POST['title']
    else:
        title = cur_news_detail['title']
    
    # abstract
    if 'abstract' in request.POST and request.POST['abstract'] != '':
        abstract = request.POST['abstract']
    else:
        abstract = cur_news_detail['abstract']
         
    # body
    if 'body' in request.POST and request.POST['body'] != '':
        body = request.POST['body']
    else:
        body = cur_news_detail['body']
         
    # author
    if 'author' in request.POST and request.POST['author'] != '':
        author = request.POST['author']
    else:
        author = cur_news_detail['author']
         
    # module
    if 'module' in request.POST and request.POST['module'] is not None:
        module = int(request.POST['module'])
    else:
        module = cur_news_detail['module']
    
    # video_target_url
    if 'video_target_url' in request.POST and request.POST['video_target_url'] != '':
        video_target_url = request.POST['video_target_url']
    else:
        video_target_url = cur_news_detail['video_target_url']
    
    # inner_pic
    if 'inner_pic' in request.FILES:
        reqfile = request.FILES['inner_pic']
        image = Image.open(reqfile)
        # image.thumbnail((128,128),Image.ANTIALIAS)
        inner_pic_sub_url = '%s.jpeg' % str(long(time.time()))
        inner_pic_path = os.path.join(settings.IMAGES_PATH,
                                      r'news',
                                      inner_pic_sub_url)
        image.save(inner_pic_path, "jpeg")
    else:
        inner_pic_sub_url = cur_news_detail['inner_pic_sub_url']
    
    pass


def admin_list_news_action(request):
    start = int(request.GET['start'])
    k = int(request.GET['k'])
    
    raw_news_list = db.admin_get_k_news_by_is_delete(start, k)
    res = {}
    news_list = []
    if raw_news_list is not None:
        for raw_news in raw_news_list:
            news_list.append({'news_id': str(raw_news['_id']),
                              'news_type': raw_news['news_type'],
                              'title': raw_news['title'],
                              'abstract': raw_news['abstract'],
                              'author': raw_news['author'],
                              'created_timestamp': raw_news['created_timestamp'],
                              'last_modify_timestamp': raw_news['last_modify_timestamp'],
                              'pub_timestamp': raw_news['pub_timestamp'],
                              'pub_status': raw_news['pub_status'],
                              })
        # end for
        res['code'] = 0
        res['msg'] = r'加载新闻成功'
        res['count'] = raw_news_list.count()
        res['list'] = news_list
    else:
        res['code'] = 1
        res['msg'] = r'加载新闻失败'
    return HttpResponse(json.dumps(res), )
    

def admin_pub_news_action(request):
    news_id = ObjectId(str(request.POST['news_id']))
    db.admin_update_pub_status(news_id, 1)
    res = {}
    res['code'] = 0
    res['msg'] = r'发布新闻成功'
    res['news_id'] = str(news_id)
    return HttpResponse(json.dumps(res), )

def admin_cancel_pub_news_action(request):
    news_id = ObjectId(str(request.POST['news_id']))
    db.admin_update_pub_status(news_id, 0)
    res = {}
    res['code'] = 0
    res['msg'] = r'发布新闻成功'
    res['news_id'] = str(news_id)
    return HttpResponse(json.dumps(res), )

def admin_delete_news_action(request):
    news_id = ObjectId(str(request.POST['news_id']))
    db.admin_delete_news(news_id)
    res = {}
    res['code'] = 0
    res['msg'] = r'删除新闻成功'
    res['news_id'] = str(news_id)
    return HttpResponse(json.dumps(res), )

        

