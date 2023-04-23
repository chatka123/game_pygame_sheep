
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/bullet.bmp')
        self.image = pygame.transform.scale(self.image, (32, 16))
        self.rect = self.image.get_rect()
        self.rect.midbottom = ai_game.candle.rect.center
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
