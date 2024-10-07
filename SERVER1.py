
import socket
import threading
from datetime import datetime

# List to keep track of all connected clients
clients = []

# Password for client authentication
PASSWORD = "mypassword"

# Function to handle each client connection
def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_socket.send("PASSWORD: ".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')

    if password == PASSWORD:
        client_socket.send("AUTH_SUCCESS".encode('utf-8'))
        connected = True
        clients.append(client_socket)

        while connected:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"[{addr}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
                    broadcast(message, client_socket)
                else:
                    connected = False
            except:
                connected = False

        client_socket.close()
        clients.remove(client_socket)
        print(f"[DISCONNECTED] {addr} disconnected.")
    else:
        client_socket.send("AUTH_FAILED".encode('utf-8'))
        client_socket.close()
        print(f"[FAILED AUTH] {addr} disconnected.")

# Function to broadcast a message to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.155.226', 5555))  # Your provided local IP address
    server.listen()
    print("[SERVER STARTED] Waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    start_server()
