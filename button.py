import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/play.bmp')
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.text_color = (2, 55, 25)
        self.font = pygame.font.SysFont(None, 48)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)