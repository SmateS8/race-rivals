
# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

DB_PATH = "users.txt"
COINS_PATH = "coins.txt"
INVALID_CHARS = ["/n",":"]

USR_LEN = 7
PWD_LEN = 12


def load_coins(path):
    with open(path) as f:
        stored_coins = f.readlines()
        for i in enumerate(stored_coins):
            stored_coins[i[0]] = i[1][:-1]
    return stored_coins

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
                return True, 201
            else:
                return {"register":False, "message":"special chars"}
        else:
            return {"register":False, "message":"username exists"}

class Coins(Resource):
    def get(self,username):
        coins = load_coins(COINS_PATH)
        balance = get_balance(coins, username)
        return {"balance":balance}
        



api.add_resource(Login,'/login')
api.add_resource(Register,'/register')

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
