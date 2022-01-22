# Python library used:
import numpy as np
from numpy.core.defchararray import count, title
import pygame
import time
import sys
import math
import random
from tkinter import *   
 
#Library to send data to UR robot
import socket

#Sources:
#https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
#https://github.com/sebadorn/Machine-Learning--Connect-Four/blob/master/game.py
#https://cpb-us-w2.wpmucdn.com/u.osu.edu/dist/b/69689/files/2018/12/Connect-Four-Main-Code-2dct7ox.pdf


# Global Variables:
# RGB Values:
# Used for the graphic of the game:
GRAY = (159, 182, 205)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
PURPLE = (218, 112, 214)

# How many rows and columns:
ROW_Q= 6
COLUMN_Q = 7

# Players:
ROBOT = 1
PLAYER = 0


#Used when making the AI:
SQR_LENGHT = 4
EMPTY = 0


# Function for the board:
# Use numpy to make a matrix of 7x6 with zeros(epty)
def make_board():
    board = np.zeros((ROW_Q, COLUMN_Q))
    return board

# Check to see if the column the user selected is open:
#is it a reasonable location
def is_rsm_location(board, col):
    return board[ROW_Q-1][col] == 0


# Function for where the pieces falls:
def where_pieces_fell(board, row, col, piece):
    board[row][col] = piece


# Finds the next available row in the users selected column
# Sees witch row the piece falls on:
def get_next_row(board, col):
    for r in range(ROW_Q):
        if board[r][col] == 0:
            return r


def get_next_col(board, col):
    for r in range(ROW_Q):
        if board[r][col] == 0:
            return col+1  # Gives column


# Function to print board, but the matrix is fliped so the piece falls to the buttom row
def print_board(board):
    print(np.flip(board, 0))


# Cheack for winners in the diffrent locations:
def winner_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_Q-3):
        for r in range(ROW_Q):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_Q-3):
        for r in range(3, ROW_Q):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

     # Check positively sloped diaganols
    for c in range(COLUMN_Q-3):
        for r in range(ROW_Q-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_Q):
        for r in range(ROW_Q-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True




def evaluate_sqr(sqr, piece):
    score = 0
   # When the robot plays, we are the opponent
    opponent = 1

 # If we are the ones playing the opponent piece changes to the robot
    if piece == 1:
        opponent = 2

# We get a high score if we get four in a row in given direction:
    if sqr.count(piece) == 4:
        score += 200
   # Lower score if it's 3 in row
    elif sqr.count(piece) == 3 and sqr.count(EMPTY) == 1:
        score += 20
    # And a even lower score if it's only 2 in row
    elif sqr.count(piece) == 2 and sqr.count(EMPTY) == 2:
        score += 10

   # If we have 3 in row it will always try to block us, but we get less point then:
   # Doesn't affect us even if player becomes opp_piece, remember we can choose position
    if sqr.count(opponent) == 3 and sqr.count(EMPTY) == 1:
        score -= 180

  # If you want the Robot to block your every move, add this
  # elif sqr.count(opponent) == 2 and sqr.count(EMPTY) == 2:
    # score -= 40
    return score


def score_position(board, piece):
    score = 0

     # Score Verdical
    for c in range(COLUMN_Q):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_Q-3):
            sqr = col_array[r:r+SQR_LENGHT]
            score += evaluate_sqr(sqr, piece)
  
    # Positiv sloped
    for r in range(ROW_Q-3):
        for c in range(COLUMN_Q-3):
            # the row and column increases for each i, with i:
            sqr = [board[r+i][c+i] for i in range(SQR_LENGHT)]
            score += evaluate_sqr(sqr, piece)

     # Negativ sloped
    for r in range(ROW_Q-3):
        for c in range(COLUMN_Q-3):
            # the row increases while the column decreases for each i:
            # The first row has to atleast be 3 abow for it to make a negative sloope
            # Therfor it start with +3 and for each i it decreases with i
            sqr = [board[r+3-i][c+i] for i in range(SQR_LENGHT)]
            score += evaluate_sqr(sqr, piece)          

    # Score Horrisontal
    for r in range(ROW_Q):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_Q-3):
            sqr = row_array[c:c+SQR_LENGHT]
            score += evaluate_sqr(sqr, piece)

    return score


def get_empty_location(board):
    empty_locations = []
    for col in range(COLUMN_Q):
        if is_rsm_location(board, col):
            empty_locations.append(col)
    return empty_locations


def pick_best_place(board, piece):
    empty_locations = get_empty_location(board)
    best_score = -10000
    # Random place, but it has to be free
    # Start with saying best column is in a random place
    best_col = random.choice(empty_locations)

    for col in empty_locations:
        row = get_next_row(board, col)
        temp_board = board.copy()  # Looks at a copy of the board to find place to put the piece
        where_pieces_fell(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
      # Compares till we get the best score, and the biggest score becomes the new best score
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def placement(board):
    location_row = get_next_row(board, col)
    location_col = get_next_col(board, col)
    location = (location_row, location_col)
    return location


def case():
   location = placement(board)
   '''
   place =  [7, 6, 5, 4, 3, 2, 1,
             14,13,12, 11, 10, 9, 8,
             21,20, 19, 18, 17, 16,15,
             28, 27, 26, 25, 24,23, 22,  
             35, 34, 33, 32 , 31, 30, 29,
             42,41, 40, 39, 38, 37, 36 ]

   place =  [42, 41, 40, 39, 38, 37, 36,
             35,34,33, 32, 31, 30, 29,
             28,27, 26, 25, 24, 23,22,
             21, 20, 19, 18, 17,16, 15,  
             14, 13, 12, 11 , 10, 9, 8,
             7,6, 5, 5, 3, 2, 1 ]

'''
   place =  [1, 2, 3, 4, 5, 6, 7,
             8,9,10, 11, 12, 13, 14,
             15,16, 17, 18, 19, 20,21,
             22, 23, 24, 25, 26,27, 28,  
             29, 30, 31, 32 , 33, 34, 35,
             36,37, 38, 39, 40, 41, 42 ]


   condition = [(location == (1,1)),(location == (1,2)),
                (location == (1,3)),(location == (1,4)),(location == (1,5)),
                (location == (1,6)),(location == (1,7)),
                
                (location == (2,1)),(location == (2,2)),
                (location == (2,3)),(location == (2,4)),(location == (2,5)),
                (location == (2,6)),(location == (2,7)),
                
                (location == (3,1)),(location == (3,2)),
                (location == (3,3)),(location == (3,4)),(location == (3,5)),
                (location == (3,6)),(location == (3,7)),
                
                (location == (4,1)),(location == (4,2)),
                (location == (4,3)),(location == (4,4)),(location == (4,5)),
                (location == (4,6)),(location == (4,7)),
                
                (location == (5,1)),(location == (5,2)),
                (location == (5,3)),(location == (5,4)),(location == (5,5)),
                (location == (5,6)),(location == (5,7)),
                
                (location == (6,1)),(location == (6,2)),
                (location == (6,3)),(location == (6,4)),(location == (6,5)),
                (location == (6,6)),(location == (6,7)) ]
       
   case = np.select(condition, place, default=42)
   return case


# With pygames and its functions we can draw how the board looks (The graphics)
def look_board(board):
    # The board
    for c in range(COLUMN_Q):
        for r in range(ROW_Q):
            pygame.draw.rect(screen, GRAY, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
# The pieces
    for c in range(COLUMN_Q):
        for r in range(ROW_Q):
            if board[r][c] == 1:
                pygame.draw.circle(screen, PINK, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PURPLE, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

'''
#Socket Conection:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host= socket.gethostname() 
Port= 1234 
msg=''
#Socket is the end point that recives data
#We send and recive data with socket
server.bind((Host, Port)) #Socket connection
server.listen()
clientsocket, address = server.accept() #If anyone tries to connect, we accept
#data = clientsocket.recv(1024) 
#print(data.decode('utf-8')) #Til string 
print(f"connection from {address} has been established!")
'''


board = make_board()
# Board is printed to the terminal
print_board(board)
game_over = False
turn = random.randint(0, 1)

'''
#Sends info about the player who starts the game:
if turn==0:
    msg="red"
elif turn==1:
    msg="blue"    

clientsocket.send(bytes(msg, "utf-8")) #Send info to clientsocket
'''


#For the visual of the game:
pygame.init()
SQUARESIZE = 100
width = COLUMN_Q * SQUARESIZE
height = (ROW_Q+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode((width, height))
look_board(board)
pygame.display.update()
The_font = pygame.font.SysFont("monospace", 75)


#So the player can choose the diffrent types of games:
#want=int(input("What do you want to play? \nType: 1,2, or 3 \n1: Easy AI/Garanteed Win, 2: Two Player, 3: Robot\n  "))

'''
#Sends info about which player who starts to robot 
if want==1 or want==2 or want==3:
    msg="want"
clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
'''
want=1

#Game starts:
if want == 1:

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                pos = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, PINK, (pos, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, PURPLE, (pos, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == PLAYER:
                    pos = event.pos[0]
                    col = int(math.floor(pos/SQUARESIZE))

                    if is_rsm_location(board, col):
                        row = get_next_row(board, col)
                        where_pieces_fell(board, row, col, 1)

                        if winner_move(board, 1):
                            title = The_font.render("You Win!!", 1, PINK)
                            screen.blit(title, (40,10))
                            game_over = True
                        
                        #Which grid the piece fell in
                        #place=case()
                        #msg=str(place)
                        #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
                        turn = 1

                        print_board(board)
                        look_board(board)                                     
                            
        #  Player 2 Input
        if turn == ROBOT and not game_over:				

            col = random.randint(0, COLUMN_Q-1)

            if is_rsm_location(board, col):
                pygame.time.wait(1000) #1 second waiting time
                row = get_next_row(board, col)
                where_pieces_fell(board, row, col, 2)

                if winner_move(board, 2):
                    title = The_font.render("Robot Wins!!", 1, PURPLE)
                    screen.blit(title, (40,10))
                    game_over = True

                print_board(board)
                look_board(board)
                #Which grid the piece fell in
                #place=case()
                #msg=str(place)
                #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
                turn = 0

        if game_over:
            pygame.time.wait(3000)

elif want==2:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                pos = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, PINK, (pos, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, PURPLE, (pos, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    pos = event.pos[0]
                    col = int(math.floor(pos/SQUARESIZE))

                    if is_rsm_location(board, col):
                        row = get_next_row(board, col)
                        where_pieces_fell(board, row, col, 1)

                        if winner_move(board, 1):
                            title = The_font.render("Player 1 wins!!", 1, PINK)
                            screen.blit(title, (40,10))
                            game_over = True
                     #Which grid the piece fell in
                        #place=case()
                        #msg=str(place)
                       #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket



                            
            # # Ask for Player 2 Input
                else:				
                    pos = event.pos[0]
                    col = int(math.floor(pos/SQUARESIZE))

                    if is_rsm_location(board, col):
                        row = get_next_row(board, col)
                        where_pieces_fell(board, row, col, 2)

                        if winner_move(board, 2):
                            title = The_font.render("Player 2 wins!!", 1, PURPLE)
                            screen.blit(title, (40,10))
                            game_over = True

                print_board(board)
                look_board(board)
                #Which grid the piece fell in
                #place=case()
                #msg=str(place)
                #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket

                #Alternating between player 1 and player 2:
                turn += 1
                turn = turn % 2


                if game_over:
                    pygame.time.wait(3000)


elif want==3:

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                pos = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(
                        screen, PINK, (pos, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(
                        screen, PURPLE, (pos, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Ask for Player 1 Input
                if turn == PLAYER:
                    pos = event.pos[0]
                    col = int(math.floor(pos/SQUARESIZE))

                    if is_rsm_location(board, col):
                        row = get_next_row(board, col)
                        where_pieces_fell(board, row, col, 1)

                        if winner_move(board, 1):
                            title = The_font.render("You Win!!", 1, PINK)
                            screen.blit(title, (40, 10))
                            game_over = True
                        
                        #Which grid the piece fell in
                        #place=case()
                        #msg=str(place)
                        #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
                        turn=1
                        print_board(board)
                        look_board(board)

        # # Ask for Player 2 Input
        if turn == ROBOT and not game_over:

            col = pick_best_place(board, 2)
            

            if is_rsm_location(board, col):
                pygame.time.wait(1000) # One second waiting time
                row = get_next_row(board, col)
                where_pieces_fell(board, row, col, 2)

                if winner_move(board, 2):
                    title = The_font.render("Robot Wins!!", 1, PURPLE)
                    screen.blit(title, (40, 10))
                    game_over = True
                
                #Which grid the piece fell in
                #place=case()
                #msg=str(place)
                #clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
            
                print_board(board)
                look_board(board)
                turn=0
                 
        if game_over:
         pygame.time.wait(3000)

            
'''
if game_over==True:
    place=case()
    msg=str(place)
    clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
    time.sleep(5000)
    msg="Game over"
    clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
    clientsocket.close()

'''

