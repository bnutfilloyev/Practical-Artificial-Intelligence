import numpy as np


class Taktikl:
    def __init__(self):
        self.player = 'x'
        self.opponent = 'o'
        self.depth_level = 5
        self.board = [
            ['x', 'o', 'x', 'o'],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['o', 'x', 'o', 'x']
        ]

    @staticmethod
    def on_board(tpl):
        row = tpl[0]
        col = tpl[1]
        if 0 <= row <= 3 and 0 <= col <= 3:
            return True
        return False

    def is_empty(self, tpl):
        row = tpl[0]
        col = tpl[1]
        if self.board[row][col] == ' ':
            return True
        return False

    def possible_moves(self, tpl, info):
        row = tpl[0]
        col = tpl[1]
        moves = []
        if self.board[row][col] == self.player or self.board[row][col] == self.opponent:
            candidate_moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for move in candidate_moves:
                if self.on_board(move) and self.is_empty(move) and (move not in info[(row, col)]):
                    moves.append(move)
        return moves

    @staticmethod
    def all_three_equal(arr):
        if arr[0] == arr[1] and arr[1] == arr[2]:
            return True
        return False

    def print_board(self):
        print("\n")
        for i in range(4):
            print(i, "|", self.board[i][0], "", self.board[i][1], "", self.board[i][2], "", self.board[i][3])
        print("  -------------")
        print("    0  1  2  3")

    def get_info(self):
        d = dict()

        for i in range(4):
            for j in range(4):
                if self.board[i][j] != ' ':
                    d[(i, j)] = []
        return d

    def evaluate(self):
        for row in range(4):
            if self.all_three_equal(self.board[row][0:3]) or self.all_three_equal(self.board[row][1:4]):
                if self.board[row][1] == self.player:
                    return 10
                elif self.board[row][1] == self.opponent:
                    return -10

        b_T = np.array(self.board).T
        for col in range(4):
            if self.all_three_equal(b_T[col][0:3]) or self.all_three_equal(b_T[col][1:4]):
                if b_T[col][1] == self.player:
                    return 10
                elif b_T[col][1] == self.opponent:
                    return -10

        for row in range(2):
            for col in range(2):
                if self.all_three_equal(
                        [self.board[row][col], self.board[row + 1][col + 1], self.board[row + 2][col + 2]]):
                    if self.board[row][col] == self.player:
                        return 10
                    elif self.board[row][col] == self.opponent:
                        return -10

        for row in range(2, 4):
            for col in range(2):
                if self.all_three_equal(
                        [self.board[row][col], self.board[row - 1][col + 1], self.board[row - 2][col + 2]]):
                    if self.board[row][col] == self.player:
                        return 10
                    elif self.board[row][col] == self.opponent:
                        return -10

        return 0

    def minimax(self, depth, is_max, info):
        score = self.evaluate()

        if score == 10 or score == -10:
            return score

        if is_max:
            best = -1000

            if depth >= self.depth_level:
                return best

            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == self.player:
                        possible_moves = self.possible_moves((i, j), info)

                        for move in possible_moves:
                            temp = info[(i, j)]
                            info.pop((i, j))
                            info[(move[0], move[1])] = temp + [(i, j)]

                            self.board[i][j] = ' '
                            self.board[move[0]][move[1]] = self.player

                            best = max(best, self.minimax(depth + 1, not is_max, info))

                            info.pop((move[0], move[1]))
                            info[(i, j)] = temp

                            self.board[move[0]][move[1]] = ' '
                            self.board[i][j] = self.player

            return best

        best = 1000

        if depth > self.depth_level:
            return best

        for i in range(4):
            for j in range(4):
                if self.board[i][j] == self.opponent:
                    possible_moves = self.possible_moves((i, j), info)

                    for move in possible_moves:
                        temp = info[(i, j)]
                        info.pop((i, j))
                        info[(move[0], move[1])] = temp + [(i, j)]

                        self.board[i][j] = ' '
                        self.board[move[0]][move[1]] = self.opponent

                        best = min(best, self.minimax(depth + 1, not is_max, info))

                        info.pop((move[0], move[1]))
                        info[(i, j)] = temp

                        self.board[move[0]][move[1]] = ' '
                        self.board[i][j] = self.opponent
        return best

    def find_best_move(self):
        best_val = -1000
        best_move = [(-1, -1), (-2, -2)]
        info = self.get_info()
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == self.opponent:
                    possible_moves = self.possible_moves((i, j), info)

                    for move in possible_moves:

                        temp = info[(i, j)]
                        info.pop((i, j))
                        info[(move[0], move[1])] = temp + [(i, j)]

                        self.board[i][j] = ' '
                        self.board[move[0]][move[1]] = self.opponent

                        move_val = self.minimax(0, True, info)

                        info.pop((move[0], move[1]))
                        info[(i, j)] = temp

                        self.board[move[0]][move[1]] = ' '
                        self.board[i][j] = self.opponent

                        if move_val > best_val:
                            best_move = [(i, j), (move[0], move[1])]
                            best_val = move_val

        return best_move

    def game(self):
        print("Let's start Taktikl game!")
        print("Here is the board:")
        self.print_board()
        print("You are X and the computer is O")

        while True:
            i = input("Which one you want to move? Format is following:\nROW,COLUMN -> ")

            if i == 'q':
                print("Bye!")
                break

            row1, col1 = map(int, i.split(','))

            i = input("Where you want to move it? Format is following:\nROW,COLUMN -> ")

            if i == 'q':
                print("Bye!")
                break

            row2, col2 = map(int, i.split(','))

            self.board[row1][col1] = ' '
            self.board[row2][col2] = 'x'

            self.print_board()

            print("Bot's turn:")
            print("Warning: it may take SOME TIME for algorithm to search for optimal move. Please don't close.")

            best_move = self.find_best_move()
            self.board[best_move[0][0]][best_move[0][1]] = ' '
            self.board[best_move[1][0]][best_move[1][1]] = 'o'

            self.print_board()
