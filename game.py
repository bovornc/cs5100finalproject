from agents import RandomAgent
from minimax import MinimaxAgent
from alphabeta import AlphabetaAgent
from expectimax import ExpectimaxAgent
from connect4 import Board


def selectAI(player):
    choice = input("What AI do you want to use for [" + player + "]? (Q to quit)]\n"
          "R: Random\n"
          "M: Minimax\n"
          "A: Alphabeta\n"
          "E: Expectimax\n"
          "I: Manual input\n")
    while choice.lower() != "q":
        if choice.lower() == "r" or choice.lower() == "random":
            return RandomAgent()
        elif choice.lower() == "m" or choice.lower() == "minimax":
            return MinimaxAgent()
        elif choice.lower() == "a" or choice.lower() == "alphabeta":
            return AlphabetaAgent()
        elif choice.lower() == "e" or choice.lower() == "expectimax":
            return ExpectimaxAgent()
        elif choice.lower() == "i" or choice.lower() == "manual":
            return "manual"
        else:
            continue

    return None


def playGame():
    board = Board()
    board.printBoard()
    player = "X"
    playerAgent = selectAI(player)
    if playerAgent is None:
        print("Goodbye!")
        return
    opponentAgent = selectAI("O")
    if opponentAgent is None:
        print("Goodbye!")
        return
    winner = None
    gameOver = False
    while gameOver is False:
        if player == "X":
            if playerAgent == "manual":
                playerMove = input("Which column do you want to drop a piece in [X]? ")
            else:
                playerMove = playerAgent.getAction(board, player)
            if playerMove is None:
                gameOver = True
                break
            print("X plays a piece at column " + str(playerMove))
            board.playMove(player, playerMove)
            board.printBoard()
            if board.checkWinner() is not None:
                winner = player
                gameOver = True
            else:
                player = "O"
        else:
            if opponentAgent == "manual":
                opponentMove = input("Which column do you want to drop a piece in [O]? ")
            else:
                opponentMove = opponentAgent.getAction(board, player)
            if opponentMove is None:
                gameOver = True
                break
            print("O plays a piece at column " + str(opponentMove))
            board.playMove(player, opponentMove)
            board.printBoard()
            if board.checkWinner() is not None:
                winner = player
                gameOver = True
            else:
                player = "X"
    if winner == "X" or winner == "O":
        print(winner + " wins!")
    else:
        print("It's a tie!")
    print("X was utilising " + str(playerAgent))
    print("O was utilising " + str(opponentAgent))
    # print("X has " + str(board.get2InARow("X")) + " 2-in-a-rows")
    # print("X has " + str(board.get3InARow("X")) + " 3-in-a-rows")
    # print("O has " + str(board.get2InARow("O")) + " 2-in-a-rows")
    # print("O has " + str(board.get3InARow("O")) + " 3-in-a-rows")


if __name__ == '__main__':
    playGame()