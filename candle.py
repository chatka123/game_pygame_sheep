import pygame
from pygame.sprite import Sprite


class Candle(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/candle_down.bmp')
        self.image = pygame.transform.scale(self.image, (120, 80))
        self.image_up = pygame.image.load('images/candle_up.bmp')
        self.image_up = pygame.transform.scale(self.image_up, (120, 80))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.candle_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.candle_speed_factor

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def blitme_up(self):
        self.screen.blit(self.image_up, self.rect)

    def center_candle(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)



