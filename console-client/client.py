import socket
import threading
import json
import time
import sys
import datetime

def yellow(text): print(f"\033[33m{text}\033[0m")
def red(text): print(f"\033[31m{text}\033[0m")
def green(text): print(f"\033[32m{text}\033[0m")
def purple(text): print(f"\033[35m{text}\033[0m")

class Client:
    def __init__(self, ip, port):
        self.active = True
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_ping = datetime.datetime.now()
        self.last_dm = ""
        self.nick = ""
    
    def connect(self):
        self.client.connect((self.ip, self.port))

        recv_thread= threading.Thread(target=self.recv)
        recv_thread.start()

        ping_thread = threading.Thread(target=self.ping)
        ping_thread.start()

    def check_command(self, msg):
        cmd = msg['COMMAND']
        if cmd == 'MESSAGE':
            print(f"<{msg['FROM']}> {msg['MSG']}")
        elif cmd == 'PRIVMSG':
            if msg['FROM'] == self.nick and msg['TO'] == self.nick:
                self.last_dm = self.nick
                purple(f"{self.nick} >> {msg['MSG']}")
            elif msg['FROM'] != self.nick and msg['TO'] == self.nick:
                purple(f"{msg['FROM']} >> {msg['MSG']}")
                self.last_dm = msg['FROM']
            elif msg['FROM'] == self.nick and msg['TO'] != self.nick:
                purple(f"{msg['TO']} << {msg['MSG']}")
                self.last_dm = msg['TO']
            else:
                purple(f"{msg['FROM']} >> {msg['TO']}: {msg['MSG']}")
        elif cmd == 'NICK':
            yellow(f"{msg['FROM']} changed nick to {msg['MSG']}")
            self.nick = msg['MSG']
        elif cmd == 'ME':
            print(f"* {msg['FROM']} {msg['MSG']}")
        elif cmd == 'WHOIS' or cmd == 'QUIT' or cmd == 'AWAY' or cmd == 'CHANNELS' or cmd == 'MOTD' or cmd == 'NOLONGERIGNORING' or cmd == 'IGNORING' or cmd == 'HELP':
            yellow(f"{msg['MSG']}")
            self.nick = msg['TO']
        elif cmd == 'NOTICE_NOLONGERAWAY':
            yellow(f"You are no longer away")
        elif cmd == 'NOTICE_PONG':
            now = datetime.datetime.now()
            diffinms = round((now - self.last_ping).total_seconds() * 1000)
            green(f"Pong: {diffinms}ms")
        elif cmd == 'NOTICE_JOIN':
            yellow(f"{msg['FROM']} joined {msg['CHANNEL']}")
            if self.nick == "":
                self.nick = msg['FROM']
        elif cmd == 'NOTICE_LEAVE':
            yellow(f"{msg['FROM']} left {msg['CHANNEL']}")
        elif cmd.startswith('ERR_'):
            red(f"{msg['COMMAND']}")

    def recv(self):
        try:
            while self.active:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    msg = data.decode("utf-8")
                    msg = json.loads(msg)
                    self.check_command(msg)
                except Exception as e:
                    print(f"2:{e}")
        except Exception as e:
            print(f"1:{e}")

    def ping(self):
        while self.active:
            self.client.send("/ping".encode("utf-8"))
            self.last_ping = datetime.datetime.now()
            time.sleep(60*3)

    def send(self, data):
        try:
            if data == '/ping':
                self.last_ping = datetime.datetime.now()
            elif data.startswith('/r'):
                data = data.replace('/r', f'/msg {self.last_dm}')
            elif data.strip() == '':
                return
            self.client.send(data.encode("utf-8"))
        except Exception as e:
            print(f"3:{e}")
isRunning = True
while isRunning:
    client = Client("127.0.0.1", 8001)
    client.connect()
    while client.active:
        msg = input()
        sys.stdout.write("\033[F")
        print("                                                                       ")
        sys.stdout.write("\033[F")
        client.send(msg)
        if msg == '/quit':
            client.active = False
            isRunning = False
            break