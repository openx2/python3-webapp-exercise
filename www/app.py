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
    #利用loop实例化app的协程处理，主机名为localhost，端口号为9000
    srv = await loop.create_server(app.make_handler(), 'localhost', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    #返回的server目前没有使用，但可以在服务器退出时用到
    return srv

loop = asyncio.get_event_loop()
srv = loop.run_until_complete(init(loop))
#主要问题是loop在连接都确定退出前就关闭了，报RuntimeError
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    srv.close()
    loop.run_until_complete(srv.wait_closed())
loop.close()
