import pygame
import os

import math
from .util_params import * 
from random import randint

def make_background():
    # I am making a tiled back ground
    # I made the tile location and the tile
    sand_tile_location = os.path.join(BG_DIR, 'tile_0055.png')
    sand_tile = pygame.image.load(sand_tile_location)
    
    cactus_tile_location = os.path.join(BG_DIR, 'tile_0063.png')
    cactus_tile = pygame.image.load(cactus_tile_location)

    sky_tile_location = os.path.join(BG_DIR, 'tile_0024.png')
    sky_tile = pygame.image.load(sky_tile_location)


    # I am getting the width and height for the tile
    sand_tile_width = sand_tile.get_width()
    sand_tile_height = sand_tile.get_height()
    
    sky_tile_width = sky_tile.get_width()
    sky_tile_height = sky_tile.get_height()

    # make surface backgorung with thesame width and height as the screen
    background = pygame.Surface((WIDTH,HEIGHT))

    #loop over the background and put the tiles on it
    for x in range(0,WIDTH,sand_tile_width):
        for y in range(0,HEIGHT,sand_tile_height):
            background.blit(sand_tile, (x,y))

    for x in range(0,WIDTH,sky_tile_width):
        for y in range(0,200,sky_tile_height):
            background.blit(sky_tile,(x,y))

    # make the cactus tile, put 20 at random tiles
    num_cactus = 20
    for i in range(num_cactus):
        x = randint(0,WIDTH)
        y = randint(500,HEIGHT)
        
        #blit them cactus
        background.blit(cactus_tile,(x,y))
    
    # return the background
    return background