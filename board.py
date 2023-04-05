from config import *
from copy import deepcopy

class Board:
  def __init__(self):
    self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, -1, 0, 0, 0],
                  [0, 0, 0, -1, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]
    self.possible_move = 0
    self.direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
  def current_board(self):
    return self.board
  
  def is_possible_move(self, row, col, player):
    if player == X:
      other = O
    else: other = X
    
    possibleMove = []
    
    for (x, y) in self.direction: # 8 direction
      pos = self.check_direction(row, col, x, y, other) # return posible (x, y)
      if pos: 
        possibleMove.append(pos)
  
  def check_direction(self, row, col, row_add, col_add, other):
    i = row + row_add
    j = col + col_add
    # check neighbor: other color -> valid move
    while (i > 0 and i < 8 and j > 0 and j < 8 and self.board[i][j] == other):
      # can move -> move to next square in its direction
      i += row_add
      j += col_add
    if (i > 0 and i < 8 and j > 0 and j < 8 and self.board[i][j] == EMPTY):
      return (i, j)
    
  def check_possible_moves(self, player):
    if(player == X):
      other = O
    else: other = X
    
    possible_move = []
    for i in range(8):
      for j in range(8):
        if self.board == player:
          possible_move = possible_move + self.is_possible_move(i, j, player)
    possible_move = list(set(possible_move))
    self.possible_move = possible_move
    return possible_move
  
  def apply_move(self, move, player):
    if move in self.possible_move:
      self.board[move[0]][move[1]] = player
      for (x, y) in self.direction:
        self.flip(move, x, y, player)
  def flip(self, position, x, y, player): # (x, y) is direction of move
    flip_square = []
    i = position[0] + x
    j = position[1] + y
    
    if player == X:
      other = O
    else: other = X
    
    # if i in range(8) and j in range(8) and self.board[i][j] == other:
    #   flip_square = flip_square + [(i, j)]
    #   i = i + x
    #   j = j + y
    while i in range(8) and j in range(8) and self.board[i][j] == other:
      flip_square = flip_square + [(i, j)]
      i = i + x
      j = j + y
    if i in range(8) and j in range(8) and self.board[i][j] == player:
      for square in flip_square:
        self.board[square[0]][square[1]] == player
