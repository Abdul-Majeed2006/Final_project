import pygame

class Sight(pygame.sprite.Sprite):
    def __init__(self, sight):
        pygame.sprite.Sprite.__init__(self) 
        self.sight = sight
        #load t#he image
        self.sight = pygame.image.load(sight)
        self.sight = pygame.transform.rotozoom(self.sight, 0, 3) 

        self.rect = self.sight.get_rect()

    def update(self):
        #sight position = mouse position
        self.rect.center = pygame.mouse.get_pos()

    def draw(self,screen):
        screen.blit(self.sight,self.rect)
        
