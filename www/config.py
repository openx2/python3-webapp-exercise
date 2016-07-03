#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Configuration
'''

__author__ = 'cx'

import config_default

class Dict(dict):
    '''支持以x.y方式访问元素内容的字典'''

    def __init__(self, name=(), values=(), **kw):
        super(Dict,self).__init__(**kw)
        self.update(zip(name, values))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    '''用override中的值替换defaults中键一样的值'''
    r = {}
    for k,v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    '''将内置的dict类型对象转为自定义的Dict类型'''
    D = Dict()
    for k,v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
