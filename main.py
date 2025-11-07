import pygame
from util_background import *
from util_params import *
from util_player import *
from util_enemy import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True



# make background by calling the make background function
background = make_background()

# make a player
player = Player()

#make enemy 
enemy_group = pygame.sprite.Group()

# make 10
for i in range(10):
    x_pos = randint(0,WIDTH)
    y_pos = randint(0, HEIGHT)
    enemy_group.add(Enemy(x_pos,y_pos,player))

########### TESTING ZONE #################



##########################################

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # event
        player.check_event(event)

    # update our player
    player.update()
    enemy_group.update()


    #draw background
    screen.blit(background,(0,0))
    


    # RENDER YOUR GAME HERE((
    player.draw(screen)
    enemy_group.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()