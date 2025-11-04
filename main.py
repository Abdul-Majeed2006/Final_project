import pygame
from util_background import *
from util_params import *
from util_player import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True



# make background by calling the make background function
background = make_background()

# make a player
player = Player()

########### TESTING ZONE #################



##########################################

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    
    screen.blit(background,(0,0))
    


    # RENDER YOUR GAME HERE((
    player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()