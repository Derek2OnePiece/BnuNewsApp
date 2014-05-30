#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created: 2014-01-17
#
# All revision operations
#
__author__ = 'Derek (Jing Luo), luojing.derek@gmail.com'
__pychecker__ = 'no-callinit no-classattr'

import os
import json

from django.http import HttpResponse
from BnuNewsAppServer import dbtools
from BnuNewsAppServer import settings


db = dbtools.DB()


def get_revision_action(request):
    settings.IMAGES_URL_PREFIX
    res = {}
    res['code'] = 0
    res['msg'] = r'获取最新版本信息成功'
    res['revision_no'] = int(settings.REVISION_NO)
    res['revision_msg'] = settings.REVISION_MSG
    res['reps_url'] = os.path.join(settings.REPO_URL_PREFIX, 
                                   settings.REVISION_FILE)

    return HttpResponse(json.dumps(res), )
    
