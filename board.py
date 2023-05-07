from copy import deepcopy


class Board:
    def __init__(self):
        # board[row][col] in UI
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.possible_move = []
        self.direction = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

    def update_board(self, cur_state):
        self.board = deepcopy(cur_state)
        return self.board

    def current_board(self):
        return self.board

    def count(self):
        count_X = 0
        count_O = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == -1:
                    count_X += 1
                elif self.board[i][j] == 1:
                    count_O += 1
        return count_X, count_O

    def weighted_score(self, player_to_move):
        # Paper link: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
        my_tiles, opp_tiles, my_front_tiles, opp_front_tiles = 0, 0, 0, 0
        p, c, l, m, f, d = 0, 0, 0, 0, 0, 0
        # Piece difference, frontier disks and disk squares
        XY = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
        ]
        V = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20],
        ]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player_to_move:
                    d += V[i][j]
                    my_tiles += 1
                elif self.board[i][j] == -player_to_move:
                    opp_tiles += 1
                    d -= V[i][j]
            if self.board[i][j] != 0:
                for k in XY:
                    x = i + k[0]
                    y = j + k[1]
                    if x >= 0 and x < 8 and y >= 0 and y < 8 and self.board[x][y] == 0:
                        if self.board[i][j] == player_to_move:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break
        if my_tiles > opp_tiles:
            p = (100 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0
        if my_front_tiles > opp_front_tiles:
            f = -(100 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0
        # Corner occupancy
        my_tiles, opp_tiles = 0, 0
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for corner in corners:
            if self.board[corner[0]][corner[1]] == player_to_move:
                my_tiles += 1
            elif self.board[corner[0]][corner[1]] == -player_to_move:
                opp_tiles += 1
        c = 25 * (my_tiles - opp_tiles)
        my_tiles = opp_tiles = 0
        # Corner closeness
        corner_neighbors = [
            [(0, 1), (1, 1), (1, 0)],
            [(0, 6), (1, 6), (1, 7)],
            [(6, 0), (6, 1), (7, 1)],
            [(6, 6), (6, 7), (7, 6)],
        ]
        for index, corner in enumerate(corners):
            if self.board[corner[0]][corner[1]] == 0:
                for neighbor in corner_neighbors[index]:
                    if self.board[neighbor[0]][neighbor[1]] == player_to_move:
                        my_tiles += 1
                    elif self.board[neighbor[0]][neighbor[1]] == -player_to_move:
                        opp_tiles += 1
        l = -12.5 * (my_tiles - opp_tiles)
        # Mobility
        my_tiles = len(self.check_possible_moves(player_to_move))
        opp_tiles = len(self.check_possible_moves(-player_to_move))
        if my_tiles > opp_tiles:
            m = (100 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0
        # Final weighted score
        score = (
            (10 * p)
            + (801.724 * c)
            + (382.026 * l)
            + (78.922 * m)
            + (74.396 * f)
            + (10 * d)
        )
        return score

    def check_direction(self, row, col, row_add, col_add, other):
        i = row + row_add
        j = col + col_add
        # check neighbor: other color -> valid move
        if i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other:
            i += row_add
            j += col_add
            while i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other:
                i += row_add
                j += col_add
            if i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == 0:
                return (i, j)

    # lookup
    def is_possible_move(self, row, col, player):
        if player == -1:
            other = 1
        else:
            other = -1

        is_possible_move = []

        for x, y in self.direction:  # 8 direction
            pos = self.check_direction(row, col, x, y, other)  # return posible (x, y)
            if pos:
                is_possible_move.append(pos)
        return is_possible_move

    # get_valid_move
    def check_possible_moves(self, player):
        if player == -1:
            other = 1
        else:
            other = -1

        possible_move = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player:
                    possible_move = possible_move + self.is_possible_move(i, j, player)
        possible_move = list(set(possible_move))
        self.possible_move = possible_move
        return possible_move

    def flip(self, position, x, y, player):  # (x, y) is direction of move
        flip_square = []
        i = position[0] + x
        j = position[1] + y

        if player == -1:
            other = 1
        else:
            other = -1
        if i in range(8) and j in range(8) and self.board[i][j] == other:
            flip_square = flip_square + [(i, j)]
            i = i + x
            j = j + y
        while i in range(8) and j in range(8) and self.board[i][j] == other:
            flip_square = flip_square + [(i, j)]
            i = i + x
            j = j + y
        # print(flip_square)
        if i in range(8) and j in range(8) and self.board[i][j] == player:
            for square in flip_square:
                self.board[square[0]][square[1]] = player

    def apply_move(self, move, player):
        self.possible_move = self.check_possible_moves(player)
        if move in self.possible_move:
            self.board[move[0]][move[1]] = player
            for x, y in self.direction:
                self.flip(move, x, y, player)

        # for i in self.board:
        #   print(i)
