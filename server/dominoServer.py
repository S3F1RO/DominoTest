#!/usr/bin/python3
import asyncio
import websockets
import random
import json
import ast
CLIENTS = set()
nb_clients = 0

class GameState:
    def __init__(self):
        self.players=[]
        self.hands = {}
        self.board = []
        self.turn_index = 0
        self.boneyard = []
        self.state  = 0

    def __init__(self, players, hands, board, turn_index, boneyard):
        self.players = players
        self.hands = hands
        self.board = board
        self.turn_index = turn_index
        self.boneyard = boneyard
        self.state = 0

def computingTurns(domino, board, side, turn_index):
    if domino == "":
        turn_index += 1
        CLIENTS[turn_index].send(json.dumps({
            "type": "update",
            "board": board,
            "current_player" : players[turn_index],
            "hands" : hands[players[turn_index]]
        }))
        pass
    else:
        board = play_domino(domino, board, side)
        if domino in hands[players[turn_index]]:
            hands[players[turn_index]].remove(domino)
            if hands[players[turn_index]] == []:
                print(f"Le joueur {players[turn_index]} a gagné!")
                websockets.send({
                    "type": "win",
                    "player": players[turn_index]
                })
            else:
                turn_index += 1
                CLIENTS[turn_index].send(json.dumps({
                    "type": "update",
                    "board": board,
                    "current_player" : players[turn_index],
                    "hands" : hands[players[turn_index]]
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
    if can_play(domino,board) == False:
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
    global nb_clients
    global game
    game = GameState([],{},[],0,[])
    async for message in websocket:

        decodedMessage = json.loads(message)
        print(decodedMessage["type"])
        
        # Process people joining
        if decodedMessage['type'] == "join":
            nb_clients+=1
            if nb_clients < 2:
                await websocket.send(json.dumps({
                    'type':'infoS',
                    'dataS': 'En attente d\'un autre joueur...'
                }))
            elif nb_clients > 4 : # J'hésite entre la taille ou si le jeu à déjà commencé
                await websocket.send(json.dumps({
                    'type':'infoS',
                    'dataS': 'Partie pleine, vous ne pouvez pas rejoindre'
                }))
                nb_clients-=1
                #continue
            
            # Example: notify all connected clients
            for client in CLIENTS:
                await client.send(json.dumps({
                        'type': 'infoS',
                        'dataS': f"{nb_clients} joueurs connectés"
                    }))
            print(nb_clients)

            #Start the game if there are enough clients
            players = []
            hands = {}
            if nb_clients >= 2:
                #create party
                dominos = generate_domino_set()
                for i in range(nb_clients+1):
                    players.append(i)
                    hands[i]=dominos[i*7:(i+1)*7]
                boneyard=[dominos[nb_clients*7:]]
                # Initialize game state
                game.players = players
                game.hands = hands
                game.boneyard = boneyard
                game.state = 1
                # Notify all clients that the game has started
                for i,client in enumerate(CLIENTS):
                    await client.send(json.dumps({
                        "type" : "init",
                        "player":game.players[i],
                        "hands":[game.hands[i]],
                        "board":game.board
                        }))
            # Processing game
        elif decodedMessage['type'] == "play":
            if game.state != 1:
                await websocket.send(json.dumps({
                    'type':'infoS',
                    'dataS': 'La partie n\'a pas encore commencé.'
                }))
            else:
                print(decodedMessage['domino'])
                domino = ast.literal_eval(decodedMessage['domino']) # turn str into
                side   = decodedMessage["side"]
                player_id = decodedMessage['player']
                if (player_id == game.turn_index):
                    game.turn_index+=1
                    if (can_play(domino,game.board)):
                        game.board = play_domino(domino,game.board,side)
                        if domino in hands[game.turn_index]:
                            hands[game.turn_index].remove(domino)
                            if hands[game.turn_index] == "":
                                print ("Joueur ", game.turn_index," à gagné")
                                await websocket.send({
                                    'type':'gameover',
                                    'winner' : game.turn_index,
                                })
                            else:
                                await websocket.send({
                                    'type' : 'update',
                                    'board' : game.board
                                    'current_player': turn_index
                                })
                    

        elif decodedMessage['type'] == "pass":
                if game.state != 1:
                    await websocket.send(json.dumps({
                        'type':'infoS',
                        'dataS': 'La partie n\'a pas encore commencé.'
                    }))
                else:
                    game.turn_index+=1
                    await websocket.send({
                        'type' : 'update',
                        'board' : game.board
                        'current_player': turn_index
                    })

async def main():
    async with websockets.serve(handler,"",8000): # Qui peut se connecter à moi
        print("Serveur Websocket démarré sur ws://localhost:8000")
        await asyncio.Future()

    
if __name__=="__main__":
    asyncio.run(main())