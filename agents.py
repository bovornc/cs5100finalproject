import random

from connect4 import Board


class RandomAgent:
    def getAction(self, board):
        possibleActions = board.getPossibleActions()
        randomAction = random.choice(possibleActions)
        return randomAction


class MultiAgentSearchAgent:
    def __init__(self):
        self.depth = 2

    # Evaluation function
    def getUtility(self, state: Board, player):
        opponent = "O"
        if player == opponent:
            opponent = "X"
        getWinner = state.checkWinner()
        if getWinner == player:                     # return a big number if you win
            return 10000
        if getWinner == opponent:
            return -10000                           # return a small number if opponent can

        player2s = state.get2InARow(player)             # number of useful 2-in-a-rows
        player3s = state.get3InARow(player)             # number of useful 3-in-a-rows

        opponent2s = state.get2InARow(opponent)
        opponent3s = state.get3InARow(opponent)

        score = 0
        score += player2s * 5 + player3s * 15
        score -= (opponent2s * 5 + opponent3s * 15)

        return score