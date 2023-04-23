import pygame.font
from pygame.sprite import Group
from candle import Candle
from bullet import Bullet


class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_candles()
        self.prep_bullets()

    def prep_score(self):
        rounded_score = round(self.stats.score, 1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, 1)
        high_score_str = 'Best: ' + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        level_str = 'lvl ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_candles(self):
        self.candles = Group()
        for candle_number in range(self.stats.candle_left):
            candle = Candle(self.ai_game)
            candle.rect.x = 10 + candle.rect.width * 1.1 * candle_number
            candle.rect.y = 10
            self.candles.add(candle)

    def prep_bullets(self):
        self.available_bullets = Group()
        available_bullets = self.settings.bullet_allowed - len(self.ai_game.bullets)
        for bullet_number in range(available_bullets):
            bullet = Bullet(self.ai_game)
            bullet.rect.bottomright = self.screen_rect.bottomright
            bullet.rect.x -= bullet.rect.width * 1.1 * bullet_number
            self.available_bullets.add(bullet)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.candles.draw(self.screen)
        self.available_bullets.draw(self.screen)




