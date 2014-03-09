#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All comment operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import json

from django.http import HttpResponse

from BnuNewsAppServer import dbtools


db = dbtools.DB()


def register_action(request):
    print request.POST
    email = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    usertype = request.POST['usertype']
    
    # username should be email
    # TODO
    
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

def login_action(request):
    email = request.POST['username']
    password = request.POST['password']
    
    res = {}
    
    user_id = db.login(email, password)

    if user_id is not None:
        res['code'] = 0
        res['msg'] = r'login success'
        res['userid'] = str(user_id)
    else:
        res['code'] = 1
        res['msg'] = r'login error'
        res['userid'] = str(user_id)
        
    return HttpResponse(json.dumps(res), )

