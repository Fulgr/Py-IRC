import socket
import threading
import datetime
import tkinter as tk
import json
import time

server_ip = "127.0.0.1"
server_port = 8001

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Velocity Client")
        self.master.configure(bg="black")

        self.sidebar = tk.Frame(master, bg="black")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.text_area = tk.Text(master, bg="black", fg="yellow", font=("Arial", 12), cursor="arrow")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(master, bg="gray", fg="lightgreen", font=("Arial", 12), cursor="tcross")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipadx=5, ipady=5)

        self.send_button = tk.Button(master, text="Send", bg="black", fg="yellow", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(side=tk.LEFT, fill=tk.X, expand=False)

        self.button = tk.Button(self.sidebar, text="#general", bg="gray", fg="lightgreen", font=("Arial", 8), command=lambda: self.send_message("/join general"))
        self.button.pack(fill=tk.X)

        self.input_field.bind("<Return>", self.send_message)

        try:
            self.connect_to_server()
        except Exception as e:
            self.text_area.insert(tk.END, f"Error: {e}")
            self.text_area.insert(tk.END, f"\nPlease enter a IP using /conn <ip>:<port>\nFor avaible networks use /networks")

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.text_area.insert(tk.END, f"Connected to {server_ip}:{server_port}\nPlease use /lhelp for a list of client commands\n")
        self.send_message("/list json")


    def close_connection(self):
        self.client.close()

    def receive_messages(self):
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8")
                if msg.startswith("/pong"):
                    ping_time = datetime.datetime.now() - datetime.datetime.strptime(' '.join(msg.split(" ")[1:]), "%Y:%m:%d:%H:%M:%S:%f")
                    ping_ms = ping_time.total_seconds() * 1000
                    self.text_area.insert(tk.END, '\n'+"Ping: " + str(round(ping_ms)) + " ms")
                elif msg.startswith("/channels"):
                    split = msg.split(" ")
                    msgunified = ' '.join(split[1:])
                    chans = json.loads(msgunified)
                    for widget in self.sidebar.winfo_children():
                        widget.destroy()
                    for chan in chans:
                        button = tk.Button(self.sidebar, text=f"#{chan}", bg="gray", fg="lightgreen", font=("Arial", 8), command=lambda chan=chan: self.send_message(f"/join {chan}"))
                        button.pack(fill=tk.X)
                else:
                    self.text_area.insert(tk.END,'\n' +  msg)
                self.text_area.see(tk.END)
        except Exception as e:
            print(f"Error: {e}")

    def send_message(self, event=None):
        msg = self.input_field.get()
        if isinstance(event, str) and event.startswith("/"):
            if event == "/motd" or event.startswith("/join") or event.startswith("/list"):
                msg = event
        elif not msg:
            return
        self.input_field.delete(0, tk.END)
        if msg == "/clear":
            self.text_area.delete('1.0', tk.END)
        elif msg == "/chans":
            self.client.send("/list json".encode("utf-8"))
            return
        elif msg == "/lhelp":
            self.text_area.insert(tk.END, '\n' + "Client commands:")
            self.text_area.insert(tk.END, '\n' + "/clear - Clear chat")
            self.text_area.insert(tk.END, '\n' + "/chans - Updates the channel sidebar")
            self.text_area.insert(tk.END, '\n' + "/conn <ip>:<port> - Connect to a server")
            self.text_area.insert(tk.END, '\n' + "/networks - List available networks")
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
            self.text_area.insert(tk.END, '\n' + "Available networks:")
            self.text_area.insert(tk.END, '\n' + "127.0.0.1:8001 - Localhost")
            self.text_area.insert(tk.END, '\n' + "node2.endelon-hosting.de:34055 - Endolon test server")
        else:
            self.client.send(msg.encode("utf-8")[:1024])

def run_gui():
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()

run_gui()