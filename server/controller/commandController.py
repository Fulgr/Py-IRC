
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
            channels(client, clients)
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
        else:
            client.send("Invalid command")
        return True
    else:
        return False
    
def motd(client):
    client.send("Welcome to the server!")

def nick(client, cmd, clients):
    nick = cmd.split(' ')[1]
    if len(nick) > 0 and len(nick) <= 16 and nick not in [c.nick for c in clients]:
        old_nick = client.nick
        client.nick = nick
        client.say(f"{old_nick} changed their nick to {client.nick}")
    else:
        client.send("Invalid nick")

def join(client, cmd):
    channel = cmd.split(' ')[1]
    if channel[0] == '#':
        channel = channel[1:]
    if len(channel) > 0 and len(channel) <= 16:
        client.say(f"{client.nick} has left #{client.channel}")
        client.channel = channel
        client.say(f"{client.nick} has joined #{client.channel}")
    else:
        client.send("Invalid channel name")

def me(client, cmd):
    client.say(f"* {client.nick} {cmd[4:]}")

def channels(client, clients):
    chans = [c.channel for c in clients]
    chans = list(dict.fromkeys(chans))
    msg = "Channels: "
    for c in chans:
        msg += f"#{c} "
    client.send(msg)

def dm(client, cmd):
    parts = cmd.split(' ')
    nick = parts[1]
    msg = ' '.join(parts[2:])
    client.dm(client, nick, msg)
    client.send(f"{nick} << {msg}")

def whois(client, cmd, clients):
    nick = cmd.split(' ')[1]
    for c in clients:
        if c.nick == nick:
            msg = f"{c.nick} is in #{c.channel}"
            if c.away and c.away != "":
                msg += f"\n{c.nick} is currently away: {c.away}"
            client.send(msg)
            return
    client.send(f"No such nick {nick}")

def away(client, cmd):
    if cmd == "/away":
        client.away = ""
        client.send("You are no longer away")
    else:
        client.away = cmd[6:]
        client.send(f"You are now away: {client.away}")

def leave(client, cmd):
    client.say(f"{client.nick} has left #{client.channel}")
    client.channel = "general"
    client.say(f"{client.nick} has joined #{client.channel}")

def quit(client):
    client.send("Thank you for using our Py-IRC network, We hope to see you again soon!")
    client.leave()

def ignore(client, cmd, clients):
    nick = cmd.split(' ')[1]
    for c in clients:
        if c.nick == nick:
            if c.addr not in client.ignore:
                client.ignore.append(c.addr)
                client.send(f"You are now ignoring {c.nick}")
                return
            else:
                client.ignore.remove(c.addr)
                client.send(f"You are no longer ignoring {c.nick}")
                return
    client.send(f"No such nick {nick}")

def help(client):
    client.send("/motd - Display the message of the day\n"
                "/nick <nick> - Change your nick\n"
                "/join <channel> - Join a channel\n"
                "/me <action> - Perform an action\n"
                "/list - List all channels\n"
                "/msg <nick> <message> - Send a private message\n"
                "/whois <nick> - Get information about a user\n"
                "/away <message> - Set an away message\n"
                "/leave - Leave the current channel\n"
                "/quit - Quit the server\n"
                "/help - Display this help message")
