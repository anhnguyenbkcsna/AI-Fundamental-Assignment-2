import pygame
import sys
import time
import random
from board import *
from config import *

# intialize the pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 48)

# screen_size
screen_size = (1000, 800)
unit = 80
start_x = (screen_size[0] - 80 * 8)/2
start_y = (screen_size[1] - 80 * 8)/2

# create the screen
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Reversi")
pygame.display.set_icon(pygame.image.load('./assets/logo.png'))

def move(mouse_x, mouse_y, player):
	pos_x = int((mouse_x - start_x)/80)
	pos_y = int((mouse_y - start_y)/80)
	return (pos_x, pos_y)

def select_move(cur_state, player_to_move, remain_time):
	NewBoard = Board()
	NewBoard.update_board(cur_state)
	start_time = time.time()
	
	possible_move = NewBoard.check_possible_moves(player_to_move)
	if possible_move:
		selected_move = random.choice(possible_move)

		end_time = time.time()
		computer_time = round(end_time - start_time, 2)
		print('Computer time: ', computer_time)
		remain_time -= computer_time
		if computer_time > 3:
			print('Computer: Time out!!!')
		return selected_move, remain_time
	else: 
		print('Computer: Out of moves!')
	end_time = time.time()
	computer_time = round(end_time - start_time, 2)
	remain_time -= computer_time
	if computer_time > 3:
		print('Computer: Time out!!!')
	return None, remain_time
  
def play():
	running = True
	clicked = False
	player_to_move = -1 # X go first
	is_player_move = True
 
	PlayingBoard = Board()
	clicked_square = []

	# remaining time
	X_time = 60
	O_time = 60
	player_start_time = time.time()
	player_end_time = 0
  
	while running:
		screen.fill((151, 222, 255))  # background
		# cursor
		pos = pygame.mouse.get_pos()
		mouse_x = pos[0]
		mouse_y = pos[1]
		square = move(mouse_x, mouse_y, player_to_move)

  		# Debug mouse cursor
		stepText = my_font.render('Mouse {}'.format(square), False, (0, 0, 0))
		screen.blit(stepText, (0, 0))

		# init board
		board = PlayingBoard.current_board()
		for col in range(8):
			for row in range(8):
				pygame.draw.rect(screen, (83, 127, 231), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit), 1)   # border
				if board[row][col] == -1: # X
					pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit))
				elif board[row][col] == 1: # O
					pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit))

# computer move
		if is_player_move == False:
			possible_move = PlayingBoard.check_possible_moves(player_to_move)
			selected_move, O_time = select_move(board, player_to_move, O_time) # receive tuple of move from Computer
			if selected_move in possible_move:
				board = PlayingBoard.apply_move(selected_move, player_to_move)

			player_to_move = - player_to_move # X -> O || O -> X
			is_player_move = True
			player_start_time = time.time()
   
# player move
		for event in pygame.event.get(): # quit game
			if event.type == pygame.QUIT:
				running = False
			# check Mouse
			if event.type == pygame.MOUSEBUTTONDOWN and is_player_move == True:
				clicked = True

			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				possible_move = PlayingBoard.check_possible_moves(player_to_move)
				if possible_move == []:
					# computer win
					count_X, count_Y = PlayingBoard.count()
					print(count_X, count_Y)
					print('Player: Out of moves!')

				# Highlight for possible_move into yellow
				clicked_square += square
				if square in possible_move:
					board = PlayingBoard.apply_move(square, player_to_move)
					player_to_move = - player_to_move # X -> O || O -> X
					is_player_move = False
				clicked = False
				
				player_end_time = time.time()
				player_time = round(player_end_time - player_start_time, 2)
				print('Player time: ', player_time)
				if player_time > 3:
					print('Player: Time out!')
		pygame.display.update()
# Run game
# def main():
play()