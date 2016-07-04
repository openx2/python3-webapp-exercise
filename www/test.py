import asyncio

import orm
from models import User, Blog, Comment

async def test(loop):
    await orm.create_pool(loop=loop, user='www-data', password='www-data',\
                               db='awesome')

    u = User(name='Michael', email='michael@example.com', passwd='1122334455',\
             image='about:blank')

    await u.save()
    await orm.close_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
