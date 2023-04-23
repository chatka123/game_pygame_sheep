import pygame
from pygame.sprite import Sprite
import pygame.font


class AlienScore(Sprite):

    def __init__(self, ai_game, point):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.SysFont(None, 30)
        text = f'+{ai_game.settings.alien_points}'
        self.text_color = (1, 2, 3)
        self.image = self.font.render(text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = point

    def draw_alien_score(self):
        self.screen.blit(self.image, self.rect)


