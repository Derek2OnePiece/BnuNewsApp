#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All user operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import json
import string

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from BnuNewsAppServer import dbtools


db = dbtools.DB()


def register_action(request):
    user_id = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    usertype = request.POST['usertype']
    
    is_succ = db.add_user(user_id, password, username, usertype)
    
    res = []
    
    if is_succ:
        res.append({'code': 0,
                    'msg': r'注册成功',
                    'user_id': user_id, }) 
    else:
        res.append({'code': 1,
                    'msg': r'注册失败',
                    'user_id': user_id, })
    return HttpResponse(json.dumps(res), )
    

