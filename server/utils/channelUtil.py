from utils.logUtil import log_error
from utils.configUtil import get_config
from utils.protocolUtil import protocol
import json

config = get_config()
channels = []

def save_channel(channel):
    with open('data/channels.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[channel.name] = {"name": channel.name}
    with open('data/channels.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = []
        channels.append(self)

    def broadcast(self, client, msg):
        if len(self.clients) <= 0:
            return
        for c in self.clients:
            try:
                if c.channel == client.channel:
                    if not c.is_ignored(client.addr):
                        c.send(msg)
            except Exception as e:
                log_error(e)
                c.leave()

    def leave(self, client):
        self.clients.remove(client)
        msg = protocol("NOTICE_LEAVE", client.nick, CHANNEL=self.name)
        self.broadcast(client, msg)

    def join(self, client):
        self.clients.append(client)
        msg = protocol("NOTICE_JOIN", client.nick, CHANNEL=self.name)
        self.broadcast(client, msg)

def get_channels():
    return channels

def get_channel(name):
    for channel in channels:
        if channel.name == name:
            return channel
    if config['allow_channel_creation']:
        c = Channel(name)
        save_channel(c)
        return c
    else:
        return False