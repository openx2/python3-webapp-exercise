#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cx'

import time, uuid

from orm import Model,StringField,FloatField,TextField,BooleanField

def next_id():
    '''根据当前时间和随机生成的uuid来给对象一个id'''
    return '%015d%s000' % (int(time.time()*1000), uuid.uuid4().hex)

class User(Model):
    '''用户表，有id,email,密码,用户名,头像,帐号创建时间,是否为管理员的属性'''
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    create_at = FloatField(default=time.time)

class Blog(Model):
    '''博客表，有id,用户id,用户名,头像,标题,概览,内容,创建时间的属性'''
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    create_at = FloatField(default=time.time)

class Comment(Model):
    '''评论表，有id,用户id,博客id,用户名,头像,内容,创建时间的属性'''
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    create_at = FloatField(default=time.time)
