#!/usr/bin/python3
import asyncio
import websockets
import random

CLIENTS = set()

class GameState:
    def __init__(self):
        self.players=[]
        self.hands = {}
        self.board = []
        self.turn_index = 0
        self.boneyard = []

def generate_domino_set():
    dominos = []
    for i in range(7):
        for j in range(i,7):
            dominos.append((i,j))
    random.shuffle(dominos)
    return dominos
    
async def handler(websocket,path):
    CLIENTS.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Reçu : {message}")
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