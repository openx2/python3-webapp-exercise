#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''async webapp'''

#导入日志包,并设置输出日志的级别为INFO
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, time, os
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

import orm
from config import configs
from coroweb import add_routes, add_static
from middlewares import logger_factory, response_factory

def init_jinja2(app, **kw):
    '''得到所需的jinja2配置，进行初始化'''
    logging.info('init jinja2...')
    #初始化模板配置，包括模板运行代码的开始结束标识符，变量的开始结束标识符
    options = dict(
        #自动转义，将变量中的<>&等字符转换为&lt;&gt;&amp;等
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        #Jinja2会在使用Template时检查模板文件的状态，如果模板有修改则重新加载模板。
        #如果对性能要求较高，可以将此值设为False
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')
    logging.info('set jinja2 template path: %s' % path)
    #Environment是Jinja2中的一个核心类，它的实例用来保存配置、全局对象，以及从本地文件系统或其它位置加载模板。
    #这里把要加载的模板和配置传给Environment，生成Environment实例
    env = Environment(loader=FileSystemLoader(path), **options)
    #filters: 一个字典描述的filters过滤器集合，如果非模板被加载时，可以安全添加或移除filters
    filters = kw.get('filters', None)
    if filters is not None:
        env.filters.update(filters)
    app['__templating__'] = env

def datetime_filter(t):
    '''确定如何显示时间的过滤器'''
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta) // 60
    if delta < 86400:
        return u'%s小时前' % (delta) // 3600
    if delta < 604800:
        return u'%s天前' % (delta) // 86400
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

#启动服务器
async def init(loop):
    #创建数据库连接池
    await orm.create_pool(loop=loop,**configs.db)
    #创建能处理1次HTTP请求的应用，loop为处理请求的协程，添加中间件
    app = web.Application(loop=loop,
                         middlewares=[logger_factory, response_factory])
    #初始化jinja2框架
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    #添加请求的handlers，即各请求相应的处理函数
    add_routes(app, 'handlers')
    #加载静态文件所在地址
    add_static(app)
    #通过应用创建处理请求的句柄
    handler = app.make_handler()
    #利用loop实例化app的协程处理，主机名为localhost，端口号为9000
    srv = await loop.create_server(handler, 'localhost', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    #创建结果集，以便在外界正常关闭服务器
    rs = { 'app': app, 'srv': srv, 'handler': handler }
    return rs

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    rs = loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        #停止接受新客户端进行连接
        rs['srv'].close()
        loop.run_until_complete(rs['srv'].wait_closed())
        #执行Application.shutdown()事件
        loop.run_until_complete(rs['app'].shutdown())
        #关闭已经接受的连接，60.0s被视为一个合理的超时等待值
        loop.run_until_complete(rs['handler'].finish_connections(60.0))
        #通过Application.clearup()调用注册的应用终结器(finalizer)
        loop.run_until_complete(rs['app'].cleanup())
        #关闭数据库连接池
        loop.run_until_complete(orm.close_pool())
    loop.close()
