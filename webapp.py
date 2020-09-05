import asyncio
import logging

import aiohttp
from aiohttp import web

import container_manager

log = logging.getLogger('webapp')
log.setLevel(logging.INFO)


async def handle_index(_):
    return web.FileResponse('static/index.html')


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    log = logging.getLogger('ws@' + str(id(ws)))
    log.setLevel(logging.INFO)

    container_pty = None

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if container_pty is None:
                await ws.send_str('Starting Container…')
                container_pty = await container_manager.start_container()

                log.info("Starting Read-Loop")

                async def read_loop():
                    while True:
                        buffer = await container_pty.recv()
                        log.info("Received Data")
                        await ws.send_str(buffer)

                asyncio.create_task(read_loop())

            log.info("Sending Command")
            await container_pty.send(msg.data + "\n")

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    log.info('Disconnected')


def run():
    log.info("Starting")
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_static('/s', 'static')
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/{name}', handle)
    web.run_app(app)
    log.info("Ended")
