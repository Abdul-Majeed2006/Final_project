import pygame
from util_params import * 
from random import randint

def make_background():
    # I am making a tiled back ground
    # I made the tile location and the tile
    sand_tile_location = 'assets/bg/tile_0055.png'
    sand_tile = pygame.image.load(sand_tile_location)
    
    cactus_tile_location = 'assets\bg\tile_0063.png'
    cactus_tile = pygame.image.load(cactus_tile_location)

    # I am getting the width and height for the tile
    tile_width = sand_tile.get_width()
    tile_height = sand_tile.get_height()
    
    # make surface backgorung with thesame width and height as the screen
    background = pygame.Surface((WIDTH,HEIGHT))

    #loop over the background and put the tiles on it
    for x in range(0,WIDTH,tile_width):
        for y in range(0,HEIGHT,tile_height):
            background.blit(sand_tile, (x,y))

    # make the cactus tile, put 20 at random tiles

    
    # return the background
    return background