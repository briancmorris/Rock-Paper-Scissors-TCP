# @Author: Brian Morris
# CSC 401 Project 1
from socket import *
import sys

# Server IP, first command line argument.
serverIP = sys.argv[1]
# Server port, second command line argument.
servercPort = int(sys.argv[2])
# Create TCP socket.
clientSocket = socket(AF_INET, SOCK_STREAM)
# Up to two connections can be queued.
clientSocket.connect((serverIP, servercPort))

sentence = 'test'
clientSocket.send(sentence)

response = clientSocket.recv(1024)
print 'From TCP Server: ', response
clientSocket.close()
