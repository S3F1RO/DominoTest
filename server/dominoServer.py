#!/usr/bin/python3
import asyncio
import websockets
import random

CLIENTS = set()
id=0
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
    
async def handler(websocket):
    CLIENTS.add(websocket)
    global id
    id+=1
    print("Client connected")
    if len(CLIENTS) > 2:
        #create party
        dominos = generate_domino_set()
        for i in range(len(CLIENTS)):
            players.append(i)
            hand[i]=dominos[i*7:(i+1)*7]
        boneyard=[dominos[len(CLIENTS)]]
        game = GameState(players,hands,[],0,boneyard)
        await websocket.send("Clients connectés, démarrer le jeu...")

    try:
        async for message in websocket:
            # print(f"Reçu : {message}")
            for client in CLIENTS:
                await client.send(message)
    except websockets.ConnectionClosed:
        print ("Client déconnecté")
    finally:
        CLIENTS.remove(websocket)

async def main():
    async with websockets.serve(handler,"",8000): # Qui peut se connecter à moi
        print("Serveur Websocket démarré sur ws://localhost:8000")
        await asyncio.Future()

    
if __name__=="__main__":
    asyncio.run(main())