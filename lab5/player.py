import socket
import rockPaperScissorsConstants as const

sock: socket = None
myPoints: int = 0
opponentPoints: int = 0

def validateMoveInput(input):
    upperInput = input.upper()
    if (upperInput == const.PAPER or upperInput == const.ROCK or upperInput == const.SCISSORS):
        return True
    return False   

def aPlayerHasWon():
    global myPoints, opponentPoints
    if (myPoints == const.GAME_WINNING_POINT):
        print(f"You won {myPoints} against {opponentPoints}")
        return True
    
    if (opponentPoints == const.GAME_WINNING_POINT):
        print(f"You lost {opponentPoints} against {myPoints}")
        return True
    
    return False

def makeMove(sock):
    while True:
        move = input(f"({myPoints},{opponentPoints}) Your move: ").upper()
        if (validateMoveInput(move)):
            sock.sendall(bytearray(move, 'utf-8'))
            return move
        else:
            print("input was not valid...")

def receiveMove(sock, myMove):
    opponentMove = sock.recv(1024).decode("utf-8")
    print("Opponent Move: ", opponentMove)
    decideRoundWinner(myMove, opponentMove)
    
def decideRoundWinner(me, opponent):
    global myPoints, opponentPoints

    if (me == const.ROCK and opponent == const.SCISSORS):
        myPoints += 1
    if (me == const.ROCK and opponent == const.PAPER):
        opponentPoints += 1
    if (me == const.SCISSORS and opponent == const.PAPER):
        myPoints += 1
    if (me == const.SCISSORS and opponent == const.ROCK):
        opponentPoints += 1
    if (me == const.PAPER and opponent == const.ROCK):
        myPoints += 1    
    if (me == const.PAPER and opponent == const.SCISSORS):
        opponentPoints += 1


def pickClientOrServer():
    while True:
        decision = input("Enter 'C' to become a client or 'S' to become the server: ").upper()

        if (decision != const.CLIENT_TYPE and decision != const.SERVER_TYPE):
            print("Invalid input! Input needs to  be either 'C' or 'S'")
            continue

        if (decision == const.SERVER_TYPE):
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            sock.bind((const.SERVER_IP_ADDRESS, const.PORT))
            sock.listen(1)
            print('\nlistening...\n')
            (socketClient, addr) = sock.accept()
            print(f"connection from {addr}")
            while True:
                myMove = makeMove(socketClient)
                receiveMove(socketClient, myMove)
                if (aPlayerHasWon()) : break

            socketClient.close()
            return

        if (decision == const.CLIENT_TYPE):
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            sock.connect((const.SERVER_IP_ADDRESS, const.PORT))

            while True:
                myMove = makeMove(sock)
                receiveMove(sock, myMove)
                if (aPlayerHasWon()) : break
            
            sock.close()
            return
        
pickClientOrServer()
        
