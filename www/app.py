#!/usr/bin/env python
#导入日志包,并设置输出日志的级别为INFO
import logging; logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web

#接受一个Request实例并返回一个Response实例的Handler
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

#启动服务器
async def init(loop):
    #创建能处理1次HTTP请求的应用，loop为处理请求的协程
    app = web.Application(loop=loop)
    #给app添加路径映射，把'/'映射到index函数上处理
    app.router.add_route('GET', '/', index)
    #通过应用创建处理请求的句柄
    handler = app.make_handler()
    #利用loop实例化app的协程处理，主机名为localhost，端口号为9000
    srv = await loop.create_server(handler, 'localhost', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    #创建结果集，以便在外界正常关闭服务器
    rs = { 'app': app, 'srv': srv, 'handler': handler }
    return rs

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
loop.close()
