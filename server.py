import socket
import threading
import json

with open("data/users.json", "r", encoding="utf-8") as file:
    users = json.load(file)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

connectedClients = []
currentUsers = {}

def run_server():
    server_ip = config['ip']
    port = config['port']
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

def handle_client(client_socket, addr):
    try:
        client_socket.send("Please use \"/msg NickServ nick password\" to login\"".encode("utf-8"))
        while True:
            try:
                request = client_socket.recv(1024).decode("utf-8")
                if request.startswith("/"):
                    print(f"Action from {addr[0]}:{addr[1]}: {request}")
                    if request.lower() == "/quit" or request == "":
                        break
                    elif request.startswith("/msg"):
                        print(f"Private message from {addr[0]}:{addr[1]}: {request}")
                        req = request.split(" ")
                        if req[1] == "NickServ":
                            if login_user(req[2], req[3], addr):
                                client_socket.send("Login successful".encode("utf-8"))
                                if client_socket not in connectedClients:
                                    connectedClients.append(client_socket)
                            else:
                                client_socket.send("Login failed".encode("utf-8"))
                        else:
                            send_dm(req[1], f"{currentUsers[addr]} >> {' '.join(req[2:])}")
                            send_dm(currentUsers[addr], f"{req[1]} << {' '.join(req[2:])}")
                    elif request.startswith("/me"):
                        broadcast(f"*{currentUsers[addr]} {' '.join(request.split(' ')[1:])}")
                    elif request.startswith("/motd"):
                        client_socket.send(config['motd'].encode("utf-8"))

                elif not currentUsers[addr]:
                    client_socket.send("Please use \"/msg NickServ nick password\" to register your nick".encode("utf-8"))

                else:
                    msg = f"<{currentUsers[addr]}> {request}"
                    print(msg)
                    broadcast(msg)
            except:
                client_socket.send("The server actively rejected your message".encode("utf-8"))

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        connectedClients.remove(client_socket)
        broadcast(f"{currentUsers[addr]} has left the chat")
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def broadcast(msg):
    for client in connectedClients:
        try:
            client.send(msg.encode("utf-8"))
        except Exception as e:
            print(f"Error when broadcasting to client: {e}")

def login_user(user, passw, addr):
    if user in users:
        if users[user] != passw or user in currentUsers.values():
            return False
        else:
            if addr in currentUsers:
                broadcast(f"{currentUsers[addr]} has changed their nick to {user}")
            else:
                broadcast(f"{user} has joined the chat")
            currentUsers[addr] = user
            return True
    users[user] = passw
    with open("data/users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)
    if addr in currentUsers:
        broadcast(f"{currentUsers[addr]} has changed their nick to {user}")
    else:
        broadcast(f"{user} has joined the chat")
    currentUsers[addr] = user
    return True

def send_dm(username, msg):
    addr = ""
    for user in currentUsers:
        if currentUsers[user] == username:
            addr = user
            break

    for client in connectedClients:
        if client.getpeername() == addr:
            client.send(msg.encode("utf-8"))
run_server()