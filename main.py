import pygame
from util_background import *
from util_params import *
from util_player import *
from util_enemy import *
from util_weapons import *
from util_sight import *
from random import randint

# pygame setup
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
# make background by calling the make background function
background = make_background()
# make a player weapon and enemy and sight
player = Player()
enemy_group = pygame.sprite.Group()
# make 10
for i in range(10):
    x_pos = randint(0,WIDTH)
    y_pos = randint(0, HEIGHT)
    enemy_group.add(Enemy(x_pos,y_pos,player))
# set up scoring
score = 0
font = pygame.font.SysFont('Arial',48)
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
    # check collision between bullet and enemy group
    collision = pygame.sprite.groupcollide(player.weapon.bullet_group,enemy_group,True,False)
    #loop through all the bullets that hit the enemy
    for bullet, enemies_hit in collision.items():
        for enemy in enemies_hit:
            #enemy takes damage
            enemy.take_damage(bullet.damage)
            score += 50
    # check collision between enemy group an dplayer 
    collision_2 = pygame.sprite.spritecollide(player,enemy_group,True)
    # loop through all the enemy that hit player
    for enemy in collision_2:
        player.take_damage(enemy.damage)
    # draw background
    screen.blit(background,(0,0))
    # RENDER YOUR GAME HERE((
    player.draw(screen)
    enemy_group.draw(screen)
    # draw and update my score
    # convert to string, only strings can be printed out
    score_string = f'{score}'
    score_surface = font.render(score_string, True, (255,0,0))
    screen.blit(score_surface,(0,0))
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()