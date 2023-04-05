import pygame
import sys
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

def play():
	running = True
	clicked = False
	player = -1 # X go first
	PlayingBoard = Board()
	clicked_square = []
  
	while running:
		screen.fill((151, 222, 255))  # background
		# cursor
		pos = pygame.mouse.get_pos()
		mouse_x = pos[0]
		mouse_y = pos[1]
		square = move(mouse_x, mouse_y, player)
  
		for event in pygame.event.get(): # quit game
			if event.type == pygame.QUIT:
				running = False
			# check Mouse
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
				stepText = my_font.render('Clicking...', False, (0, 0, 0))
				screen.blit(stepText, (800, 0))
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked_square += square
				board[square[0]][square[1]] = player
				clicked = False
				player = -player # X -> O || O -> X

  	# Debug mouse cursor
		stepText = my_font.render('Mouse {}'.format(square), False, (0, 0, 0))
		screen.blit(stepText, (0, 0))
  	
		stepText = my_font.render('Move {}'.format(clicked_square), False, (0, 0, 0))
		screen.blit(stepText, (0, 50))

		# init board
		board = PlayingBoard.current_board()
		for row in range(8):
			for col in range(8):
				pygame.draw.rect(screen, (83, 127, 231), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit), 1)   # border
				if board[row][col] == -1: # X
					pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit))
				elif board[row][col] == 1: # O
					pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(row*unit + start_x, col*unit + start_y, unit, unit))
		pygame.display.update()

# Run game
# def main():
play()