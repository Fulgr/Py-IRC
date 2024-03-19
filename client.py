import socket
import threading
import sys
import os
import random
import time
import colors
import datetime

os.system("cls")

username = "Guest" + str(random.randint(1, 9999))
password = "pass"

def receive_messages(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8")
            if msg.startswith("/pong"):
                ping_time = datetime.datetime.now() - datetime.datetime.strptime(' '.join(msg.split(" ")[1:]), "%Y-%m-%d %H:%M:%S.%f")
                ping_ms = ping_time.total_seconds() * 1000
                print(colors.prGreen("Ping: " + str(round(ping_ms)) + " ms"))
            elif "<<" in msg or ">>" in msg:
                print(colors.prPurple(msg))
            elif "<" in msg and ">" in msg and msg.split("<")[1].split(">")[0]:
                print(msg)
            else:
                print(colors.prYellow(msg))
    except Exception as e:
        print(colors.prRed(f"Error: {e}"))


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "0.0.0.0"
    server_port = 8001
    client.connect((server_ip, server_port))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        client.send("/motd".encode("utf-8"))
        time.sleep(0.2)
        client.send(f"/msg NickServ {username} {password}".encode("utf-8"))
        while True:
            msg = input()
            sys.stdout.write("\033[F")
            if msg == "/clear":
                os.system("cls")
            else:
                client.send(msg.encode("utf-8")[:1024])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


run_client()
