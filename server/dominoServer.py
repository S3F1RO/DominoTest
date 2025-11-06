import asyncio
import websockets
import random
import json
import ast

CLIENTS=set() 
players = []
game = None

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
    print(a,b)
    print(board)
    return a == left or b == left or a == right or b == right

def play_domino(domino,board,side):
    a,b = domino
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
        else:
            raise ValueError("Coup invalide sur la gauche")
    elif side == "right":
        if a == right:
            board.append((a,b))
        if b == right:
            board.append((b,a))
        else: 
            raise ValueError("Coup invalide sur la droite")
    else:
        raise ValueError("Side inconnu")
    
    return board

class GameState:
        def __init__(self,players):
            self.players=[]
            self.hands={}
            self.board=[]
            self.turn_index = 0
            self.boneyard = []
            self.state = 0

            for player in players:
                dominos = generate_domino_set()
                self.hands[player] = [dominos.pop() for _ in range(7)]
            self.boneyard = dominos
    
players=[]
async def handler(websocket):
    global game,players
    print("Client connecté")
    try:
        async for message in websocket:

            # Boucle pour process msgs
            data = json.loads(message)
            print(data)

            if data['type'] == "join": 
                if websocket not in CLIENTS:                   
                    CLIENTS.add(websocket)
                    players.append(websocket)
                    print(f"Joueur ajouté ({len(players)} total)")
                
                if len(players) >= 2 and game is None:
                    game = GameState(players)
                    print("La partie commence")

                    for player in players: 
                        await player.send(json.dumps({
                            "type":"init",
                            "hands":game.hands[player],
                            "board":game.board,
                            "your_turn": (player == players[game.turn_index])
                        }))
                elif len(players) < 2:      
                    await websocket.send(json.dumps({
                            "type":"infoS",
                            "dataS":"En attente d'un autre joueur"
                        }))
                elif game is not None:
                    await websocket.send(json.dumps({
                    "type": "infoS",
                    "dataS": "Partie déjà en cours"
                }))

            elif data['type'] == "play":
                player = websocket
                domino = ast.literal_eval(data['domino'])

                if (can_play(domino,game.board)):
                    print(f"bro played {domino}")
                    
                    #Apply move
                    try:
                        game.board=play_domino(domino,game.board,data['side'])
                    except ValueError as e:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": str(e)
                        }))
                        continue

                    #check if the user has the domino
                    try:
                        game.hands[player].remove(domino)
                    except ValueError as e:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": "Tu n'as pas ce domino"
                        }))
                        continue
                    
                    #Check winner
                    if not game.hands[player]:
                        for p in CLIENTS.copy():
                            try:
                                await p.send(json.dumps({
                                    "type":"game_over",
                                    "winner": players['player']
                                }))
                            except websockets.ConnectionClosed:
                                CLIENTS.remove(p)
                        continue
                    else:
                        #Broadcasting to everyone next turn
                        for p in CLIENTS.copy():
                            try:
                                await p.send(json.dumps({
                                    "type": "update",
                                    "board": game.board,
                                    "your_turn": (p == players[game.turn_index])
                                }))
                            except websockets.ConnectionClosed:
                                CLIENTS.remove(p)
                else:
                    await websocket.send(json.dumps({
                        "type": "invalid_move",
                        "message": "Coup invalide"
                    }))
            elif data['type'] == "pass":
                print("Toc..Toc...")

    except websockets.ConnectionClosed:
        print("Client déconnecté")
    finally:
        CLIENTS.remove(websocket)
    
async def main():
    async with websockets.serve(handler,'',8000):
        print("Serveur Websocket démarré sur ws://localhost:8000")
        await asyncio.Future()

if __name__=="__main__":
    asyncio.run(main())