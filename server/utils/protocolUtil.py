import json

def protocol(COMMAND, FROM, MSG=None, TO=None, CHANNEL=None):
    if COMMAND == "PRIVMSG":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "MESSAGE":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "CHANNEL": CHANNEL})
    elif COMMAND == "LEAVE" or COMMAND == "JOIN":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "CHANNEL": CHANNEL})
    elif COMMAND == "MOTD":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "NICK":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG,"CHANNEL": CHANNEL})
    elif COMMAND == "ME":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "CHANNEL": CHANNEL})
    elif COMMAND == "CHANNELS":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "WHOIS":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "AWAY":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "QUIT":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "NOLONGERIGNORING":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "IGNORING":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})
    elif COMMAND == "HELP":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "MSG": MSG, "TO": TO})

    elif COMMAND == "NOTICE_NOLONGERAWAY":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "NOTICE_PONG":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "NOTICE_JOIN":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "CHANNEL": CHANNEL})
    elif COMMAND == "NOTICE_LEAVE":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "CHANNEL": CHANNEL})
    
    elif COMMAND == "ERR_NONICKNAMEGIVEN":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_NICKANAMETOOSHORT":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_NICKNAMEINUSE":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_NICKANAMETOOLONG":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_NEEDMOREPARAMS":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_CHANNELNAMETOOSHORT":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_CHANNELNAMETOOLONG":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_ALREADYINCHANNEL":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_CHANNELDOESNOTEXIST":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})
    elif COMMAND == "ERR_NOSUCHNICKNAME":
        return json.dumps({"COMMAND": COMMAND, "FROM": FROM, "TO": TO})