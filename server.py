import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen(5)

data = {
    "users": [],
    "last_user_id": 1000,
    "last_chat_id": 1000
}

def save_data():
    with open("data.json", "w") as file:
        json.dump(data, file)

def load_data():
    global data
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        save_data()

def generate_user_id():
    data["last_user_id"] += 1
    return data["last_user_id"]

def generate_chat_id():
    data["last_chat_id"] += 1
    return data["last_chat_id"]

def handle_client_connection(client_socket):
    user_id = generate_user_id()
    client_socket.send(f"Your User ID: {user_id}\n".encode())
    print(f"Assigned User ID: {user_id}")
    
    while True:
        try:
            chat_name = client_socket.recv(1024).decode().strip()
            if not chat_name:
                break
            last_chat_id = generate_chat_id()
            client_socket.send(f"Last Chat ID for '{chat_name}': {last_chat_id}\n".encode())
        except ConnectionResetError:
            break

    client_socket.close()

load_data()

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    handle_client_connection(client_socket)

save_data()
