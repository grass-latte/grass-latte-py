import threading

import websockets
import asyncio

async def _echo(websocket):
    print(f"New connection: {websocket.remote_address}")
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

async def _start_server():
    server = await websockets.serve(_echo, "localhost", 3030)
    print("Server started at ws://localhost:3030")
    await server.wait_closed()

def run_server_in_background():
    def event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_start_server())

    server_thread = threading.Thread(target=event_loop, daemon=True)
    server_thread.start()