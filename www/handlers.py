#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cx'

from coroweb import get, post
from models import User

@get('/')
def index(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
