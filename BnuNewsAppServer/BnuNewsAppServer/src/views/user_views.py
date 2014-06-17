#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All user operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json

from PIL import Image
from django.http import HttpResponse
from bson.objectid import ObjectId

from BnuNewsAppServer import dbtools
from BnuNewsAppServer import settings

db = dbtools.DB()


def register_action(request):
    email = request.POST['email']
    password = request.POST['password']
    name = request.POST['name']
    user_type = request.POST['user_type']
    
    # username must be email
    # TODO
    res = {}
    if db.check_user_exist_by_email(email):
        res['code'] = 1
        res['msg'] = r'邮箱已被注册'
        return HttpResponse(json.dumps(res), )
    # end if
    
    user_id = db.add_user(email, password, name, user_type)
    
    if user_id is not None:
        res['code'] = 0
        res['msg'] = r'注册成功'
        res['user_id'] = str(user_id)
        res['email'] = email
        res['name'] = name
        res['user_type'] = user_type
    else:
        res['code'] = 1
        res['msg'] = r'注册失败'
        
    return HttpResponse(json.dumps(res), )

def login_action(request):
    email = request.POST['email']
    password = request.POST['password']
    
    user = db.login(email, password)
    
    res = {}
    if user is not None:
        res['code'] = 0
        res['msg'] = r'登陆成功'
        res['user_id'] = str(user['_id'])
        res['email'] = user['email']
        res['user_type'] = user['user_type']
        res['name'] = user['name']
        res['phone'] = user['phone']
        res['sid'] = user['sid']
        res['gender'] = user['gender']
        res['signature'] = user['signature']
        if user['avatar_sub_url'] != r'':
            res['avatar_url'] = os.path.join(settings.IMAGES_URL_PREFIX, 
                                             r'user_avatar',
                                             user['avatar_sub_url'])
        else:
            res['avatar_url'] = r''        
    else:
        res['code'] = 1
        res['msg'] = r'登陆失败'
        
    return HttpResponse(json.dumps(res), )


def update_user_profile_action(request):
    user_id = ObjectId(request.POST['user_id'])
    cur_user_info = db.get_user_info_by_id(user_id)
    # name
    if 'name' in request.POST and request.POST['name'] != r'':
        name = request.POST['name']
    else:
        name = cur_user_info['name']
    # user_type
    if 'user_type' in request.POST and request.POST['user_type'] != r'':
        user_type = request.POST['user_type']
    else:
        user_type = cur_user_info['user_type']    
    # phone
    if 'phone' in request.POST and request.POST['phone'] != r'':
        phone = request.POST['phone']    
    else:
        phone = cur_user_info['phone']
    # sid
    if 'sid' in request.POST and request.POST['sid'] != r'':
        sid = request.POST['sid']
    else:
        sid = cur_user_info['sid']
    # gender
    if 'gender' in request.POST and request.POST['gender'] is not None:
        gender = int(request.POST['gender'])    
    else:
        gender = cur_user_info['gender']    
    # signature
    if 'signature' in request.POST and request.POST['signature'] != r'':
        signature = request.POST['signature']    
    else:
        signature = cur_user_info['signature']
    # avatar_sub_url
    if 'avatar_image' in request.FILES:
        reqfile = request.FILES['avatar_image']
        image = Image.open(reqfile)
        image.thumbnail((128,128),Image.ANTIALIAS)
        avatar_sub_url = '%s.jpeg' % str(user_id)
        avatar_path = os.path.join(settings.IMAGES_PATH, 
                                   r'user_avatar',
                                   avatar_sub_url)
        image.save(avatar_path, "jpeg")
    else:
        avatar_sub_url = cur_user_info['avatar_sub_url']
    
    db.update_user_profile(user_id = user_id, 
                           name = name,
                           user_type = user_type,
                           avatar_sub_url = avatar_sub_url,
                           phone = phone, 
                           sid = sid, 
                           gender = gender, 
                           signature = signature)
    res = {}
    res['code'] = 0
    res['msg'] = r'更新用户资料成功'
    res['user_id'] = str(user_id)
    
    return HttpResponse(json.dumps(res), )
