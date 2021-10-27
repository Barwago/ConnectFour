# To create the board, we use matrices to represent each square
import numpy as np
import pygame
import sys
import math

#Globale variabler
ROW_COUNT= 6
COLUMN_COUNT = 7
#RGB Value
GRAY= (159,182,205) 
BLACK = (0,0,0) 
PINK = (255,192,203) 
PURPLE = (218,112,214)

def creat_board():
#Matrix with zeros 7x6
  board = np.zeros((ROW_COUNT,COLUMN_COUNT))
  return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board,col):
#To cheak if a column is full
    return board[ROW_COUNT-1][col] == 0

#Function to see witch row the piece falls on:
def get_next_row(board,col):
    for r in range (ROW_COUNT):
         if board[r][col]==0:
             return r 

#A function for the board
def print_board(board):
  print ( np.flip(board,0))


def winning_move(board,piece):
#Horisontal win:
#Only possible to get horisontol win for 4 of the colums:
 for c in range(COLUMN_COUNT-3):
   for r in range (ROW_COUNT):
      if board[r][c]==piece and board[r][c+1]==piece and  board[r][c+2]==piece and  board[r][c+3]==piece:
          return True
  
  #Vertical win:
 for c in range(COLUMN_COUNT):
    for r in range (ROW_COUNT-3):
      if board[r][c]==piece and board[r+1][c]==piece and  board[r+2][c]==piece and  board[r+3][c]==piece:
          return True

 #Slope (Possitiv):
 for c in range(COLUMN_COUNT-3):
    for r in range (ROW_COUNT-3):
      if board[r][c]==piece and board[r+1][c+1]==piece and  board[r+2][c+2]==piece and  board[r+3][c+3]==piece:
          return True

 #Slope (Negativ):
 for c in range(COLUMN_COUNT-3):
     #4 row:
    for r in range (3,ROW_COUNT-3):
      if board[r][c]==piece and board[r-1][c+1]==piece and  board[r-2][c+2]==piece and  board[r-3][c+3]==piece:
          return True

def draw_board(board):
  for c in range (COLUMN_COUNT):
    for r in range (ROW_COUNT):
      pygame.draw.rect(screen, GRAY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
      pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
 


board = creat_board()
print_board(board)
game_over = False 
turn = 0

#initalize pygame
pygame.init()
 
#define our screen size
SQUARESIZE = 100

#define width and height of board
width = COLUMN_COUNT + SQUARESIZE
height = (ROW_COUNT + 1) + SQUARESIZE
size= (width,height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
#Calling function draw_board again
draw_board(board)
pygame.display.update()

#The game continious till a player gets four in a row
while not game_over:

 for event in pygame.event.get():
   if event.type == pygame.QUIT:
     sys.exit()

   if event.type == pygame.MOUSEBUTTONDOWN:
     print(event.pos)

     #Ask for player 1 input
 if turn == 0:
    posx = event.pos[0]
    col= int(math.floor(posx/SQUARESIZE)) #To round it down to neerest int
        
    if is_valid_location(board, col):
            row=get_next_row(board,col)
            drop_piece(board,row,col, 1)
            if winning_move(board,1):
                print("Player 1 Wins")
                game_over=True


               
     #Ask for player 2 input   
 else: 
   posx = event.pos[0]
   col= int(math.floor(posx/SQUARESIZE)) #To round it down to neerest int
   if is_valid_location(board, col):
             row=get_next_row(board,col)
             drop_piece(board,row,col, 2)
             if winning_move(board,2):
                print("Player 2 Wins")
                game_over=True
                break
 
 print_board(board) 
 turn+=1  
 #Switches between players 1 and 2
 turn=turn%2 
    

