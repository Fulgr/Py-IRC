import socket
import threading
from utils.configUtil import get_config
from utils.logUtil import log_error, log
from utils.clientUtil import handle_client
import modules.logClearModule as log_clear_module
import modules.initializeChannelsModule as initialize_channels_module

def start_module(module):
    thread = threading.Thread(target=module.start)
    thread.start()

def run_modules():
    log("Running modules")
    start_module(log_clear_module)
    start_module(initialize_channels_module)

def run_server():
    config = get_config()
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log("Socket created")
        server.bind((config['ip'], config['port']))
        log(f"Socket bound to {config['ip']}:{config['port']}")
        server.listen()
        log(f"Server started listening on {config['ip']}:{config['port']}")
        run_modules()

        while True:
            client_socket, addr = server.accept()
            log(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
            log(f"Started new thread to handle client {addr[0]}:{addr[1]}")
    except Exception as e:
        log_error(e)
    finally:
        server.close()
        log("Server closed")

run_server()