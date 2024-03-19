import socket
import threading
import sys
import os
import random
import time
import colors

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
            if "<<" in msg or ">>" in msg:
                print(colors.prYellow(msg))
            else:
                print(msg)
    except Exception as e:
        print(colors.prRed(f"Error: {e}"))


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
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
