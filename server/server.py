import socket
import threading
from controller.configController import get_config
from controller.errorController import log_error
from controller.clientController import handle_client

def run_server():
    config = get_config()
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((config['ip'], config['port']))
        server.listen()
        print(f"Server started on {config['ip']}:{config['port']}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except Exception as e:
        log_error(e)
    finally:
        server.close()

run_server()