import pygame
from .util_params import *

class UI:
    def __init__(self):
        self.title_font = pygame.font.SysFont('Consolas', 80, bold=True)
        self.header_font = pygame.font.SysFont('Consolas', 48)
        self.body_font = pygame.font.SysFont('Consolas', 24)
        self.small_font = pygame.font.SysFont('Consolas', 18)
        
    def draw_text(self, surface, text, font, color, center_pos):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center_pos)
        surface.blit(text_surf, text_rect)
        return text_rect

    def draw_title_screen(self, screen, player_name, high_scores):
        # 1. Background
        screen.fill(DARK_GREY)
        
        # 2. Border
        pygame.draw.rect(screen, GREEN_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        
        # 3. Title
        self.draw_text(screen, "DESERT STRIKE", self.title_font, GREEN_TERMINAL, (WIDTH/2, 100))
        self.draw_text(screen, "[ SYSTEM READY ]", self.small_font, GREEN_TERMINAL, (WIDTH/2, 160))

        # 4. Input Box
        input_box_rect = pygame.Rect(0, 0, 400, 60)
        input_box_rect.center = (WIDTH/2, HEIGHT/2 - 50)
        pygame.draw.rect(screen, BLACK, input_box_rect)
        pygame.draw.rect(screen, GREEN_TERMINAL, input_box_rect, 2)
        
        # Player Name
        name_surf = self.header_font.render(player_name, True, WHITE)
        name_rect = name_surf.get_rect(center=input_box_rect.center)
        screen.blit(name_surf, name_rect)
        
        # Cursor
        if pygame.time.get_ticks() % 1000 < 500:
             cursor_rect = pygame.Rect(name_rect.right + 2, name_rect.top + 5, 2, name_rect.height - 10)
             pygame.draw.rect(screen, GREEN_TERMINAL, cursor_rect)

        # Instructions
        self.draw_text(screen, "ENTER IDENTITY TO INITIALIZE", self.body_font, LIGHT_GREY, (WIDTH/2, HEIGHT/2 + 20))
        self.draw_text(screen, "PRESS <ENTER> TO DEPLOY", self.body_font, GREEN_TERMINAL, (WIDTH/2, HEIGHT/2 + 60))

        # 5. High Scores (Panel)
        panel_y = HEIGHT - 250
        self.draw_text(screen, "TOP OPERATORS", self.body_font, YELLOW, (WIDTH/2, panel_y))
        
        y_offset = panel_y + 40
        for i, entry in enumerate(high_scores):
            score_str = f"{i+1}. {entry['name']:<10} {entry['score']:>6}"
            self.draw_text(screen, score_str, self.body_font, WHITE, (WIDTH/2, y_offset))
            y_offset += 30

    def draw_hud(self, screen, score, wave, health, ammo, max_ammo, focus=100, focus_max=100):
        # Top Bar
        pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, 50))
        pygame.draw.line(screen, GREEN_TERMINAL, (0, 50), (WIDTH, 50), 2)
        
        # Score
        score_surf = self.header_font.render(f"SCORE: {score}", True, GREEN_TERMINAL)
        screen.blit(score_surf, (20, 5))
        
        # Wave
        wave_surf = self.header_font.render(f"WAVE: {wave}", True, RED)
        wave_rect = wave_surf.get_rect(center=(WIDTH/2, 25))
        screen.blit(wave_surf, wave_rect)

        # Health Bar (Top Right)
        health_width = 200
        pygame.draw.rect(screen, RED, (WIDTH - 220, 10, health_width, 30)) # Back
        current_health_width = int((health / 100) * health_width)
        pygame.draw.rect(screen, GREEN_TERMINAL, (WIDTH - 220, 10, current_health_width, 30)) # Front
        pygame.draw.rect(screen, WHITE, (WIDTH - 220, 10, health_width, 30), 2) # Border

        # Ammo (Bottom Right)
        ammo_color = WHITE if ammo > 5 else RED
        ammo_text = f"AMMO: {ammo}/{max_ammo}"
        if ammo == 0: ammo_text = "RELOADING..."
        ammo_surf = self.body_font.render(ammo_text, True, ammo_color)
        screen.blit(ammo_surf, (WIDTH - 200, HEIGHT - 40))

        # Bottom Center: Focus Meter
        focus_pct = max(0, min(1, focus / focus_max))
        focus_color = (0, 191, 255) # Deep Sky Blue
        pygame.draw.rect(screen, DARK_GREY, (WIDTH/2 - 100, HEIGHT - 50, 200, 10))
        pygame.draw.rect(screen, focus_color, (WIDTH/2 - 100, HEIGHT - 50, 200 * focus_pct, 10))
        self.draw_text(screen, "FOCUS", self.body_font, focus_color, (WIDTH/2, HEIGHT - 65))

    def draw_damage_flash(self, screen, alpha):
        if alpha > 0:
            flash_surface = pygame.Surface((WIDTH, HEIGHT))
            flash_surface.fill(RED)
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0,0))

    def draw_game_over(self, screen, score, high_scores):
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200) # Transparent
        screen.blit(overlay, (0,0))
        
        # Text
        self.draw_text(screen, "MISSION FAILED", self.title_font, RED, (WIDTH/2, 150))
        self.draw_text(screen, f"FINAL SCORE: {score}", self.header_font, WHITE, (WIDTH/2, 250))
        
        self.draw_text(screen, "PRESS [R] TO RETRY", self.body_font, GREEN_TERMINAL, (WIDTH/2, HEIGHT - 100))

        # High Scores
        y_offset = 350
        self.draw_text(screen, "LEADERBOARD", self.body_font, YELLOW, (WIDTH/2, y_offset))
        y_offset += 40
        for i, entry in enumerate(high_scores):
            color = GREEN_TERMINAL if i == 0 else WHITE
            score_str = f"{i+1}. {entry['name']:<10} {entry['score']:>6}"
            self.draw_text(screen, score_str, self.body_font, color, (WIDTH/2, y_offset))
            y_offset += 30

    def draw_pause_screen(self, screen):
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150) # Semi-transparent
        screen.blit(overlay, (0,0))
        
        # Text
        self.draw_text(screen, "SYSTEM PAUSED", self.title_font, YELLOW, (WIDTH/2, HEIGHT/2 - 50))
        self.draw_text(screen, "PRESS [P] TO RESUME", self.body_font, WHITE, (WIDTH/2, HEIGHT/2 + 50))

