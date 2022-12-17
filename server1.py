import os
import socket
import threading
import time

host = '127.0.0.1'
port = 5070
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

addresses = {}
clients = []
nicknames = {}
games = {}


def broadcast_player_1(message, adr):
    addresses[adr].send(f'{nicknames[adr][0]}: {message.split("_")[1]}'.encode())
    if message != 'game_over':
        if len(games[adr]) > 4:
            addresses[games[adr][4]].send(f'{nicknames[adr][0]}: {message.split("_")[1]}'.encode())


def broadcast_player_2(message, adr):
    if message.startswith("click"):
        for key in games:
            if games[key][4] == adr:
                addresses[key].send(message.encode())
    else:
        addresses[adr].send(f'{nicknames[adr][0]}: {message.split("_")[1]}'.encode())
        if message != 'game_over':
            for key in games:
                if games[key][4] == adr:
                    addresses[key].send(f'{nicknames[adr][0]}: {message.split("_")[1]}'.encode())


def servers_view(client, adr):
    client.send(str(games).encode())
    create_game(client, adr)


def create_game(client, adr):
    while True:
        try:
            gm = client.recv(1024).decode().split('_')
            if gm[0] == 'create':
                word = gm[1]
                description = gm[2]
                games[adr] = [word, description, adr, nicknames[adr][0]]
                client.send(adr.encode())
                handle(client, 1, adr)
            elif gm[0] == 'connect':
                games[gm[1]].append(adr)
                games[gm[1]].append(nicknames[adr][0])
                handle(client, 2, adr)
            else:
                client.send(str(games).encode())
        except:
            if adr in addresses:
                del addresses[adr]
            client.close()
            if adr in nicknames:
                del nicknames[adr]
            print(addresses)
            print(nicknames)
            break


def handle(client, role, adr):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message.startswith("stop"):
                if role == 1:
                    broadcast_player_1(message, adr)
                elif role == 2:
                    broadcast_player_2(message, adr)
            else:
                message = message.split('_')
                if message[1] in games:
                    del games[message[1]]
                break
        except:
            if adr in addresses:
                del addresses[adr]
            client.close()
            if adr in nicknames:
                del nicknames[adr]
            print(addresses)
            print(nicknames)
            return
    servers_view(client, adr)


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        nickname = client.recv(1024).decode()

        nicknames[str(address[1])] = (nickname, str(address[1]))
        addresses[str(address[1])] = client

        print("Nickname is {}".format(nickname))
        print(client)
        print(nicknames)

        thread = threading.Thread(target=servers_view, args=(client, str(address[1])))
        thread.start()


os.system('cls')

receive()
