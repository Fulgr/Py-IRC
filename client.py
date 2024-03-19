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

server_ip = "127.0.0.1"
server_port = 8001

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


def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            elif msg.startswith("/conn"):
                server_ip = msg.split(" ")[1].split(":")[0]
                server_port = int(msg.split(":")[1])
                return {"ip": server_ip, "port": server_port, "is_running": True}
            else:
                client.send(msg.encode("utf-8")[:1024])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


is_running = True
while is_running:
    os.system("cls")
    print(f"Connecting to {server_ip}:{server_port}")
    try:
        output = run_client(server_ip, server_port)
        is_running = output["is_running"]
        server_ip = output["ip"]
        server_port = output["port"]
    except Exception as e:
        print(colors.prRed(f"Error: {e}"))
        server_ip = input("Enter server IP: ")
        server_port = int(input("Enter server port: "))
        is_running = True