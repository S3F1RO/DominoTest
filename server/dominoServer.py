#!/usr/bin/python3
import asyncio
import websockets
import random
import json
CLIENTS = set()

class GameState:
    def __init__(self):
        self.players=[]
        self.hands = {}
        self.board = []
        self.turn_index = 0
        self.boneyard = []

    def __init__(self, players, hands, board, turn_index, boneyard):
        self.players = players
        self.hands = hands
        self.board = board
        self.turn_index = turn_index
        self.boneyard = boneyard

def generate_domino_set():
    dominos = []
    for i in range(7):
        for j in range(i,7):
            dominos.append((i,j))
    random.shuffle(dominos)
    return dominos
    
async def handler(websocket):
    CLIENTS.add(websocket)
    async for message in websocket:
        print(len(CLIENTS))
        # Verify if there are too many clients
        
        if len(CLIENTS) > 4 :
            print("Trop de clients connectés, déconnexion...")
            await websocket.send("Trop de clients connectés, déconnexion...")
            CLIENTS.remove(websocket)
            await websocket.close()
        
        #Start the game if there are enough clients
        players = []
        hands = {}
        if len(CLIENTS) >= 2:
            clients = len(CLIENTS)
            #create party
            dominos = generate_domino_set()
            for i in range(clients):
                players.append(i)
                hands[i]=dominos[i*7:(i+1)*7]
            boneyard=[dominos[clients*7:]]
            game = GameState(players,hands,[],0,boneyard)

            # try:
            for i,client in enumerate(CLIENTS):
                print("Hello")
                await websocket.send("Coucou")
                await client.send(json.dumps({"player":game.players[i],"hands":game.hands[i],"board":game.board}))
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