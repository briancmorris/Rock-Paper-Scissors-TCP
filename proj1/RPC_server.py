# @Author: Brian Morris
# CSC 401 Project 1
from socket import *
import sys

# Server port, first command line argument.
serverPort = int(sys.argv[1])
# Create TCP socket.
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# Up to two connections can be queued.
serverSocket.listen(2)

print("Server is ready to serve!")

while True:
    connectionSocket, address = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    # Error check string.

    # Result of game.
    resultString = 'test'
    connectionSocket.send(resultString)
    connectionSocket.close()
