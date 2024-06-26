import socket
import threading
import datetime
import tkinter as tk
import json
import time
import os

initial_commands = ["/list", "/motd"]

appdatapath = os.getenv('APPDATA') + "\\VelocityClient"
if not os.path.exists(appdatapath):
    os.makedirs(appdatapath)
    with open(appdatapath + "\\config.json", "w") as f:
        f.write('{"theme": "dark"}')
os.chdir(appdatapath)

with open(f"{appdatapath}/config.json", "r", encoding="utf-8") as f:
    file = json.load(f)
    if "theme" not in file:
        file["theme"] = "dark"
    if "autonick" in file:
        initial_commands.append(f"/nick {file['autonick']}")


server_ip = "127.0.0.1"
server_port = 8001

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Velocity Client")

        color = "#191b1d"
        self.channel_bg = "#373737"
        self.channel_fg = "lightgreen"

        self.sidebar = tk.Frame(master, bg=color)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.text_area = tk.Text(master, bg=color, fg="white", font=("Arial", 12), cursor="arrow")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(master, bg=color, fg="white", font=("Arial", 12), cursor="tcross")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipadx=5, ipady=5)

        self.send_button = tk.Button(master, text="►", bg=color, fg="lightgreen", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(side=tk.LEFT, fill=tk.X, expand=False)

        self.button = tk.Button(self.sidebar, text="#general", bg=self.channel_bg, fg=self.channel_fg, font=("Arial", 8), command=lambda: self.send_message("/join general"))
        self.button.pack(fill=tk.X)

        self.current_channel = "general"

        self.input_field.bind("<Return>", self.send_message)

        try:
            self.connect_to_server()
            with open(f"{appdatapath}/config.json", "r", encoding="utf-8") as f:
                file = json.load(f)
            self.change_theme(file["theme"])
        except Exception as e:
            self.text_area.insert(tk.END, f"Error: {e}")
            self.text_area.insert(tk.END, f"Please enter a IP using /conn <ip>:<port>\nFor available networks use /networks")

    def change_theme(self, theme):
        if theme == "dark":
            self.master.configure(bg="#191b1d")
            self.text_area.configure(bg="#191b1d", fg="white")
            self.input_field.configure(bg="#191b1d", fg="white")
            self.send_button.configure(bg="#191b1d", fg="lightgreen")
            self.sidebar.configure(bg="#191b1d")
            for widget in self.sidebar.winfo_children():
                widget.configure(bg="#373737", fg="lightgreen")
            self.channel_bg = "#373737"
            self.channel_fg = "lightgreen"
        elif theme == "light":
            self.master.configure(bg="white")
            self.text_area.configure(bg="white", fg="black")
            self.input_field.configure(bg="white", fg="black")
            self.send_button.configure(bg="white", fg="black")
            self.sidebar.configure(bg="white")
            for widget in self.sidebar.winfo_children():
                widget.configure(bg="lightgrey", fg="black")
            self.channel_bg = "lightgrey"
            self.channel_fg = "black"
        elif theme == "hacker":
            self.master.configure(bg="#191b1d")
            self.text_area.configure(bg="#191b1d", fg="lightgreen")
            self.input_field.configure(bg="#191b1d", fg="lightgreen")
            self.send_button.configure(bg="#191b1d", fg="lightgreen")
            self.sidebar.configure(bg="#191b1d")
            for widget in self.sidebar.winfo_children():
                widget.configure(bg="#191b1d", fg="lightgreen")
            self.channel_bg = "#373737"
            self.channel_fg = "lightgreen"
        elif theme == "custom":
            self.master.configure(bg="black")
            self.text_area.configure(bg="black", fg="white")
            self.input_field.configure(bg="black", fg="white")
            self.send_button.configure(bg="black", fg="white")
            self.sidebar.configure(bg="black")
            for widget in self.sidebar.winfo_children():
                widget.configure(bg="black", fg="white")
            self.channel_bg = "black"
            self.channel_fg = "white"

    def send_initial_commands(self):
        for command in initial_commands:
            self.client.send(command.encode("utf-8")[:1024])
            time.sleep(0.5)

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        ping_thread = threading.Thread(target=self.ping)
        ping_thread.daemon = True
        ping_thread.start()

        self.text_area.insert(tk.END, f"Connected to {server_ip}:{server_port}\nPlease use /lhelp for a list of client commands\n")

    def close_connection(self):
        self.client.close()

    def ping(self):
        while True:
            self.client.send("/ping".encode("utf-8")[:1024])
            time.sleep(60*3)

    def receive_messages(self):
        try:
            initial_messages_thread = threading.Thread(target=self.send_initial_commands)
            initial_messages_thread.start()
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    msg = data.decode("utf-8")
                    msg = json.loads(msg)
                    if msg['COMMAND'] == 'MESSAGE':
                        self.text_area.insert(tk.END,'\n' +  f"<{msg['FROM']}> {msg['MSG']}")
                    elif msg['COMMAND'] == 'CHANNELS':
                        chans = json.loads(msg['MSG'])
                        for widget in self.sidebar.winfo_children():
                            widget.destroy()
                        for chan in chans:
                            button = tk.Button(self.sidebar, text=f"#{chan}", bg=self.channel_bg, fg=self.channel_fg, font=("Arial", 8), command=lambda chan=chan: self.send_message(f"/join {chan}"))
                            button.pack(fill=tk.X)
                    elif msg['COMMAND'] == 'NOTICE_JOIN':
                        self.text_area.insert(tk.END, '\n' + f"{msg['FROM']} joined {msg['CHANNEL']}")
                    elif msg['COMMAND'] == 'NOTICE_LEAVE':
                        self.text_area.insert(tk.END, '\n' + f"{msg['FROM']} left {msg['CHANNEL']}")
                    elif msg['COMMAND'] == 'MOTD' or msg['COMMAND'] == 'IGNORING' or msg['COMMAND'] == 'NOLONGERIGNORING':
                        self.text_area.insert(tk.END, '\n' + msg['MSG'])
                    elif msg['COMMAND'] == 'NICK':
                        self.text_area.insert(tk.END, '\n' + f"{msg['FROM']} changed their nickname to {msg['MSG']}")
                    elif msg['COMMAND'] == 'PRIVMSG':
                        self.text_area.insert(tk.END, '\n' + f"{msg['FROM']} >> {msg['TO']}: {msg['MSG']}")
                    elif msg['COMMAND'] == 'ERR_INVALIDCOMMAND':
                        self.text_area.insert(tk.END, '\n' + "Invalid command")
                    elif msg['COMMAND'] == 'HELP' or msg['COMMAND'] == 'WHOIS':
                        response = msg['MSG'].split('\n')
                        for line in response:
                            self.text_area.insert(tk.END, '\n' + line)
                    elif msg['COMMAND'] == 'ME':
                        self.text_area.insert(tk.END, '\n' + f"* {msg['FROM']} {msg['MSG']}")
                    elif msg['COMMAND'] == 'NOTICE_PONG':
                        pass
                    elif msg['COMMAND'] == 'AWAY':
                        self.text_area.insert(tk.END, '\n' + f"{msg['TO']} is away: {msg['MSG']}")
                    elif msg['COMMAND'] == 'ERR_NICKNAMEINUSE':
                        self.text_area.insert(tk.END, '\n' + "Nickname is already in use")
                    elif msg['COMMAND'] == 'ERR_ALREADYINCHANNEL':
                        self.text_area.insert(tk.END, '\n' + "You are already in that channel")
                    else:
                        self.text_area.insert(tk.END, '\n' + json.dumps(msg))
                    self.text_area.see(tk.END)
                except Exception as e:
                    insert(self, f"1:{e}")
        except Exception as e:
            insert(self, f"2:{e}")

    def send_message(self, event=None):
        msg = self.input_field.get()
        if isinstance(event, str) and event.startswith("/"):
            if event == "/motd" or event.startswith("/join") or event.startswith("/list"):
                msg = event
        elif not msg:
            return
        self.input_field.delete(0, tk.END)
        if msg.startswith("/join"):
            splitmsg = msg.split(' ')
            if len(splitmsg) < 2:
                self.text_area.insert(tk.END, '\n' + "Invalid channel")
                return
            self.current_channel = splitmsg[1]
        elif msg.startswith("/msg"):
            splitmsg = msg.split(' ')
            if len(splitmsg) < 3:
                self.text_area.insert(tk.END, '\n' + "Invalid message")
                return
            self.current_channel = splitmsg[1]
            with open(f"{appdatapath}/config.json", "r", encoding="utf-8") as f:
                file = json.load(f)
            file['recentcontact'] = splitmsg[1]
            with open(f"{appdatapath}/config.json", "w", encoding="utf-8") as f:
                json.dump(file, f)
        if msg == "/clear":
            self.text_area.delete('1.0', tk.END)
        elif msg == "/chans":
            self.client.send("/list".encode("utf-8")[:1024])
            return
        elif msg.startswith("/r"):
            splitmsg = msg.split(' ')
            if len(splitmsg) < 2:
                self.text_area.insert(tk.END, '\n' + "Invalid message")
                return
            with open(f"{appdatapath}/config.json", "r", encoding="utf-8") as f:
                file = json.load(f)
            if "recentcontact" not in file:
                self.text_area.insert(tk.END, '\n' + "No recent contact")
                return
            self.client.send(f"/msg {file['recentcontact']} {' '.join(splitmsg[1:])}".encode("utf-8")[:1024])
        elif msg == "/lhelp":
            self.text_area.insert(tk.END, '\n\n' + "Client commands:")
            self.text_area.insert(tk.END, '\n' + "/clear - Clear chat")
            self.text_area.insert(tk.END, '\n' + "/chans - Updates the channel sidebar")
            self.text_area.insert(tk.END, '\n' + "/conn <ip>:<port> - Connect to a server")
            self.text_area.insert(tk.END, '\n' + "/networks - List available networks")
            self.text_area.insert(tk.END, '\n' + "/themes - List available themes")
            self.text_area.insert(tk.END, '\n' + "/theme <theme> - Change theme")
            self.text_area.insert(tk.END, '\n' + "/autonick <nick> - Set a default nickname\n")
        elif msg.startswith("/conn"):
            try:
                self.text_area.delete('1.0', tk.END)
                self.close_connection()
                global server_ip, server_port
                server_ip = msg.split(" ")[1].split(":")[0]
                server_port = int(msg.split(" ")[1].split(":")[1])
                self.connect_to_server()
            except Exception as e:
                self.text_area.insert(tk.END, '\n' + f"Error: {e}")
                raise Exception("Invalid connection string")
        elif msg.startswith("/networks"):
            self.text_area.insert(tk.END, '\n\n' + "Available networks:")
            self.text_area.insert(tk.END, '\n' + "127.0.0.1:8001 - Localhost")
        elif msg.startswith("/themes"):
            self.text_area.insert(tk.END, '\n\n' + "Available themes:")
            self.text_area.insert(tk.END, '\n' + "dark - Dark theme")
            self.text_area.insert(tk.END, '\n' + "light - Light theme")
            self.text_area.insert(tk.END, '\n' + "hacker - Hacker theme")
            self.text_area.insert(tk.END, '\n' + "custom - Custom theme")
            self.text_area.insert(tk.END, '\n' + "To change theme use /theme <theme>\n")
        elif msg.startswith("/theme"):
            splitmsg = msg.split(' ')
            if len(splitmsg) < 2:
                self.text_area.insert(tk.END, '\n' + "Invalid theme")
                return
            with open(f"{appdatapath}\\config.json", "r", encoding="utf-8") as f:
                file = json.load(f)
            file["theme"] = splitmsg[1]
            with open(f"{appdatapath}\\config.json", "w", encoding="utf-8") as f:
                json.dump(file, f)
            self.text_area.insert(tk.END, '\n' + f"Theme set to {splitmsg[1]}")
            self.change_theme(splitmsg[1])
        elif msg.startswith("/autonick"):
            with open(f"{appdatapath}\\config.json", "r", encoding="utf-8") as f:
                file = json.load(f)
            if len(msg.split(" ")) < 2:
                del file["autonick"]
            else:
                file["autonick"] = ' '.join(msg.split(" ")[1:])
            with open(f"{appdatapath}\\config.json", "w", encoding="utf-8") as f:
                json.dump(file, f)
        else:
            self.client.send(msg.encode("utf-8")[:1024])

def run_gui():
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()

def insert(self, msg):
    self.text_area.insert(tk.END, '\n' + msg)

run_gui()