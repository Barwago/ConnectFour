# Python library used:
import numpy as np
from numpy.core.defchararray import count
import pygame
import sys
import math
import random
from tkinter import *   
 
#Library to send data to UR robot
import socket



# Global Variables:
# RGB Values:
# Used for the graphic of the game:
GRAY = (159, 182, 205)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
PURPLE = (218, 112, 214)

# How many rows and columns:
ROW_COUNT = 6
COLUMN_COUNT = 7

# Players:
PLAYER = 0
ROBOT = 1

WINDOW_LENGHT = 4

EMPTY = 0

#PLAYER_P = 1
#ROBOT_P = 2


# Function for the board:
# Use numpy to make a matrix of 7x6 with zeros(epty)
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Function for where the pieces falls:


def drop_piece(board, row, col, piece):
    board[row][col] = piece


# Check to see if the column the user selected is open:
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


# Finds the next available row in the users selected column
# Sees witch row the piece falls on:
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def get_next_open_col(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return col+1  # Gives column


# Function to print board, but the matrix is fliped so the piece falls to the buttom row

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


def evaluate_window(window, piece):
    score = 0
   # When the robot plays, we are the opponent
    opp_piece = 1

 # If we are the ones playing the opponent piece changes to the robot
    if piece == 1:
        opp_piece = 2

# We get a high score if we get four in a row in given direction:
    if window.count(piece) == 4:
        score += 100
   # Lower score if it's 3 in row
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    # And a even lower score if it's only 2 in row
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

   # If we have 3 in row it will always try to block us, but we get less point then:
   # Doesn't affect us even if player becomes opp_piece, remember we can choose position
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

  # If you want the Robot to block your every move, add this
  # elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
    # score -= 40
    return score


def score_position(board, piece):
    score = 0

    # Score center column
    #center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    #center_count = center_array.count(piece)
    #score += center_count * 6

    # Score Horrisontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGHT]
            score += evaluate_window(window, piece)
     # Score Verdical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGHT]
            score += evaluate_window(window, piece)

    # Positiv sloped
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # the row and column increases for each i, with i:
            window = [board[r+i][c+i] for i in range(WINDOW_LENGHT)]
            score += evaluate_window(window, piece)

     # Negativ sloped
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # the row increases while the column decreases for each i:
            # The first row has to atleast be 3 abow for it to make a negative sloope
            # Therfor it start with +3 and for each i it decreases with i
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGHT)]
            score += evaluate_window(window, piece)

    return score


def get_valid_location(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_location(board)
    best_score = -10000
    # Random place, but it has to be free
    # Start with saying best column is in a random place
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()  # Looks at a copy of the board to find place to put the piece
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
      # Compares till we get the best score, and the biggest score becomes the new best score
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def placement(board):
    location_row = get_next_open_row(board, col)
    location_col = get_next_open_col(board, col)
    location = (location_row, location_col)
    return location


def case():
   location = placement(board)
   place =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              11, 12, 13, 14, 15, 16, 17, 18,
              19, 20, 21, 22, 23, 24, 25, 26,
              27, 28, 29, 30, 31, 32, 33, 34,
              35, 36, 37, 38, 39, 40, 41, 42]

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
 
def socet(game_over, turn):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  #UR IP adress
    #Loopback adresse, bruk adressen til robotene 
    port = 2222
    client.connect((host,port)) #Socket oppkobling

    while not game_over:
          #Les inn beskjed fra brukeren
         #client.send(bytes(case(),'utf-8')) #Sender data til robotstudio
         client.send(bytes(turn,'utf-8')) #Sender data til robotstudio
        
         data = client.recv(1024) #Motta data fra robotstudio:
         print(data.decode('utf-8')) #Make it into string
        
    client.close() #Close the connection
    

# With pygames and its functions we can draw how the board looks (The graphics)
def draw_board(board):
    # The board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GRAY, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
# The pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, PINK, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PURPLE, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


def button():    # import everything from tkinter module
    #create a tkinter window
    root = Tk()             
    # Open window having dimension 100x100
    root.geometry('100x100')
     #Create a Button
    btn1 = Button(root, text = 'Easy AI!', bd = '5',
                            command = onclick(1) )
    
    btn2 = Button(root, text = 'Two Player!', bd = '5',
                            command = onclick2() )
    
    btn3 = Button(root, text = 'Hard Game!', bd = '5',
                            command = onclick3())
    # Set the position of button on the top of window.  
    btn1.pack(side = 'top')   
    btn2.pack(side = 'top')  
    btn3.pack(side = 'top')    
    root.mainloop()

def onclick(want):
    

def onclick2():
    

def onClick3():
      


board = create_board()
# Board is printed to the terminal
print_board(board)
game_over = False
turn = random.randint(PLAYER, ROBOT)

# Print hvem som starter spillet

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

button()

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

if onclick():
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


elif onclick2():
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
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
                            label = myfont.render("Player 1 wins!!", 1, PINK)
                            screen.blit(label, (40,10))
                            game_over = True
                                        
                            
            # # Ask for Player 2 Input
                else:				
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, PURPLE)
                            screen.blit(label, (40,10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)


elif onClick3():
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(
                        screen, PINK, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(
                        screen, PURPLE, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("You Win!!", 1, PINK)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2
                        #socket(game_over,turn) 
                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == ROBOT and not game_over:

            #col = random.randint(0, COLUMN_COUNT-1)
            col = pick_best_move(board, 2)
            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(1000)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("Robot Wins!!", 1, PURPLE)
                    screen.blit(label, (40, 10))
                    game_over = True
            
                
                print_board(board)
                draw_board(board)
                #socket(game_over,turn) 
                turn += 1
                turn = turn % 2
                

        if game_over:
            pygame.time.wait(3000)



