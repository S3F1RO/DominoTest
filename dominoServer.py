#!/usr/bin/python3
import asyncio
import websockets

CLIENTS = set()

async def handler(websocket,path):
    CLIENTS.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Re u : {message}")
            for client in CLIENTS:
                await client.send(message)
    except websockets.ConnectionClosed:
        print ("Client déconnecté")
    finally:
        CLIENTS.remove(websocket)

async def main():
    async with websockets.serve(handler,"localhost",8000):
        print("Serveur Websocket démarré sur ws://localhost:8000")
        await asyncio.Future()

    
if __name__=="__main__":
    asyncio.run(main())