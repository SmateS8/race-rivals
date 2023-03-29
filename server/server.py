#server.py

import socket
import threading
import os
import time

HOST = 'localhost'  # You can change this to your server's IP address
PORT = 8000  # You can change this to any available port number


stored_credentials = []
user_names = []
passwords = []

def load_data():
    with open("users.txt") as f:
        stored_credentials = f.readlines()
        for i in enumerate(stored_credentials):
            stored_credentials[i[0]] = i[1][:-1]
    user_names = []
    passwords = []
    for i in stored_credentials:
        user, password = i.split(":")
        user_names.append(user)
        passwords.append(password)
    



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}...")


    conn, addr = s.accept()
    with conn:
        load_data()
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if data.decode("UTF-8") == "LOGIN":

            conn.sendall("OK".encode())
            data = conn.recv(1024)
            data = data.decode()

            if data in stored_credentials:
                conn.sendall("CORRECT".encode())
            else:
                conn.sendall("WRONG".encode())

        if data.decode("UTF-8") == "SIGNUP":

            conn.sendall("OK".encode())
            data = conn.recv(1024)
            data = data.decode()

            user, password = data.split(":")
            if user in user_names:
                pass



        else:
            conn.sendall("UNSUPPORTED_AUTH".encode())

                

