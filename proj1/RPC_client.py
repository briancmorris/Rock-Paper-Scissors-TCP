# @Author: Brian Morris
# CSC 401 Project 1
from __future__ import print_function
import socket
import sys


# Automated socket for programming.
IP = socket.gethostbyname(socket.gethostname())
# Server IP, first command line argument.
# serverIP = sys.argv[1]
# Server port, second command line argument.
serverPort = int(sys.argv[2])
# Create TCP socket.
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server.
clientSocket.connect((IP, serverPort))
while True:
    response = clientSocket.recv(1024)

    # Don't print empty responses.
    if len(response) > 1:
        print(response, end='')

    # Connected to server.
    if response.lower().__contains__("connected"):
        continue
    # Server asks us to wait.
    elif response.lower().__contains__("wait"):
        continue
    # Server asks for input.
    elif response.lower().__contains__("enter"):
        option = raw_input()
        clientSocket.send(option)
    # Server is busy.
    elif response.lower().__contains__("busy"):
        break
    # Game end.
    elif (
            response.lower().__contains__("lost") or
            response.lower().__contains__("won") or
            response.lower().__contains__("tie")):
        break
    # Error
    else:
        continue

clientSocket.close()
