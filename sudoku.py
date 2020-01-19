import pygame
from pygame.locals import *
import sys 
import random



class cube():
    def __init__(self, value, guess, color, cube_number, width=40, offset=40):
        self.value = value
        self.color = color
        self.highlighted_color = (250,0,0,1)
        self.cube_number = cube_number
        self.guess = guess
        self.row = cube_number//9
        self.col = cube_number%9
        self.width = width
        self.offset = offset
        self.x_coord = self.col*self.width+self.offset
        self.y_coord = self.row*self.width+self.offset
        self.rect_coords = (self.x_coord, self.y_coord, self.width, self.width)
        self.center_coords = (self.x_coord + self.width//2, self.y_coord + self.width//2) 
        self.is_clicked = False
    
    def draw_cube(self, surface):
        if self.is_clicked:
            pygame.draw.rect(surface, self.highlighted_color, self.rect_coords, 3)
        else:
            pygame.draw.rect(surface, self.color, self.rect_coords, 1)

    def draw_upper_left_number(self, surface):
        if self.guess != 0:
            myFont = pygame.font.SysFont("comicsans", 25)
            text = myFont.render(str(self.guess), 1, (0,0,0))
            surface.blit(text, self.rect_coords)
    
    def draw_center_number(self, surface):
        if self.value != 0:
            myFont = pygame.font.SysFont("comicsans", 40)
            text = myFont.render(str(self.value), 1, (0,0,0))
            text_rect = text.get_rect(center=self.center_coords)
            surface.blit(text, text_rect)
    


class board():
    def __init__(self, surface, color=(0,0,0)):
        self.surface = surface
        self.color = color
        self.cube_array = []
        self.width = 40
        self.offset = 40
        
    def add_cubes(self, sudoku_matrix, guess_matrix):
        for i in range(len(sudoku_matrix)):
            for j in range(len(sudoku_matrix[i])):
                c = cube(sudoku_matrix[i][j], guess_matrix[i][j], self.color, cube_number=9*i+j)
                self.cube_array.append(c)

    def draw_board(self):
        self.surface.fill((255,255,255))
        drawnHline = False
        drawnVline = False

        # vertical thick lines
        pygame.draw.line(self.surface, self.color, (self.offset+self.width*6, self.offset), (self.offset+self.width*6, self.offset+self.width*9), 4)
        pygame.draw.line(self.surface, self.color, (self.offset+self.width*3, self.offset), (self.offset+self.width*3, self.offset+self.width*9), 4)

        # horizontal thick lines
        pygame.draw.line(self.surface, self.color, (self.offset, self.offset+self.width*3), (self.offset+self.width*9, self.offset+self.width*3), 4)
        pygame.draw.line(self.surface, self.color, (self.offset, self.offset+self.width*6), (self.offset+self.width*9, self.offset+self.width*6), 4)

        for c in self.cube_array:
            c.draw_cube(self.surface)
            c.draw_center_number(self.surface)
            c.draw_upper_left_number(self.surface)

    def click_cube(self, position):
        if position[0] >= self.offset and position[0] <= self.width*9+self.offset and position[1] >= self.offset and position[1] <= self.width*9+self.offset:
            col = (position[0]-self.offset)//self.width
            row = (position[1]-self.offset)//self.width
            return col+row*9
        else:
            return 0

    def highlight_cube(self, cube_number):
        for c in self.cube_array:
            if c.cube_number == cube_number:
                c.is_clicked = True
            else:
                c.is_clicked = False
        self.draw_board()
    
    def change_value(self, cube_number, new_value):
        c = self.cube_array[cube_number]
        c.value = new_value
        self.draw_board()
    
    def check_value(self, cube_number, correct_matrix, key):
        c = self.cube_array[cube_number]
        if key == correct_matrix[c.row][c.col]:
            return True
        else:
            return False


############ end classes ################    


def is_valid(matrix, row_number, col_number, value):
    if valid_box(matrix, row_number, col_number, value) and valid_col(matrix, col_number, value) and valid_row(matrix, row_number, value):
        return True
    else:
        return False

def valid_row(matrix, row_number, value):
    for i in range(9):
        val = matrix[row_number][i]
        if val == value:
            return False
    return True

def valid_col(matrix, col_number, value):
    for i in range(9):
        val = matrix[i][col_number]
        if val == value:
            return False
    return True

def valid_box(matrix, row_number, col_number, value):
    row_number = (row_number//3) * 3
    col_number = (col_number//3) * 3
    for i in range(3):
        for j in range(3):
            val = matrix[i+row_number][j+col_number]
            if val == value:
                return False
    return True

def find_empty(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return [i,j]
    return None

def board_completed(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True

def solve_board(matrix):
    
    row_col = find_empty(matrix)
    if row_col:
        row_number = row_col[0]
        col_number = row_col[1]
    else:
        return True

    for value in range(1,10):
        if is_valid(matrix, row_number, col_number, value):
            matrix[row_number][col_number] = value
            if solve_board(matrix):
                 return True
            
            matrix[row_number][col_number] = 0
    return False

def print_board(matrix):
    print('printing board')
    for i in range(len(matrix)):
        print(matrix[i])
    
##########################################################################################################

sudoku_matrix = [[3,0,6,5,0,8,4,0,0], 
                 [5,2,0,0,0,0,0,0,0], 
                 [0,8,7,0,0,0,0,3,1], 
                 [0,0,3,0,1,0,0,8,0], 
                 [9,0,0,8,6,3,0,0,5], 
                 [0,5,0,0,9,0,6,0,0], 
                 [1,3,0,0,0,0,2,5,0], 
                 [0,0,0,0,0,0,0,7,4], 
                 [0,0,5,2,0,6,3,0,0]] 

answer_matrix = [[3,0,6,5,0,8,4,0,0], 
                 [5,2,0,0,0,0,0,0,0], 
                 [0,8,7,0,0,0,0,3,1], 
                 [0,0,3,0,1,0,0,8,0], 
                 [9,0,0,8,6,3,0,0,5], 
                 [0,5,0,0,9,0,6,0,0], 
                 [1,3,0,0,0,0,2,5,0], 
                 [0,0,0,0,0,0,0,7,4], 
                 [0,0,5,2,0,6,3,0,0]] 

solve_board(answer_matrix)

print_board(sudoku_matrix)
print_board(answer_matrix)


guess_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(9)]



pygame.init()

width = 720
height = 480
surface = pygame.display.set_mode((width, height))
surface.fill((255,255,255))

key = None

board = board(surface)
board.add_cubes(sudoku_matrix, guess_matrix)
board.draw_board()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_1:
                key = 1
            elif key == pygame.K_2:
                key = 2
            elif key == pygame.K_3:
                key = 3
            elif key == pygame.K_4:
                key = 4
            elif key == pygame.K_5:
                key = 5
            elif key == pygame.K_6:
                key = 6
            elif key == pygame.K_7:
                key = 7
            elif key == pygame.K_8:
                key = 8
            elif key == pygame.K_9:
                key = 9
            else: 
                key = None

        if key != None:
            if board.check_value(cube_number, answer_matrix, key):
                board.change_value(cube_number, key)
            key = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            cube_number = board.click_cube(position)
            if cube_number != 0:
                board.highlight_cube(cube_number)
                key = None
            
               

    pygame.display.update()
                
        



