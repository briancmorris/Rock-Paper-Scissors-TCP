# @Author: Brian Morris
# CSC 401 Project 1
import socket
import sys
import thread

# Number of players connected to the server.
numPlayers = 0


def game(player1socket, player2socket):
    """
    Defines the behavior of a game of rock, paper, scissors.
    :param player1socket: The TCP socket of player 1.
    :param player2socket: The TCP socket of player 2.
    :return:
    """
    # Server message.
    print "\n>>New Game Thread spawned"

    # Utilize global variable numPlayers.
    global numPlayers

    # Prompt for valid input from both players.
    player1socket.send("Enter R, P, or S: ")
    player2socket.send("Enter R, P, or S: ")

    # Receive and print the response from player 1.
    response1 = player1socket.recv(1024)
    print ">>Player 1 played: " + response1

    # Receive and print the response from player 2.
    response2 = player2socket.recv(1024)
    print ">>Player 2 played: " + response2

    # Result string.
    result = "result of the game is "

    # Evaluate tie case.
    if response1.__eq__(response2):
        result = result + "tie\nYou tied!\nDisconnecting from the game server. Thank you for playing!\n"
        player1socket.send(result)
        player2socket.send(result)
        # Server message.
        print ">>Players tied!"
    # Evaluate if player 1 wins.
    elif (
            (response1.__contains__("R") and response2.__contains__("S")) or
            (response1.__contains__("S") and response2.__contains__("P")) or
            (response1.__contains__("P") and response2.__contains__("R"))
    ):
        result = result + "1"
        player1socket.send(result + "\nYou won!\nDisconnecting from the game server. Thank you for playing!")
        player2socket.send(result + "\nYou lost!\nDisconnecting from the game server. Thank you for playing!")
        # Server message.
        print ">>Player 1 won!"
    # Player 2 wins.
    else:
        result = result + "2"
        player1socket.send(result + "\nYou lost!\nDisconnecting from the game server. Thank you for playing!\n")
        player2socket.send(result + "\nYou won!\nDisconnecting from the game server. Thank you for playing!\n")
        # Server message.
        print ">>Player 2 won!"

    # Remove 2 players from the count.
    numPlayers -= 2
    # Server message.
    print ">>Game over."
    # Exit game.
    return


# Server port, first command line argument.
serverPort = int(sys.argv[1])
# Create TCP socket.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to port.
serverSocket.bind(('', serverPort))
# Up to three connections can be queued.
serverSocket.listen(3)
# Server initialized. Print status.
print("Server is ready to serve!")

# "Queue" of player sockets.
playerSockets = []

# Check for connecting players.
while True:
    # Accept new players.
    playerSocket, playerAddress = serverSocket.accept()
    # Add them to players queue.
    playerSockets.append(playerSocket)
    # Update numPlayers
    numPlayers += 1
    # Send welcome message.
    playerSocket.send("Connected to the Rock, Paper, Scissors Game Server.\n")

    # Indicate new player to server.
    print "\nA new player is trying to connect to the game server on " + str(playerAddress[0]) + ":" + str(playerAddress[1])

    # First player connected.
    if numPlayers == 1:
        # Server message.
        print "Current number of available players is 1\nOne player waiting for another player to join."

        # Player message.
        playerSocket.send("You are player 1.\nWaiting for a second player to join.\n\n")
    # Second player connected.
    elif numPlayers == 2:
        # Server message.
        print "Current number of available players is 2\nTwo players available, let's play!"

        # Player message.
        playerSocket.send("You are player 2.\nLet's play!\n\n")

        # Start up the game thread.
        thread.start_new_thread(game, (playerSockets.pop(0), playerSockets.pop(0),))

    # Full game.
    elif numPlayers > 2:
        print "Two players already playing. Can't start a new game.\n"
        # Kick out excess players.
        for socket in playerSockets:
            socket.send("Server is busy with a game. Try to connect later.\n")
            playerSockets.remove(socket)
            numPlayers -= 1
