import socket
import threading
import sys
import os
import random
import time
import colors
import datetime

os.system("cls")

username = "NickServ"

server_ip = "127.0.0.1"
server_port = 8001

def receive_messages(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8")
            if "<<" in msg or ">>" in msg:
                print(colors.prPurple(msg))
                if ">>" in msg:
                    m = msg.split(" ")
                    msg = " ".join(m[2:])
                    user = m[0]
                    if msg.startswith("REGISTER"):
                        client.send(f"/msg {user} {username} is online".encode("utf-8"))
            elif ("<" in msg and ">" in msg and msg.split("<")[1].split(">")[0]) or (msg[0]=="*"):
                pass
            else:
                print(colors.prYellow(msg))
    except Exception as e:
        print(colors.prRed(f"Error: {e}"))


def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    client.send(f"/nick {username}".encode("utf-8"))
    time.sleep(1)
    client.send("NickServ is online".encode("utf-8"))

    while True:
        msg = input()
        sys.stdout.write("\033[F")
        client.send(msg.encode("utf-8"))

while True:
    os.system("cls")
    print(f"Connecting to {server_ip}:{server_port}")
    try:
        run_client(server_ip, server_port)
    except:
        time.sleep(1)