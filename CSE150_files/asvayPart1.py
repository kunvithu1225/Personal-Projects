# TCPClient.py
from socket import *
import sys


serverName = 'localhost' # ???
serverPort = 12000  # ???

clientID = "client123"
clientIP = "127.0.0.1"  # localhost
clientPort = 1225  # unprivileged port (1024-49151)

# Initializing TCP socket
try: 
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
except Exception as e: 
    print(f"Error: Unable to connect to server - {e}")
    clientSocket.close()  # Ensure socket closes on failure
    sys.exit(1)

# Function to send REGISTER message
def send_register():
    register_msg = f"REGISTER\r\nclientID: {clientID}\r\nIP: {clientIP}\r\nPort: {clientPort}\r\n\r\n"
    clientSocket.send(register_msg.encode())
    response = clientSocket.recv(1024).decode()
    if response:
        print(f"Server Response: {response}")
    else:
        print("Error: No response from server.")

# Function to send BRIDGE message
def send_bridge():
    bridge_msg = f"BRIDGE\r\nclientID: {clientID}\r\n\r\n"
    clientSocket.send(bridge_msg.encode())
    response = clientSocket.recv(1024).decode()
    if response:
        print(f"Server Response: {response}")
    else:
        print("Error: No response from server.")

# Main loop for user input
try:
    while True:
        cmd = input("Enter command (/id, /register, /bridge, /quit): ").strip().lower()

        if cmd == "/id":
            print(f"Client ID: {clientID}")
        elif cmd == "/register":
            send_register()
        elif cmd == "/bridge":
            send_bridge()
        elif cmd == "/quit":
            print("Closing connection.")
            break
        else:
            print("Invalid command. Use /id, /register, /bridge, or /quit.")
finally:
    clientSocket.close()
