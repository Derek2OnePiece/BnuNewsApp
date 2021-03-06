#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All user operations for backend
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import json

from django.http import HttpResponse

from BnuNewsAppServer import dbtools


db = dbtools.DB()

def login_action(request):
    email = request.POST['email']
    password = request.POST['password']
    
    user = db.login_admin(email, password)
    
    res = {}
    if user is not None:
        res['code'] = 0
        res['msg'] = r'登陆成功'
        res['user_id'] = str(user['_id'])    
    else:
        res['code'] = 1
        res['msg'] = r'登陆失败'
        
    return HttpResponse(json.dumps(res), )

def get_user_summary_action(request):
    res = {}
    res['code'] = 0
    res['msg'] = r'获取用户统计数据成功'
    res['reg_user_count'] = 145
    res['reg_user_summary_file_url'] = r'appserver/admin/file/dd.md' 
    
    return HttpResponse(json.dumps(res), )