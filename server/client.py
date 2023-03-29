#client.py
#Demo client

import socket

HOST = 'localhost'  
PORT = 8000  

AUTH_TYPE = 'LOGIN' #LOGIN SIGNUP

USER_NAME = "MATYs"
PASSWORD = "HESLO123"

INVALID_CHARS = [':']

for char in INVALID_CHARS:
    if char not in USER_NAME or char not in PASSWORD:
        print("Credentials are character valid!")


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = "LOGIN"
            s.sendall(message.encode())
            data = s.recv(1024)
            if data.decode('utf-8') != "OK":
                print(f"Server does not support {message}")
                break
            message = USER_NAME+':'+PASSWORD
            s.sendall(message.encode())
            data = s.recv(1024).decode()
            print(data)
            if data == "CORRECT":
                print("Logged in succesfully!")
            else:
                print("Wrong credentials!")