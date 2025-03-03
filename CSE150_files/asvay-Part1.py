# TCPClient.py
from socket import *

serverName = 'localhost'
serverPort = 12000

# Initializing TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Sending REGISTER message
register_msg = "REGISTER client123"
clientSocket.send(register_msg.encode())

# Sending BRIDGE message
bridge_msg = "BRIDGE client456"
clientSocket.send(bridge_msg.encode())

print("Messages Sent!")
clientSocket.close()
