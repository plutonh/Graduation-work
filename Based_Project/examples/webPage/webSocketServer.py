import aiohttp
from aiohttp import web, WSCloseCode
import asyncio


async def http_handler(request):
    return web.Response(text="""
<html>
    <head>
        <script>
            const webSocket = new WebSocket("ws://localhost:8000/ws");
            console.log("aaa")
            webSocket.onmessage = (event) => {
                console.log(event)
            }
            const contactServer = () => {
                console.log("Send a message");
                webSocket.send("Initialize");
            }
        </script>
        <body>
            <h1>
                <button onclick="contactServer()">Click Here</button>
            </h1>
        </body>
    </head>
</html>""",
    content_type = 'text/html')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str('some websocket message payload')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

    return ws


def create_runner():
    app = web.Application()
    app.add_routes([
        web.get('/',   http_handler),
        web.get('/ws', websocket_handler),
    ])
    return web.AppRunner(app)


async def start_server(host="localhost", port=8000):
    runner = create_runner()
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()