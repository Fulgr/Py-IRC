from datetime import datetime
import json
from utils.configUtil import get_config
import utils.channelUtil as channelUtil
from utils.protocolUtil import protocol

config = get_config()

def check_command(cmd, client, clients):
    if cmd.startswith('/'):
        print(f"{client.addr}: {cmd}")
        if cmd.startswith('/motd'):
            motd(client)
        elif cmd.startswith('/nick'):
            nick(client, cmd, clients)
        elif cmd.startswith('/join'):
            join(client, cmd)
        elif cmd.startswith('/me'):
            me(client, cmd)
        elif cmd.startswith('/list'):
            channels(client, clients, cmd)
        elif cmd.startswith('/msg') or cmd.startswith('/query'):
            dm(client, cmd)
        elif cmd.startswith('/who') or cmd.startswith('/whois'):
            whois(client, cmd, clients)
        elif cmd.startswith('/leave'):
            leave(client, cmd)
        elif cmd.startswith('/away'):
            away(client, cmd)
        elif cmd.startswith('/quit'):
            quit(client)
        elif cmd.startswith('/ignore'):
            ignore(client, cmd, clients)
        elif cmd.startswith('/help'):
            help(client)
        elif cmd.startswith('/ping'):
            ping(client)
        elif cmd.startswith('/version'):
            client.send("Version: " + get_config()['version'])
        else:
            client.send("Invalid command")
        return True
    else:
        return False
    
def motd(client):
    msg = protocol("MOTD", "SERVER", f"Welcome to our {config['version']} network!\nPlease type /help for a list of commands within this network\nEnjoy your stay", TO=client.nick)
    client.send(msg)

def nick(client, cmd, clients):
    splitmsg = cmd.split(' ')
    if len(splitmsg) < 2:
        msg = protocol("ERR_NONICKNAMEGIVEN", "SERVER", TO=client.nick)
        client.send(msg)
        return
    nick = cmd.split(' ')[1]
    if len(nick) < 3:
        msg = protocol("ERR_NICKANAMETOOSHORT", "SERVER", TO=client.nick)
        client.send(msg)
        return
    if len(nick) > 9:
        msg = protocol("ERR_NICKANAMETOOLONG", "SERVER", TO=client.nick)
        client.send(msg)
        return
    if nick in [c.nick for c in clients]:
        msg = protocol("ERR_NICKNAMEINUSE", "SERVER", TO=client.nick)
        client.send(msg)
        return
    old_nick = client.nick
    client.nick = nick
    msg = protocol("NICK", old_nick, f"NICK {old_nick} {client.nick}", CHANNEL=client.channel.name)
    client.channel.broadcast(client, msg)

def join(client, cmd):
    splitmsg = cmd.split(' ')
    if len(splitmsg) < 2:
        msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
        client.send(msg)
        return
    channel = splitmsg[1]
    if len(channel) < 3:
        msg = protocol("ERR_CHANNELNAMETOOSHORT", "SERVER", TO=client.nick)
        client.send(msg)
        return
    if len(channel) > 9:
        msg = protocol("ERR_CHANNELNAMETOOLONG", "SERVER", TO=client.nick)
        client.send(msg)
        return
    if client.channel.name == channel:
        msg = protocol("ERR_ALREADYINCHANNEL", "SERVER", TO=client.nick)
        client.send(msg)
        return
    c = client.channel
    c.leave(client)
    r = channelUtil.get_channel(channel)
    if not r:
        msg = protocol("ERR_CHANNELDOESNOTEXIST", "SERVER", TO=client.nick)
        client.send(msg)
        client.channel = c
    else:
        client.channel = r
    client.channel.join(client)

def me(client, cmd):
    splitmsg = cmd.split(' ')
    if len(splitmsg) < 2:
        msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
        client.send(msg)
        return
    msg = " ".join(splitmsg[1:])
    msg = protocol("ME", client.nick, msg, CHANNEL=client.channel.name)
    client.channel.broadcast(client, msg)

def channels(client, clients, cmd):
    chans = [c.name for c in channelUtil.get_channels()]
    chans_json = json.dumps(chans)
    msg = protocol("CHANNELS", "SERVER", chans_json, TO=client.nick)
    client.send(msg)

def dm(client, cmd):
    parts = cmd.split(' ')
    if len(parts) < 3:
        msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
        client.send(msg)
        return
    nick = parts[1]
    msg = " ".join(parts[2:])
    msg = protocol("PRIVMSG", client.nick, msg, TO=nick)
    client.dm(msg)
    client.send(msg)

def whois(client, cmd, clients):
    splitmsg = cmd.split(' ')
    if len(splitmsg) < 2:
        msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
        client.send(msg)
        return
    nick = splitmsg[1]
    for c in clients:
        if c.nick == nick:
            msg = f"{c.nick} is in #{c.channel.name}"
            if c.away and c.away != "":
                msg += f"\n{c.nick} is away: {c.away}"
            msg = protocol("WHOIS", "SERVER", msg, TO=client.nick)
            client.send(msg)
            return
    msg = protocol("ERR_NOSUCHNICKNAME", "SERVER", TO=client.nick)
    client.send(msg)

def away(client, cmd):
    if cmd == "/away":
        client.away = ""
        msg = protocol("NOTICE_NOLONGERAWAY", "SERVER", TO=client.nick)
        client.send(msg)
    else:
        if len(cmd) < 6:
            msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
            client.send(msg)
            return
        client.away = cmd[6:]
        msg = protocol("AWAY", "SERVER", client.away, TO=client.nick)
        client.send(msg)

def leave(client, cmd):
    client.channel.leave(client)
    client.channel = channelUtil.get_channel(get_config()['default_channel'])
    client.channel.join(client)

def quit(client):
    msg = "Thank you for using our Py-IRC network, We hope to see you again soon!"
    msg = protocol("QUIT", "SERVER", msg, TO=client.nick)
    client.send(msg)
    client.leave()

def ignore(client, cmd, clients):
    splitmsg = cmd.split(' ')
    if len(splitmsg) < 2:
        msg = protocol("ERR_NEEDMOREPARAMS", "SERVER", TO=client.nick)
        client.send(msg)
        return
    nick = splitmsg[1]
    for c in clients:
        if c.nick == nick:
            if c.addr not in client.ignore:
                client.ignore.append(c.addr)
                msg = f"You are now ignoring {c.nick}"
                msg = protocol("IGNORING", "SERVER", msg, TO=client.nick)
                client.send(msg)
                return
            else:
                client.ignore.remove(c.addr)
                msg = f"You are no longer ignoring {c.nick}"
                msg = protocol("NOLONGERIGNORING", "SERVER", msg, TO=client.nick)
                client.send(msg)
                return
    msg = protocol("ERR_NOSUCHNICKNAME", "SERVER", TO=client.nick)
    client.send(msg)

def help(client):
    msg = ( "/motd - Display the message of the day\n"
            "/nick <nick> - Change your nick\n"
            "/join <channel> - Join a channel\n"
            "/me <action> - Perform an action\n"
            "/list - List all channels\n"
            "/msg <nick> <message> - Send a private message\n"
            "/whois <nick> - Get information about a user\n"
            "/away <message> - Set an away message\n"
            "/ignore <nick> - Ignore a user\n"
            "/ping - Ping the server\n"
            "/leave - Leave the current channel\n"
            "/quit - Quit the server\n"
            "/version - Display the server's Velocity IRC version\n"
            "/help - Display this help message")
    msg = protocol("HELP", "SERVER", msg, TO=client.nick)
    client.send(msg)

def ping(client):
    msg = protocol("NOTICE_PONG", "SERVER", TO=client.nick)
    client.send(msg)