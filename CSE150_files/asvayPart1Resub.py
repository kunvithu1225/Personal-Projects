from socket import *
import sys

serverName = 'localhost'  # ??
serverPort = 12000  # ??
clientID = "client123"
clientIP = "127.0.0.1"
clientPort = 1225  # Random unprivileged port (1024-49151)

# Initializing the TCP socket
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
except Exception as e:
    print(f"Error: Unable to connect to server - {e}")
    sys.exit(1)

def send_register():
    register_msg = f"REGISTER\r\nclientID: {clientID}\r\nIP: {clientIP}\r\nPort: {clientPort}\r\n\r\n"
    clientSocket.send(register_msg.encode())
    clientSocket.settimeout(2)  # Setting timeout to prevent infinite waiting
    try:
        response = clientSocket.recv(1024).decode()
        print(f"Server Response: {response}")
    except timeout:
        print("Error: No response from server.")

def send_bridge():
    bridge_msg = f"BRIDGE\r\nclientID: {clientID}\r\n\r\n"
    clientSocket.send(bridge_msg.encode())
    clientSocket.settimeout(2)  # Setting timeout to prevent infinite waiting
    try:
        response = clientSocket.recv(1024).decode()
        print(f"Server Response: {response}")
    except timeout:
        print("Error: No response from server.")

# Sending REGISTER/BRIDGE upon startup
send_register()
send_bridge()

clientSocket.close()
print("Client execution completed successfully.")
