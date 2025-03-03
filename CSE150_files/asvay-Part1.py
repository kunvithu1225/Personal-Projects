# TCPClient.py
from socket import *

serverName = 'localhost'
serverPort = 12000

# Initializing TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Send REGISTER message
register_msg = "REGISTER client123"
clientSocket.send(register_msg.encode())

# Send BRIDGE message
bridge_msg = "BRIDGE client456"
clientSocket.send(bridge_msg.encode())

print("Messages Sent!")
clientSocket.close()



# TCPServer.py
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')
      
while True:
    connectionSocket, addr = serverSocket.accept()

    while True:
        sentence = connectionSocket.recv(1024).decode()
        if not sentence: 
            break
        print(f"Received: {sentence}")
    
    connectionSocket.close()