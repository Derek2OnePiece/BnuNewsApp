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
    email = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    user_type = request.POST['usertype']
    
    # username should be email
    # TODO
    
    user_id = db.add_user(email, password, name, user_type)
    
    res = {}
    res['userid'] = str(user_id)
    res['username'] = email
    res['user_type'] = user_type
    res['name'] = name
    
    if user_id is not None:
        res['code'] = 0
        res['msg'] = r'注册成功'

    else:
        res['code'] = 1
        res['msg'] = r'注册失败'
        
    return HttpResponse(json.dumps(res), )

def login_action(request):
    email = request.POST['username']
    password = request.POST['password']
    
    res = {}
    
    user = db.login(email, password)

    if user is not None:
        res['code'] = 0
        res['msg'] = r'login success'
        res['userid'] = str(user['_id'])
        res['username'] = user['email']
        res['user_type'] = user['user_type']
        res['name'] = user['name']
    else:
        res['code'] = 1
        res['msg'] = r'login error'
        
    return HttpResponse(json.dumps(res), )


def update_user_profile_action(request):
    user_id = ObjectId(request.POST['user_id'])
    phone = ''
    if 'phone' in request.POST:
        phone = request.POST['phone']
    sid = ''
    if 'sid' in request.POST:
        sid = request.POST['sid']
    gender = 0
    if 'gender' in request.POST:
        gender = request.POST['gender']
    signature = ''
    if 'signature' in request.POST:
        signature = request.POST['signature']
    
    if 'avatar_image' in request.FILES:
    
        reqfile = request.FILES['avatar_image']
        image = Image.open(reqfile)
        image.thumbnail((64,64),Image.ANTIALIAS)
        avater_sub_url = '%s.jpeg' % str(user_id)
        avater_path = os.path.join(settings.IMAGES_PATH, 
                                   r'user_avatar',
                                   avater_sub_url)
        image.save(avater_path,"jpeg")
        
    else:
        avater_sub_url = r'0.jpeg'
    
    db.update_user_profile(user_id, avater_sub_url, phone, sid, gender, signature)
    res = {}
    res['code'] = 0
    res['msg'] = r'update success'
    res['userid'] = str(user_id)

        
    return HttpResponse(json.dumps(res), )
