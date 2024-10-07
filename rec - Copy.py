import socket
import threading
from datetime import datetime

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[RECEIVED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
        except:
            print("[ERROR] Connection closed by the server.")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input("")
        if message:
            client_socket.send(message.encode('utf-8'))
            print(f"[YOU] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server using the local IP address
    client.connect(('192.168.155.226', 5555))  # Your provided local IP address

    # Receive initial prompt for password
    initial_message = client.recv(1024).decode('utf-8')
    print(initial_message)

    # Send password
    password = input("Enter the password: ")
    client.send(password.encode('utf-8'))

    # Check if authentication succeeded
    auth_status = client.recv(1024).decode('utf-8')
    if auth_status == "AUTH_SUCCESS":
        print("[AUTHENTICATED] You are now connected.")
        
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        # Allow the client to send messages in the main thread
        send_messages(client)
    else:
        print("[AUTH FAILED] Connection closed.")
        client.close()



