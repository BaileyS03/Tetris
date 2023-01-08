"""
Author: Bailey Stoodley
Date: 8 Jan 2023
Title: Tetris Game
"""
from os import PRIO_PGRP
import random
## utilising pygame to make key bkngind etc easier
import pygame
import time
from pygame import mixer

COLOURS = [
    (3,65, 174),
    (114, 203, 59),
    (255, 213, 0),
    (255, 151, 28),
    (255, 50, 19),
    (225, 32, 144)
]

COLOURS_PALE = {
    (3,65, 174): (2, 49, 131),
    (114, 203, 59): (86,152,44),
    (255, 213, 0): (191,160,0),
    (255, 151, 28): (223,132,24),
    (255, 50, 19): (191,38,14),
    (225, 32, 144): (191, 24, 108)
}
    
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (128,128,128)
TILE_MATRIX = (4,4)
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 500

"""

TILES FOLLOW GRID AS SUCH
| 0 | 1 | 2 | 3 |
-----------------
| 4 | 5 | 6 | 7 |
-----------------
| 8 | 9 | 10| 11|
-----------------
| 12| 13| 14| 15|

if there is tuples set with missing numbers for the grid above, it is assumed to be 0 / empty.

"""

tiles = {
    "I": [(4,5,6,7), (2,6,10,14), (8,9,10,11), (1,5,9,13)],
    "O": [(0,1,4,5)],
    "S": [(4,5,1,2), (1,5,6,10), (8,9,5,6), (0,4,5,9)],
    "Z": [(0,1,5,6), (9,5,6,2), (4,5,9,10), (8,4,5,1)],
    "L": [(0,4,5,6), (2,1,5,9), (4,5,6,10), (1,5,9,8)],
    "J": [(4,5,6,2), (1,5,9,10), (8,4,5,6), (0,1,5,9)],
    "T": [(1,2,3,6), (2,6,10,7), (5,6,7,10), (2,6,10,5), (5,6,7,2)]
}


class Tile:
    # utilising a grid system in which the tiles are given coords

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name, self.type = random.choice(list(tiles.items()))
        self.rotation = random.randint(0,3) % len(tiles[self.name])
        self.type = self.type[self.rotation]
        self.colour = random.randint(0, len(COLOURS) - 1)

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(tiles[self.name])
        self.type = tiles[self.name][self.rotation]

    def piece(self):
        return tiles[self.name][self.rotation]

    def set_rotation(self, rotation):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y
        
"""Game Logic"""
class Tetris:
    height = 0
    width = 0
    tile = None
    level = 1
    zoom = 20
    x = 100
    y = 60
    score = 0
    
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.score = 0
        self.lines = 0
        self.state = "START"
        self.next_pieces = []

        #now populate game grid
        grid = []
        for row in range(height):
            new_row = []
            for column in range(width):
                new_row.append(0)
            grid.append(new_row)
        self.grid = grid

        for i in range(3):
            x = random.randint(0, self.width//2)
            self.next_pieces.append(Tile(x,0)) 

    def new_tile(self):
        self.tile = self.next_pieces.pop(0)
        x = random.randint(0, self.width//2)
        self.next_pieces.append(Tile(x,0)) 

    def intersection(self):
        intersection = False

        #check each individual block in prefefined matrix above is empty or set
        for row in range(TILE_MATRIX[0]):
            for column in range(TILE_MATRIX[1]):
                   # convert row, column to grid coordinate
                if row * 4 + column in self.tile.piece():
                    if row + self.tile.y > (self.height - 1) or \
                        column + self.tile.x > (self.width - 1) or \
                        column + self.tile.x < 0 or \
                        self.grid[row + self.tile.y][column + self.tile.x] != 0: #checking if the grid coordinate is already occupied
                        intersection = True
        return intersection
        
    def stop_game(self):
        for row in range(TILE_MATRIX[0]):
            for column in range(TILE_MATRIX[1]):
                if row * 4 + column in self.tile.piece() :
                    self.grid[row + self.tile.y][column + self.tile.x] = COLOURS[self.tile.colour]
        self.check_full_line()
        self.new_tile()
        if self.intersection():
            game.state = "gameover"

    def check_full_line(self):
        lines = 0
        for row in range(1, self.height):
            empty = 0
            for column in range(self.width):
                if self.grid[row][column] == 0:
                    empty += 1

            if empty == 0:
                lines += 1
                
                # now need to move everything down
                for rows in range(row, 1, -1):
                    for columns in range(self.width):
                        self.grid[rows][columns] = self.grid[rows-1][columns]

            #now set the new score depending on the lines
            self.score += lines ** 2
            self.lines += lines
            self.level = 1 if self.lines < 10 else self.lines % 10

    def go_down(self):
        self.tile.set_y(self.tile.y + 1)
        if self.intersection():
            self.tile.y -= 1
            self.stop_game()

    def go_side(self, dx):
        prior = self.tile.x
        self.tile.set_x(self.tile.x + dx)
        if self.intersection():
            self.tile.set_x(prior)

    def rotate(self):
        prior = self.tile.get_rotation()
        self.tile.rotate()
        if self.intersection():
            self.tile.set_rotation(prior)

"""Game Engine"""
if __name__ == "__main__":
    pygame.init()
    size = (SCREEN_HEIGHT, SCREEN_WIDTH)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris Game")
    
    mixer.init()
    mixer.music.load('tetris background.mp3')
    mixer.music.play()

    #stop once user click the close button
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20,10)
    counter = 0
    down_button = False
    left_button = False
    right_button = False
    stop = False
    mute = 0
    pause = 0

    while not stop:            
        if game.tile is None:
            game.new_tile()

        counter += 1
        
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level) == 0 or down_button:
            if game.state == "START":
                game.go_down()

        elif left_button:
            game.go_side(-1)
            time.sleep(0.05)

        elif right_button:
            game.go_side(1)
            time.sleep(0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                     game.rotate()
                if event.key == pygame.K_DOWN:
                    down_button = True
                if event.key == pygame.K_LEFT:
                    left_button = True
                if event.key == pygame.K_RIGHT:
                    right_button = True
                if event.key == pygame.K_SPACE:
                    game.rotate()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)
                if event.key == pygame.K_p:
                    pause = (pause + 1) % 2
                    print(pause)
                if event.key == pygame.K_m:
                    mute = (mute + 1) % 2
                    print(mute)
                    if (mute):
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                down_button = False
            elif event.key == pygame.K_LEFT:
                left_button = False
            elif event.key == pygame.K_RIGHT:
                right_button = False

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j + 60,
                                                game.y + game.zoom * i,
                                                game.zoom, game.zoom], 1)
                
                if game.grid[i][j] != 0:
                    x = game.x + game.zoom * j + 61
                    y = game.y + game.zoom * i + 1
                    w = game.zoom - 2
                    h = game.zoom - 1

                    pygame.draw.rect(screen, game.grid[i][j], [x, y, w, h])
                    pygame.draw.polygon(screen, COLOURS_PALE[game.grid[i][j]], [(x,y), (x+w, y), (x+w, y+h)])

        if game.tile is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.tile.piece():
                        x = game.x + game.zoom * (j + game.tile.x) + 61
                        y = game.y + game.zoom * (i + game.tile.y) + 1
                        w = game.zoom - 2
                        h = game.zoom - 2

                        pygame.draw.rect(screen, COLOURS[game.tile.colour],[x,y,w,h])
                        pygame.draw.polygon(screen, COLOURS_PALE[COLOURS[game.tile.colour]], [(x,y), (x+w, y), (x+w, y+h)])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        font2 = pygame.font.SysFont('geneva', 25, True, False)
        font3 = pygame.font.SysFont('Calibri', 20, True, False)
        
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_lines = font.render("Lines: " + str(game.lines), True, BLACK)
        text_tetris = font2.render("TETRIS", True, BLACK)
        text_predict = font3.render("coming up...", True, BLACK)
        text_score_rect = text.get_rect(center=(SCREEN_WIDTH//3.5, SCREEN_HEIGHT+80))
        text_lines_rect = text.get_rect(center=(SCREEN_WIDTH//1.7, SCREEN_HEIGHT+80))
        text_predict_rect = [15,60]
        
        screen.blit(text, text_score_rect)
        screen.blit(text_tetris, [150,20])
        screen.blit(text_lines, text_lines_rect)
        screen.blit(text_predict, text_predict_rect)

        for num, piece in enumerate(game.next_pieces):
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in piece.piece():
                        x = game.zoom * (j) + 40
                        y = game.zoom * (i) + 100 + 115 * num
                        w = game.zoom - 2
                        h = game.zoom - 2
                        pygame.draw.rect(screen, COLOURS[piece.colour],[x,y,w,h])
                        pygame.draw.polygon(screen, COLOURS_PALE[COLOURS[piece.colour]], [(x,y), (x+w, y), (x+w, y+h)])

        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

pygame.quit()