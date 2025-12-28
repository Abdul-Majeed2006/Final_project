import pygame
import os
from .util_params import *

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        # Dictionary mapping logical names to filenames
        sound_map = {
            'shoot_rifle': 'impactMetal_heavy_000.ogg',
            'shoot_shotgun': 'impactPlate_heavy_000.ogg',
            'shoot_mg': 'impactMetal_light_003.ogg',
            'hit_enemy': 'impactSoft_medium_001.ogg',
            'hit_player': 'impactPunch_heavy_000.ogg',
            'pickup_health': 'impactBell_heavy_003.ogg',
            'pickup_weapon': 'impactPlate_light_003.ogg',
            'enemy_death': 'impactGlass_light_001.ogg',
            'game_over': 'impactBell_heavy_000.ogg',
            'explosion': 'impactMining_000.ogg'
        }

        for name, filename in sound_map.items():
            try:
                path = os.path.join(AUDIO_DIR, filename)
                self.sounds[name] = pygame.mixer.Sound(path)
                # Adjust volumes
                if 'shoot' in name:
                    self.sounds[name].set_volume(0.4)
                elif 'pickup' in name:
                    self.sounds[name].set_volume(0.6)
                elif 'hit' in name:
                    self.sounds[name].set_volume(0.5)

            except Exception as e:
                print(f"Warning: Failed to load sound {name} ({filename}): {e}")
                self.sounds[name] = None

    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
