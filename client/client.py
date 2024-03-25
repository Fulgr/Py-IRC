import socket
import threading
import random
import time
import datetime
import tkinter as tk

username = "Guest" + str(random.randint(1, 9999))

server_ip = "127.0.0.1"
server_port = 8001

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Velocity Client")

        self.text_area = tk.Text(master)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(master)
        self.input_field.pack(fill=tk.X)

        self.input_field.bind("<Return>", self.send_message)

        self.connect_to_server()

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_message(f"/nick {username}")

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
                else:
                    self.text_area.insert(tk.END,'\n' +  msg)
                self.text_area.see(tk.END)
        except Exception as e:
            print(f"Error: {e}")

    def send_message(self, event=None):
        if not self.input_field.get() and event:
            self.client.send(event.encode("utf-8")[:1024])
        msg = self.input_field.get()
        if msg == "/clear":
            self.text_area.delete('1.0', tk.END)
        else:
            self.client.send(msg.encode("utf-8")[:1024])
        self.input_field.delete(0, tk.END)

def run_gui():
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()

run_gui()