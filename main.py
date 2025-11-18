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
# game state title, playing, game over
game_state = 'Title'
# make background by calling the make background function
background = make_background()
# make a player weapon and enemy and sight
player = Player()
enemy_group = pygame.sprite.Group()
# set up scoring, set up wave
wave_number = 1
score = 0
font = pygame.font.SysFont('Arial',48)
# fonts fro different screen
title_font = pygame.font.SysFont('Arial',80)
prompt_font = pygame.font.SysFont('Arial',30)
wave_message_font = pygame.font.SysFont('Arial',60)
wave_message = None
wave_message_timer = 0
wave_message_duration = 180 # 3 seconds, 180fps/60fps
#initial wave
for i in range(10):
    x_pos = randint(0,WIDTH)
    y_pos = randint(0,HEIGHT)
    enemy_group.add(Enemy(x_pos,y_pos,player,wave_number))
########### TESTING ZONE #################

##########################################
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # event based on the game state
        if game_state == 'Title':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:# enter key
                    game_state = 'Playing'

        elif game_state == 'Playing':
            #event
            player.check_event(event)
        elif game_state == 'Gameover':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #R to restart game
                    #reset the game
                    score = 0
                    player.reset()
                    enemy_group.empty()
                    for i in range(10):
                        x_pos = randint(0,WIDTH)
                        y_pos = randint(0,HEIGHT)
                        enemy_group.add(Enemy(x_pos,y_pos,player,wave_number))
                    #set the game to playing
                    game_state = 'Playing'
    # draw background
    screen.blit(background,(0,0))
    #now update game based on the value of game state
    if game_state == 'Title':
        # draw title screen
        title_text = title_font.render('My shooter game',True,(255,0,0))
        prompt_text = prompt_font.render('press Enter to start',True,(255,255,255))
        # make sure the text is i  center
        title_rect = title_text.get_rect(center=(WIDTH/2,(HEIGHT/2)-50))
        prompt_rect = prompt_text.get_rect(center=(WIDTH/2,(HEIGHT/2) +50))
        screen.blit(title_text,title_rect)
        screen.blit(prompt_text,prompt_rect)
    elif game_state == 'Playing':
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
        # check for waves
        if not enemy_group: # if enemygroup is empty
            wave_number +=1
            #wave message
            wave_message_text = f'WAVE: {wave_number}'
            wave_message = wave_message_font.render(wave_message_text,True,(255,0,0))
            wave_message_timer = wave_message_duration
            #spawn new enemies
            for i in range (10):
                x_pos = randint(0,WIDTH)
                y_pos = randint(0,HEIGHT)
                enemy_group.add(Enemy(x_pos,y_pos,player,wave_number))
        # RENDER YOUR GAME HERE((
        player.draw(screen)
        enemy_group.draw(screen)
        # draw and update my score
        # convert to string, only strings can be printed out
        score_string = f'{score}'
        score_surface = font.render(score_string, True, (255,0,0))
        screen.blit(score_surface,(0,0))
        #draw wave message
        if wave_message_timer > 0:
            wave_message_rect = wave_message.get_rect(center=(WIDTH/2,(HEIGHT/2)-100))
            screen.blit(wave_message,wave_message_rect)
            wave_message_timer -=1
        # kill player when health = 0 'Gameover'
        if player.health <= 0:
            player.kill()
            game_state = 'Gameover'
    elif game_state == 'Gameover':
        # draw gamw over screen
        player.draw(screen)
        enemy_group.draw(screen)
        #draw players score
        score_string = f'{score}'
        score_surface = font.render(score_string,True,(255,0,0))
        screen.blit(score_surface,(0,0))
        #draw gameover text
        title_text = title_font.render('Game Over',True,(255,0,0))
        prompt_text = prompt_font.render('Press R to Restart',True,(255,255,255))
        #ceter texts
        title_rect = title_text.get_rect(center=(WIDTH/2,(HEIGHT/2)-50))
        prompt_rect = prompt_text.get_rect(center=(WIDTH/2,(HEIGHT/2)+50))
        #draw
        screen.blit(title_text,title_rect)
        screen.blit(prompt_text,prompt_rect)
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()