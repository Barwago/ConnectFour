import numpy as np
import pygame
import sys
import math
import random 

#Global Variables:
#RGB Values:
#Used for the graphic of the game:
GRAY= (159,182,205) 
BLACK = (0,0,0)
PINK = (255,192,203) 
PURPLE = (218,112,214)

#How many rows and columns:
ROW_COUNT = 6
COLUMN_COUNT = 7

#Players:
PLAYER = 0
ROBOT = 1

#EMPTY = 0
#Pieces
#PLAYER_P = 1
#ROBOT_P = 2


#Function for the board:
# Use numpy to make a matrix of 5x4 with zeros(epty)
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

#Function for where the pieces falls:
def drop_piece(board, row, col, piece):
	board[row][col] = piece


#Check to see if the column the user selected is open:
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0


#Finds the next available row in the users selected column
#Sees witch row the piece falls on:
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

#Function to print board, but the matrix is fliped so the piece falls to the buttom row 
def print_board(board):
	print(np.flip(board, 0))

# Cheack for winners in the diffrent locations:
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

#With pygames and its functions we can draw how the board looks (The graphics)
def draw_board(board):
# The board 
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, GRAY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
#The pieces	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, PINK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, PURPLE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
#Board is printed to the terminal 
print_board(board)
game_over = False
turn = random.randint(PLAYER,ROBOT)

#Print hvem som starter spillet

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, PURPLE, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("You Win!!", 1, PINK)
						screen.blit(label, (40,10))
						game_over = True
 
					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)                                     
                        
	# # Ask for Player 2 Input
	if turn == ROBOT and not game_over:				

		col = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		#col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, 2)

			if winning_move(board, 2):
				label = myfont.render("Robot Wins!!", 1, PURPLE)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)




        