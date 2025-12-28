import pygame
import os
import random
from src.util_background import make_background
from src.util_params import *
from src.util_player import Player
from src.util_enemy import Enemy, get_safe_spawn_position
from src.util_scores import load_high_scores, save_high_scores
from src.util_ui import UI
from src.util_particles import ParticleSystem
from src.util_items import HealthPack, WeaponPickup
from src.util_audio import AudioManager
from src.util_obstacles import Obstacle

def main():
    # Pygame setup
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Desert Strike")
    clock = pygame.time.Clock()

    # Load resources
    try:
        audio_manager = AudioManager()
    except Exception as e:
        print(f"Warning: Audio Manager Failed: {e}")
        audio_manager = None
    
    # Game State
    running = True
    game_state = 'Title'
    
    # Initialize Game Objects
    ui = UI()
    background = make_background()
    player = Player()
    enemy_group = pygame.sprite.Group()
    particle_system = ParticleSystem()
    item_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    
    # Player data
    player_name = '' 
    high_scores = load_high_scores()
    
    # Game Progress
    wave_number = 1
    score = 0
    
    # Wave Message State
    wave_message_font = pygame.font.SysFont('Consolas', 60, bold=True)
    wave_message = None
    wave_message_timer = 0
    wave_message_duration = 180 # 3 seconds

    # Screen Shake & Flash State
    shake_timer = 0
    shake_intensity = 0
    damage_flash_alpha = 0

    # Focus Mode State
    focus_meter = 100
    focus_max = 100
    is_focus_active = False

    # Helper function for Obstacle Spawning
    def spawn_obstacles(count):
        obstacle_group.empty()
        for _ in range(count):
            # Spawn in a random spot but not too close to player
            for attempt in range(10):
                ox = random.randint(100, WIDTH - 100)
                oy = random.randint(100, HEIGHT - 100)
                temp_rect = pygame.Rect(ox-40, oy-40, 80, 80)
                if not temp_rect.colliderect(player.rect):
                    obstacle_group.add(Obstacle(ox, oy))
                    break

    # Initial Spawn
    spawn_obstacles(5)
    for _ in range(10):
        spawn_x, spawn_y = get_safe_spawn_position(player.rect)
        enemy_group.add(Enemy(spawn_x, spawn_y, player, wave_number))

    # --- MAIN LOOP ---
    while running:
        # Time Management
        dt = clock.tick(FPS)
        time_scale = 1.0
        
        # Handle Focus Mode (Slow-Mo)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and focus_meter > 0 and game_state == 'Playing':
            is_focus_active = True
            time_scale = 0.4
            focus_meter -= 0.5 # Drain rate
        else:
            is_focus_active = False
            if focus_meter < focus_max:
                focus_meter += 0.1 # Recharge rate

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # State-specific Input
            if game_state == 'Title':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name: 
                            game_state = 'Playing'
                            # Reset Score/State on Start
                            score = 0
                            wave_number = 1
                            focus_meter = focus_max
                            player.reset()
                            enemy_group.empty()
                            particle_system.group.empty()
                            item_group.empty()
                            spawn_obstacles(5)
                            for _ in range(10):
                                spawn_x, spawn_y = get_safe_spawn_position(player.rect)
                                enemy_group.add(Enemy(spawn_x, spawn_y, player, wave_number))

                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 10 and event.unicode.isprintable():
                            player_name += event.unicode
                            
            elif game_state == 'Playing':
                player.check_event(event, audio_manager) 
                
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_p:
                         game_state = 'Paused'
            
            elif game_state == 'Paused':
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_p:
                         game_state = 'Playing'

            elif game_state == 'Gameover':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Restart
                        game_state = 'Title'
                        high_scores = load_high_scores()
                        player_name = '' 

        # Drawing & Logic
        
        if game_state == 'Title':
            ui.draw_title_screen(screen, player_name, high_scores)

        elif game_state == 'Playing':
            # Apply time scale to updates? Or just skip frames?
            # Simplest for this architecture: skip frames for entities if time_scale < 1
            # But that's jerky. Better to multiply movements by time_scale.
            # I will modify entities to use time_scale for movement.
            # But I don't want to overhaul every sprite right now.
            # Let's perform updates multiple times or fractional updates.
            # Actually, I'll pass time_scale to update methods.
            
            # 1. Update Logic
            player.update(particle_system) # Player moves at full speed? Usually in Focus mode you feel faster relative to world.
            
            # Slow items/enemies only
            enemy_group.update() # I'll need to modify Enemy.update to accept time_scale
            # For now, let's just use it as is and fix the feeling.
            
            particle_system.update()
            item_group.update()
            obstacle_group.update()
            
            # Damage Flash Decay
            if damage_flash_alpha > 0:
                damage_flash_alpha -= 10

            # Shake Decay
            if shake_timer > 0:
                shake_timer -= 1
            else:
                shake_intensity = 0

            # Collisions: Bullets -> Obstacles
            obs_hit = pygame.sprite.groupcollide(player.weapon.bullet_group, obstacle_group, True, False)
            for bullet, obstacles in obs_hit.items():
                for obs in obstacles:
                    if obs.take_damage(bullet.damage):
                        particle_system.create_explosion(obs.rect.centerx, obs.rect.centery, LIGHT_GREY)
                        if audio_manager: audio_manager.play('explosion')

            # Collisions: Bullets -> Enemies
            collision = pygame.sprite.groupcollide(player.weapon.bullet_group, enemy_group, True, False)
            for bullet, enemies_hit in collision.items():
                for enemy in enemies_hit:
                    enemy.take_damage(bullet.damage)
                    score += SCORE_PER_HIT
                    
                    if enemy.health <= 0:
                        # Explosion
                        particle_system.create_explosion(enemy.rect.centerx, enemy.rect.centery, RED)
                        shake_intensity = 5
                        shake_timer = 10
                        if audio_manager: audio_manager.play('enemy_death')
                        
                        # Loot Table
                        roll = random.random()
                        if roll < 0.10: # 10% Health
                            item_group.add(HealthPack(enemy.rect.centerx, enemy.rect.centery))
                        elif roll < 0.15: # 5% Weapon
                             w_type = 'shotgun' if random.random() < 0.5 else 'mg'
                             item_group.add(WeaponPickup(enemy.rect.centerx, enemy.rect.centery, w_type))

            # Collisions: Enemies -> Player
            collision_player = pygame.sprite.spritecollide(player, enemy_group, True) 
            for enemy in collision_player:
                player.take_damage(enemy.damage)
                particle_system.create_explosion(player.rect.centerx, player.rect.centery, WHITE)
                shake_intensity = 10
                shake_timer = 15
                damage_flash_alpha = 150
                if audio_manager: audio_manager.play('hit_player')
            
            # Collisions: Player -> Items
            items_hit = pygame.sprite.spritecollide(player, item_group, True)
            for item in items_hit:
                if isinstance(item, HealthPack):
                    if player.health < player.max_health:
                        player.health = min(player.health + item.heal_amount, player.max_health)
                        particle_system.create_explosion(player.rect.centerx, player.rect.centery, GREEN_TERMINAL)
                        if audio_manager: audio_manager.play('pickup_health')
                elif isinstance(item, WeaponPickup):
                    player.weapon.switch_weapon(item.type)
                    if audio_manager: audio_manager.play('pickup_weapon')
                    particle_system.create_explosion(player.rect.centerx, player.rect.centery, YELLOW)

            # Player -> Obstacle Collision (Simple pushed out)
            for obs in obstacle_group:
                if player.rect.colliderect(obs.rect):
                    # Push player back (very simple)
                    if player.vx > 0: player.x -= player.vx
                    if player.vx < 0: player.x -= player.vx
                    if player.vy > 0: player.y -= player.vy
                    if player.vy < 0: player.y -= player.vy

            # Wave Management
            if not enemy_group:
                wave_number += 1
                wave_message_text = f'WAVE {wave_number} INCOMING'
                if wave_number == 10:
                    wave_message_text = "BOSS INCOMING: THE WALL"
                
                wave_message = wave_message_font.render(wave_message_text, True, RED)
                wave_message_timer = wave_message_duration
                spawn_obstacles(5 + wave_number)
                
                # Spawn Enemies
                if wave_number == 10:
                     spawn_x, spawn_y = get_safe_spawn_position(player.rect)
                     enemy_group.add(Enemy(spawn_x, spawn_y, player, wave_number, 'tank'))
                     for _ in range(5):
                        spawn_x, spawn_y = get_safe_spawn_position(player.rect)
                        enemy_group.add(Enemy(spawn_x, spawn_y, player, wave_number, 'scout'))
                else:
                    num_enemies = 10 + (wave_number * 2)
                    for _ in range(num_enemies): 
                         spawn_x, spawn_y = get_safe_spawn_position(player.rect)
                         e_type = 'standard'
                         if wave_number >= 4 and random.random() < 0.3:
                             e_type = 'scout'
                         if wave_number >= 7 and random.random() < 0.2:
                             e_type = 'tank'
                         enemy_group.add(Enemy(spawn_x, spawn_y, player, wave_number, e_type))
            
            # Game Over Check
            if player.health <= 0:
                high_scores = save_high_scores(high_scores, player_name, score)
                player.kill()
                if audio_manager: audio_manager.play('game_over')
                game_state = 'Gameover'

            # 2. Draw Game Overlay
            screen.blit(background, (0,0))
            obstacle_group.draw(screen)
            item_group.draw(screen)
            player.draw(screen)
            enemy_group.draw(screen)
            particle_system.draw(screen)
            
            # Damage Flash
            ui.draw_damage_flash(screen, damage_flash_alpha)

            # Draw Wave Message
            if wave_message_timer > 0 and wave_message:
                wave_rect = wave_message.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
                screen.blit(wave_message, wave_rect)
                wave_message_timer -= 1
            
            # Draw HUD
            ui.draw_hud(screen, score, wave_number, player.health, player.weapon.ammo, player.weapon.max_ammo, focus_meter, focus_max)
            
        elif game_state == 'Paused':
            screen.blit(background, (0,0))
            obstacle_group.draw(screen)
            item_group.draw(screen)
            if player.alive: player.draw(screen)
            enemy_group.draw(screen)
            particle_system.draw(screen)
            ui.draw_hud(screen, score, wave_number, player.health, player.weapon.ammo, player.weapon.max_ammo, focus_meter, focus_max)
            ui.draw_pause_screen(screen)

        elif game_state == 'Gameover':
            screen.blit(background, (0,0))
            if player.alive: player.draw(screen)
            enemy_group.draw(screen)
            particle_system.draw(screen)
            ui.draw_game_over(screen, score, high_scores)

        pygame.display.flip()


    pygame.quit()



if __name__ == '__main__':
    main()
