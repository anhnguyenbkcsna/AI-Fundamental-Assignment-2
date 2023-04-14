import time
import random
from config import *
from copy import deepcopy

from config import *
from copy import deepcopy

class Board:
  def __init__(self):
    # board[row][col] in UI
    self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, -1, 0, 0, 0],
                  [0, 0, 0, -1, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]
    self.possible_move = []
    self.direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
  def update_board(self, cur_state):
    self.board = cur_state
    return self.board
  def current_board(self):
    return self.board
  
  def check_direction(self, row, col, row_add, col_add, other):
    i = row + row_add
    j = col + col_add
    # check neighbor: other color -> valid move
    if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other):
      i += row_add
      j += col_add
      while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other):
        i += row_add
        j += col_add
      if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == EMPTY):
        return (i, j)
  
  #lookup
  def is_possible_move(self, row, col, player):
    if player == -1:
      other = 1
    else: other = -1
    
    is_possible_move = []
    
    for (x, y) in self.direction: # 8 direction
      pos = self.check_direction(row, col, x, y, other) # return posible (x, y)
      if pos: 
        is_possible_move.append(pos)
    return is_possible_move

  #get_valid_move
  def check_possible_moves(self, player):
    if player == -1:
      other = 1
    else: other = -1

    possible_move = []
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == player:
          possible_move = possible_move + self.is_possible_move(i, j, player)
    possible_move = list(set(possible_move))
    self.possible_move = possible_move
    return possible_move

  def flip(self, position, x, y, player): # (x, y) is direction of move
    flip_square = []
    i = position[0] + x
    j = position[1] + y
    
    if player == -1:
      other = 1
    else: other = -1
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
    if move in self.possible_move:
      self.board[move[0]][move[1]] = player
      for (x, y) in self.direction:
        self.flip(move, x, y, player)

def select_move(cur_state, player_to_move, remain_time):
	NewBoard = Board()
	NewBoard.update_board(cur_state)
	start_time = time.time()
	
	possible_move = NewBoard.check_possible_moves(player_to_move)
	if possible_move:
		selected_move = random.choice(possible_move)

		end_time = time.time()
		computer_time = round(end_time - start_time, 2)
		remain_time -= computer_time
		if computer_time > 3:
			print('Computer: Time out!!!')
		return selected_move, remain_time
	else: 
		print('Computer: Out of moves!')
	return None