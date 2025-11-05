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

    def computingTurns(self, domino, board, side, turn_index):
        self.board = play_domino(domino, board, side)
        if domino in self.hands[self.players[turn_index]]:
            self.hands[self.players[turn_index]].remove(domino)
            if self.hands[self.players[turn_index]] == []:
                print(f"Le joueur {self.players[turn_index]} a gagné!")
                await websockets.send({
                    "type"
                })
            else:
                self.turn_index += 1
                await websockets.send(json.dumps({
                    "type": "update",
                    "board": self.board,
                    "current_player" : self.players[self.turn_index]
                }))
def generate_domino_set():
    dominos = []
    for i in range(7):
        for j in range(i,7):
            dominos.append((i,j))
    random.shuffle(dominos)
    return dominos

def can_play(domino,board):
    if not board:
        return True
        left = board[0][0]
        right = board[-1][1]
        a,b = domino
        return a == left or b == left or a == right or b == right

def play_domino(domino,board,side):
    a,b = domino
    if can_play(domino,board)==False:
        raise ValueError("Coup invalide")
    else: 
        if not board:
            board.append((a,b))
            return board
        left = board[0][0]
        right = board[-1][1]
        if side == "left":
            if b == left:
                board.insert(0,(a,b))
            elif a == left:
                board.insert(0,(b,a))
            else :
                raise ValueError("Coup invalide sur la gauche")
        elif side == "right":
            if a == right:
                board.append((a,b))
            elif b == right:
                board.append((b,a))
            else :
                raise ValueError("Coup invalide sur la droite")
        else :
            raise ValueError("Side inconnu")

        return board
    
async def handler(websocket):
    CLIENTS.add(websocket)
    async for message in websocket:
        # Verify if there are too many clients
        if len(CLIENTS) < 2:
            await websocket.send("En attente d'un autre client...")

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
                await client.send(json.dumps({
                    "player":game.players[i],
                    "hands":[game.hands[i]],
                    "board":game.board
                    }))

        # except websockets.ConnectionClosed:
        #     print("Client déconnecté")
        # finally:
        #     CLIENTS.remove(websocket)

async def main():
    async with websockets.serve(handler,"",8000): # Qui peut se connecter à moi
        print("Serveur Websocket démarré sur ws://localhost:8000")
        await asyncio.Future()

    
if __name__=="__main__":
    asyncio.run(main())