#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cx'

'''
JSON API definition
'''

import json, logging, inspect, functools

class APIError(Exception):
    '''
    The base APIError which contains error(required), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid. The data spectifies the error field of input form.
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data spectifies the resource name.
    '''
    def __init__(self, resource_name, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound',
                                                       resource_name, message)

class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden',
                                                         'permission', message)

class Page(object):
    '''管理页如何显示内容'''

    #参数说明：
    #item_count:要显示的条目数量
    #page_index:要显示的是第几页
    #page_size:每页的条目数量
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        #计算出应该有多少页才能显示全部的条目
        self.page_count = item_count // page_size + (1 if item_count %
                                                     page_size != 0 else 0)
        #如果没有条目或要显示的页超过了总页数
        if item_count == 0 or (page_index > self.page_count):
            #则不显示
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            #否则设置要显示的页
            self.page_index = page_index                #页号
            self.offset = page_size * (page_index - 1)  #从哪个条目开始
            self.limit = page_size                      #这页能显示多少条目
        self.has_next = self.page_size < self.page_count
        self.has_previous = self.page_size > 1

    def __str__(self):
        return 'item count: %s, page count: %s, page index: %s, page size: %s, offset: %s, limit: %s' %\
                (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
