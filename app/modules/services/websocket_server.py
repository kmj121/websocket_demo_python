# ----------- server 端 -----------
import asyncio
import logging
import websockets

logging.basicConfig()

USERS = set()

async def notify_users():
    # 对注册列表内的客户端进行推送
    if USERS: # asyncio.wait doesn't accept an empty list
        message = input('please input:')
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        # 处理客户端数据请求 （业务逻辑）
        async for message in websocket:
            print(message)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
websockets.serve(counter, 'localhost', 6789))
asyncio.get_event_loop().run_forever()

# ----------- client 端 -----------
async def consumer_handler():
    async with websockets.connect(
    'ws://localhost:6789') as websocket:
        async for message in websocket:
            print(message)


asyncio.get_event_loop().run_until_complete(consumer_handler())