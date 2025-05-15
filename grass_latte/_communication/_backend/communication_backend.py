import asyncio
import threading
import time

import websockets
from asyncio import Queue, AbstractEventLoop

from websockets.asyncio.server import serve, ServerConnection, Server

from .._interface import SendTypes
from ..._port_range import get_port_range

asyncio_loop: AbstractEventLoop | None = None
server: Server | None  = None
message_queue: Queue[SendTypes] = Queue()
websocket: ServerConnection | None = None
websocket_lock = asyncio.Lock()

async def _send_messages():
    global websocket
    global websocket_lock

    while True:
        message = await message_queue.get()

        while not websocket:
            await asyncio.sleep(0.1)

        async with websocket_lock:
            if websocket_lock:
                try:
                    await websocket.send(message.model_dump_json())
                except websockets.ConnectionClosed:
                    websocket = None

async def _handle_connection(new_websocket: ServerConnection):
    global websocket
    global websocket_lock

    # print(f"New connection: {new_websocket.remote_address}")

    async for message in new_websocket:
        if message != "Hello":
            print("Rejecting new websocket due to invalid handshake")
            return

        async with websocket_lock:
            if websocket is None:
                websocket = new_websocket
            else:
                # print(f"Websocket attempted to connect while existing connection exists. Rejecting.")
                return

        break

    try:
        async for message in websocket:
            print(f"Received message: {message}")
    finally:
        async with websocket_lock:
            websocket = None
            # print("Websocket disconnected")

def _ensure_server_running() -> AbstractEventLoop:
    global server
    global asyncio_loop

    if not asyncio_loop:
        def start_asyncio_loop():
            global asyncio_loop

            try:
                asyncio_loop = asyncio.get_running_loop()
            except RuntimeError:
                background_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(background_loop)
                asyncio_loop = background_loop
                background_loop.run_forever()

        threading.Thread(target=start_asyncio_loop, daemon=True).start()

    if not server:
        while not asyncio_loop:
            time.sleep(0.1)

        async def a_serve():
            global server
            port_range = get_port_range()
            port_used = None
            for p in range(port_range[0], port_range[1] + 1):
                try:
                    server = await serve(_handle_connection, "localhost", p)
                    port_used = p
                    break
                except OSError:
                    continue

            if server is None:
                raise Exception(f"Cannot start websocket server - all ports {port_range[0]}-{port_range[1]} in use")

            asyncio.create_task(server.serve_forever())
            asyncio.create_task(_send_messages())
            # print(f"Server started at ws://localhost:{port_used}")

        asyncio.run_coroutine_threadsafe(a_serve(), asyncio_loop)

    assert asyncio_loop is not None
    return asyncio_loop


def enqueue_send_object(s: SendTypes):
    a_loop = _ensure_server_running()
    asyncio.run_coroutine_threadsafe(message_queue.put(s), a_loop)

