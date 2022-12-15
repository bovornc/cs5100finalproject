from agents import MultiAgentSearchAgent
from connect4 import Board
from connect4 import ROW_LENGTH


class AlphabetaAgent(MultiAgentSearchAgent):
    def getAction(self, state: Board, player):
        if len(state.XLocations) == 0 and len(state.OLocations) == 0:
            return round(ROW_LENGTH / 2)
        return self.maxValue(state, player, 0, -9999999, 9999999)[1]

    def maxValue(self, state: Board, player, depth: int, alpha: int, beta: int):
        action = None
        if state.checkWinner() is not None or len(state.getPossibleActions()) == 0 or depth > self.depth+1:
            return self.getUtility(state, player), action
        u = -9999999
        for a in state.getPossibleActions():
            successor = state.getSuccessor(a)
            nextPlayer = successor.whoseTurn()
            nextDepth = depth + 1
            if nextPlayer == player:
                if self.maxValue(successor, nextPlayer, nextDepth, alpha, beta)[0] > u:
                    u = self.maxValue(successor, nextPlayer, nextDepth, alpha, beta)[0]
                    action = a
            else:
                if self.minValue(successor, nextPlayer, nextDepth, alpha, beta)[0] > u:
                    u = self.minValue(successor, nextPlayer, nextDepth, alpha, beta)[0]
                    action = a
            if u > beta:
                return u, action
            alpha = max(alpha, u)
        return u, action

    def minValue(self, state: Board, player, depth: int, alpha: int, beta: int):
        action = None
        if state.checkWinner() is not None or len(state.getPossibleActions()) == 0 or depth > self.depth+1:
            return self.getUtility(state, player), action
        u = 9999999
        for a in state.getPossibleActions():
            successor = state.getSuccessor(a)
            nextPlayer = successor.whoseTurn()
            nextDepth = depth + 1
            if nextPlayer == player:
                if self.maxValue(successor, nextPlayer, nextDepth, alpha, beta)[0] < u:
                    u = self.maxValue(successor, nextPlayer, nextDepth, alpha, beta)[0]
                    action = a
            else:
                if self.minValue(successor, nextPlayer, nextDepth, alpha, beta)[0] < u:
                    u = self.minValue(successor, nextPlayer, nextDepth, alpha, beta)[0]
                    action = a
            if u < alpha:
                return u, action
            beta = min(beta, u)
        return u, action