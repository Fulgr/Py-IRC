from utils.logUtil import log_error
from utils.configUtil import get_config
from utils.commandUtil import check_command
import utils.channelUtil as channelUtil
from utils.protocolUtil import protocol
import random
import json

config = get_config()
clients = []

class Client:
    def __init__(self, client_socket, addr, nick):
        self.client_socket = client_socket
        self.addr = addr
        self.nick = nick
        self.buffer_size = config['buffer_size']
        self.channel = channelUtil.get_channel(config['default_channel'])
        self.away = ""
        self.ignore = []

    def send(self, data):
        try:
            self.client_socket.send(data.encode('utf-8'))
        except Exception as e:
            log_error(e)

    def is_ignored(self, addr):
        return addr in self.ignore
    
    def recv(self, length):
        try:
            return self.client_socket.recv(length).decode('utf-8')
        except Exception as e:
            log_error(e)

    def dm(self, client, nick, msg):
        for c in clients:
            if c.nick == nick:
                if not c.is_ignored(client.addr):
                    msg = protocol("PRIVMSG", client.nick, msg, TO=nick)
                    c.send(json.dumps(msg))

    def leave(self):
        self.client_socket.close()
        clients.remove(self)
        self.channel.leave(self)

    def say(self, msg):
        msg = protocol("MESSAGE", self.nick, msg, CHANNEL=self.channel.name)
        self.channel.broadcast(self, msg)

def handle_client(client_socket, addr):
    try:
        client = Client(client_socket, addr, nick=f"Guest{random.randint(1000, 9999)}")
        clients.append(client)
        client.channel.join(client)
        while True:
            try:
                msg = client.recv(client.buffer_size)
                if not msg:
                    client.leave()
                    break
                if not msg.strip() == "":
                    cmd = check_command(msg, client, clients)
                    if not cmd:
                        client.say(msg)
                    elif cmd != True:
                        client.say(cmd)
            except Exception as e:
                log_error(e)
                client.leave()
                break
    except Exception as e:
        log_error(e)
    finally:
        if client in clients:
            client.leave()