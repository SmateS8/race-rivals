
# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import os
import random 

app = Flask(__name__)
api = Api(app)

DB_PATH = "users.txt"
COINS_PATH = "coins.txt"
PLAYERS_FOLDER = "players_data"
UPGRADES_PATH = "CAR_UPGRADES.json"
INVALID_CHARS = ["/n",":"]

lobbies = []#ex. lobby[0] = player1 name, player2 name ,player1 time, player2 time ,waiting for player(True, False), id
USR_LEN = 7
PWD_LEN = 12

def create_new_car_data(FILENAME,CAR_UPG_PATH, engine_lvl, gearbox_lvl):
    with open(CAR_UPG_PATH, 'r') as f:
        upgrades = json.load(f)
    with open(FILENAME, 'w') as f:
        data = {

            "max_vel": upgrades['engine_upgrades'][engine_lvl]['top_speed'],
            "offroad_vel": 1.5,
            "acceleration":  upgrades['gearbox_upgrades'][gearbox_lvl]['acceleration'],
            "deceleration": 0.05,
            "rotation_speed": 2,
            "engine_level": engine_lvl,
            "gearbox_level": gearbox_lvl,
            "engine_label": upgrades['engine_upgrades'][engine_lvl]['name'],
            "gearbox_label": upgrades['gearbox_upgrades'][gearbox_lvl]['name']
        }
        json.dump(data, f)


def load_coins(path):
    with open(path) as f:
        stored_coins = f.readlines()
        for i in enumerate(stored_coins):
            stored_coins[i[0]] = i[1][:-1]
    return stored_coins

def create_balance(path, username, balance):
        with open(path,'a') as f:
            f.write(f"{username}:{balance}\n")


def set_balance(path, username, balance):
    stored_coins = load_coins(path)
    for index, line in enumerate(stored_coins):
        user, coins = line.split(":")
        if user == username:
            stored_coins[index] = f"{username}:{balance}"
            break
    for i in range(len(stored_coins)):
        stored_coins[i] = stored_coins[i] + '\n'
    print(stored_coins)
    with open(path,'w') as f:
        f.writelines(stored_coins)
    

def get_balance(users,username):
    for user in users:
        name, coins = user.split(":")
        if name == username:
            break
    return coins

def load_credentials(path):
    with open(path) as f:
        stored_credentials = f.readlines()
        for i in enumerate(stored_credentials):
            stored_credentials[i[0]] = i[1][:-1]
    return stored_credentials

def check_credentials(path,username, password):
    creds = load_credentials(path)
    if f"{username}:{password}" in creds:
        return True
    return False

def check_username(path,username):
    creds = load_credentials(path)
    usernames = []
    for i in creds:
        usernames.append(i.split(":")[0])
    if username in usernames:
        return True
    return False

def valid_credentials(username,password):
    for char in INVALID_CHARS:
        if char in username or char in password:
            return False
    return True

def add_credentials(path, username,password):
    with open(path,'a') as f:
        f.write(f"{username}:{password}\n")





class Login(Resource):
    def get(self):
        username = request.json['username'] 
        password = request.json['password']

        return check_credentials(DB_PATH,username,password)
       
class Register(Resource):
    def post(self):
        username = request.json['username'] 
        password = request.json['password']

        if not check_username(DB_PATH,username):
            if valid_credentials(username,password):
                add_credentials(DB_PATH,username,password)
                create_balance(COINS_PATH,username,0)
                create_new_car_data(os.path.join(PLAYERS_FOLDER,username + '.json'),UPGRADES_PATH,0,0)
                return True, 201
            else:
                return {"register":False, "message":"special chars"}
        else:
            return {"register":False, "message":"username exists"}

class GetCoins(Resource):
    def get(self,username):
        coins = load_coins(COINS_PATH)
        balance = get_balance(coins, username)
        if check_username(DB_PATH,username):
            return {"balance":balance}
        return {"balance":False, "message":"user unknown"}
class SetCoins(Resource):    
    def post(self,username,amount):
        if not check_username(DB_PATH,username):
            return {"balance":False, "message":"user unknown"}
        if amount < 0:
            amount = 0
        set_balance(COINS_PATH,username,amount)
        stored_coins = load_coins(COINS_PATH)
        balance = get_balance(stored_coins,username)
        return {"balance": balance}
    
class Car(Resource):
    def get(self,username):
        if not check_username(DB_PATH,username):
            return False
        with open(os.path.join(PLAYERS_FOLDER,username+'.json'),'r') as f:
            data = json.load(f)
            return data

    def post(self,username):
        if not check_username(DB_PATH,username):
            return False
        with open(os.path.join(PLAYERS_FOLDER,username+'.json'),'w') as f:
            
            data = request.json
            print(data)
            json.dump(data,f)

class MultiplayerLobby(Resource):
    def get(self,username):
        this_lobby = ""
        for lobby in lobbies:
            if lobby['waiting_for_players'] == True:
                lobby = lobby
                lobby['player2'] = username
                lobby['waiting_for_players'] = False
                return {'lobby': lobby}
        if not this_lobby:
            #create a new one
            this_lobby = {
                'player1' : username,
                'player2' : "",
                'player1_time' : 0,
                'player2_time' : 0,
                'waiting_for_players' : True,
                'id':0 #Will be changed
            }
            original = False
            while not original:
                original = True
                id = random.randint(1,1000)
                for i in lobbies:
                    if i['id'] == id:
                        original = False
            this_lobby['id'] = id
            lobbies.append(this_lobby)
            return {'lobby' : this_lobby}
        

class CheckMPLobby(Resource):
    def get(self, lobby_id):
        for i in lobbies:
            if i['id'] == lobby_id:
                lobby_to_return = i
                return {'lobby': lobby_to_return}
        return False

class PostTimeToLobby(Resource):
    def get(self, lobby_id, username, timebz, timeaz):
        for index, lobby in enumerate(lobbies):
            if lobby['id'] == lobby_id:
                if username == lobby['player1']:
                    lobbies[index]['player1_time'] = float(f'{timebz}.{timeaz}')
                else:
                    lobbies[index]['player2_time'] = float(f'{timebz}.{timeaz}')
                print(lobbies[index])
                return True







api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(GetCoins,'/balance/<string:username>')
api.add_resource(SetCoins,'/balance/set/<string:username>/<int:amount>')
api.add_resource(Car,'/car/<string:username>')
api.add_resource(MultiplayerLobby,'/lobby/create/<string:username>')
api.add_resource(CheckMPLobby, '/lobby/check/<int:lobby_id>')
api.add_resource(PostTimeToLobby, '/lobby/time/<int:lobby_id>/<string:username>/<int:timebz>/<int:timeaz>')
# @app.route('/login', methods=['GET'])
# def login():
#     username = request.json["username"]
#     passwords = request.json["password"]

#     creds = load_credentials

#     if f"{username}:{passwords}":
#         return "CORRECT"
#     return "Wrong"


if __name__ == "__main__":
    app.run(debug = True)
