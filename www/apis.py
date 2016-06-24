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
