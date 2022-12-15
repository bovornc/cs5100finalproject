COLUMN_HEIGHT = 6
ROW_LENGTH = 7


class Column:
    def __init__(self):
        self.list = []

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i]

    def push(self, element):
        if len(self.list) >= COLUMN_HEIGHT:
            return 1
        if element != "X" and element != "O":
            return 1
        else:
            self.list.append(element)
            return 0

    def peek(self):
        return self.list[-1]

    def aslist(self):
        column = []
        for i in range(len(self.list)):
            column.append(self.list[i])
        return column


class Board:
    def __init__(self):
        self.board = []
        for i in range(ROW_LENGTH):
            self.board.append(Column())
        self.XLocations = []
        self.OLocations = []

    def __copy__(self):
        boardCopy = Board()
        currentBoard = self.getBoard()
        for i in range(ROW_LENGTH):
            for j in range(len(currentBoard[i])):
                boardCopy.getBoard()[i].push(currentBoard[i][j])
        return boardCopy

    def getBoard(self):
        return self.board

    def printBoard(self):
        columns = []
        for column in self.board:
            columns.append(column.aslist())
        strings = []
        currentRow = 0
        while currentRow < COLUMN_HEIGHT:
            string = "[ "
            for column in columns:
                if len(column) <= currentRow:
                    string += "_ "
                else:
                    string += column[currentRow] + " "
            string += "]"
            strings.insert(0, string)
            currentRow += 1
        for string in strings:
            print(string)
        axis = "  "
        for i in range(len(self.board)):
            axis += str(i) + " "
        print(axis)
        print("")

    def checkWinner(self):
        winner = None

        # Check vertical winner
        for i in range(ROW_LENGTH):
            for j in range(3, COLUMN_HEIGHT):
                if len(self.board[i]) >= 4 and j < len(self.board[i]):
                    if self.board[i][j] == self.board[i][j-1] \
                            == self.board[i][j-2] == self.board[i][j-3]:
                        winner = self.board[i][j]
                        return winner

        # Check horizontal winner
        for j in range(COLUMN_HEIGHT):
            for i in range(3, ROW_LENGTH):
                if len(self.board[i]) > j and len(self.board[i-1]) > j \
                        and len(self.board[i-2]) > j and len(self.board[i-3]) > j:
                    if self.board[i][j] == self.board[i-1][j] \
                            == self.board[i-2][j] == self.board[i-3][j]:
                        winner = self.board[i][j]
                        return winner

        # Check diagonal winner
        for i in range(ROW_LENGTH - 3):
            for j in range(COLUMN_HEIGHT - 3):
                # Check bottom left to top right diagonal
                if len(self.board[i]) >= j+1 and len(self.board[i+1]) >= j+2 \
                        and len(self.board[i+2]) >= j+3 and len(self.board[i+3]) >= j+4:
                    if self.board[i][j] == self.board[i+1][j+1] \
                            == self.board[i+2][j+2] == self.board[i+3][j+3]:
                        winner = self.board[i][j]
                        return winner
                # Check top left to bottom right diagonal
                if len(self.board[i]) >= j+4 and len(self.board[i+1]) >= j+3 \
                        and len(self.board[i+2]) >= j+2 and len(self.board[i+3]) >= j+1:
                    if self.board[i+3][j] == self.board[i+2][j+1] \
                            == self.board[i+1][j+2] == self.board[i][j+3]:
                        winner = self.board[i+3][j]
                        return winner

        return winner

    def playMove(self, player, column: int):
        column = int(column)
        if player != "X" and player != "O":
            return 1
        if 0 > column > ROW_LENGTH:
            return 1
        self.board[column].push(player)
        if player == "X":
            self.XLocations.append((column, len(self.board[column])))
        else:
            self.OLocations.append((column, len(self.board[column])))
        return 0

    def whoseTurn(self):
        if len(self.XLocations) > len(self.OLocations):
            return "O"
        return "X"

    # Standard version, returns a list of all columns that aren't full
    def getPossibleActions(self):
        actions = []
        for i in range(ROW_LENGTH):
            if len(self.board[i]) < COLUMN_HEIGHT:
                actions.append(i)
        return actions

    # Experimental version, mimicking "partially observable game" by limiting the playable
    # actions to only within 1 spot of existing pieces
    # def getPossibleActions(self):
    #     actions = set()
    #     for i in range(ROW_LENGTH):
    #         if len(self.board[i]) > 0:
    #             if len(self.board[i]) < COLUMN_HEIGHT:
    #                 actions.add(i)
    #             if i-1 >= 0 and len(self.board[i-1]) < COLUMN_HEIGHT:
    #                 actions.add(i-1)
    #             if i+1 < ROW_LENGTH and len(self.board[i+1]) < COLUMN_HEIGHT:
    #                 actions.add(i+1)
    #     return list(actions)

    def getSuccessor(self, action: int):
        boardCopy = self.__copy__()
        player = self.whoseTurn()
        boardCopy.playMove(player, action)
        return boardCopy

    def get2InARow(self, player):
        twoInARowCount = 0

        # Check vertical
        for i in range(ROW_LENGTH):
            height = len(self.board[i])
            if height >= 2:
                # Count vertical 2 in a row
                if self.board[i][height-1] == self.board[i][height-2] == player:
                    # Count potential future vertical 4
                    if height+2 < COLUMN_HEIGHT:
                        twoInARowCount += 1

        # Check horizontal
        for j in range(COLUMN_HEIGHT):
            for i in range(1, ROW_LENGTH):
                if len(self.board[i]) > j and len(self.board[i-1]) > j:
                    # Count horizontal 2 in a row
                    if self.board[i][j] == self.board[i-1][j] == player:
                        # Count potential future horizontal 4
                        if i-3 >= 0 and len(self.board[i-3]) \
                                < len(self.board[i-2]) < len(self.board[i-1]):
                            twoInARowCount += 1
                        elif i-2 >= 0 and len(self.board[i-2]) < len(self.board[i-1])\
                                and i+1 < ROW_LENGTH and len(self.board[i+1]) < len(self.board[i]):
                            twoInARowCount += 1
                        elif i+2 < ROW_LENGTH and len(self.board[i+2])\
                                < len(self.board[i+1]) < len(self.board[i]):
                            twoInARowCount += 1

        # Check diagonals
        for i in range(ROW_LENGTH - 1):
            for j in range(COLUMN_HEIGHT - 1):
                # Check bottom left to top right diagonal for 2 in a row
                if len(self.board[i]) >= j+1 and len(self.board[i+1]) >= j+2:
                    if self.board[i][j] == self.board[i+1][j+1] == player:
                        # Count potential future 4s
                        if i-2 >= 0 and len(self.board[i-2]) < len(self.board[i]) + 2\
                                and len(self.board[i-2]) < len(self.board[i]) + 1:
                            twoInARowCount += 1
                        elif i-1 >= 0 and len(self.board[i-1]) < len(self.board[i]) + 1 \
                                and i+2 < ROW_LENGTH and len(self.board[i+2]) < len(self.board[i]):
                            twoInARowCount += 1
                        elif i+3 < ROW_LENGTH and len(self.board[i+3]) < len(self.board[i]) + 2\
                                and len(self.board[i+2]) < len(self.board[i]) + 1:
                            twoInARowCount += 1

                # Check top left to bottom right diagonal for 2 in a row
                if len(self.board[i]) >= j+2 and len(self.board[i+1]) >= j+1:
                    if self.board[i][j+1] == self.board[i+1][j] == player:
                        # Count potential future 4s
                        if i-2 >= 0 and len(self.board[i-2]) < len(self.board[i-1]) + 2 \
                                and len(self.board[i-2]) < len(self.board[i]) + 1:
                            twoInARowCount += 1
                        elif i-1 >= 0 and len(self.board[i-1]) <= len(self.board[i]) \
                                and i+2 < ROW_LENGTH and len(self.board[i+2]) < len(self.board[i+1]):
                            twoInARowCount += 1
                        elif i+3 < ROW_LENGTH and len(self.board[i + 3]) < len(self.board[i + 2]) \
                                < len(self.board[i + 1]):
                            twoInARowCount += 1

        return twoInARowCount

    def get3InARow(self, player):
        threeInARowCount = 0

        # Check vertical
        for i in range(ROW_LENGTH):
            height = len(self.board[i])
            if height >= 3:
                # Count vertical 2 in a row
                if self.board[i][height-1] == self.board[i][height-2] == self.board[i][height-3] == player:
                    # Count potential future vertical 4
                    if height+3 < COLUMN_HEIGHT:
                        threeInARowCount += 1

        # Check horizontal
        for j in range(COLUMN_HEIGHT):
            for i in range(2, ROW_LENGTH):
                if len(self.board[i]) > j and len(self.board[i-1]) > j and len(self.board[i-2]) > j:
                    # Count vertical 3 in a row
                    if self.board[i][j] == self.board[i-1][j] == self.board[i-2][j] == player:
                        # Count potential horizontal 4
                        if i-3 >= 0 and len(self.board[i-3]) < len(self.board[i-2]):
                            threeInARowCount += 1
                        elif i+1 < ROW_LENGTH and len(self.board[i+1]) < len(self.board[i]):
                            threeInARowCount += 1

        # Check diagonals
        for i in range(ROW_LENGTH - 2):
            for j in range(COLUMN_HEIGHT - 2):
                # Check bottom left to top right diagonal
                if len(self.board[i]) >= j+1 and len(self.board[i+1]) >= j+2 \
                        and len(self.board[i+2]) >= j+3:
                    if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == player:
                        # Count potential diagonal 4
                        if i-1 >= 0 and len(self.board[i-1]) < len(self.board[i]):
                            threeInARowCount += 1
                        elif i+3 < ROW_LENGTH and len(self.board[i+3]) <= len(self.board[i+2]):
                            threeInARowCount += 1
                # Check top left to bottom right diagonal
                if len(self.board[i]) >= j+3 and len(self.board[i+1]) >= j+2 \
                        and len(self.board[i+2]) >= j+1:
                    if self.board[i][j+2] == self.board[i+1][j+1] == self.board[i+2][j] == player:
                        # Count potential diagonal 4
                        if i-1 >= 0 and len(self.board[i-1]) <= len(self.board[i]):
                            threeInARowCount += 1
                        elif i+3 < ROW_LENGTH and len(self.board[i+3]) < len(self.board[i+2]):
                            threeInARowCount += 1

        return threeInARowCount