import sys
import pygame
from settings import Settings
from candle import Candle
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from alien_score import AlienScore
import json


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings = Settings(self)
        self.stats = GameStats(self)
        self.candle = Candle(self)
        pygame.display.set_caption('Sheep')
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.sb = Scoreboard(self)
        self.aliens_score = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'play')
        self.time_animating = 0
        self.aliens_score_time_animating = 0

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_activ:
                self.candle.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.candle.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.candle.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_activ:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN and not self.stats.game_activ:
            self._start_playing()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.candle.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.candle.moving_left = False

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('high_score.json', 'w') as f:
                    json.dump(self.stats.high_score, f)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_activ:
            self._start_playing()

    def _start_playing(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_activ = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_bullets()
        self.sb.prep_candles()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.candle.center_candle()
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.time_animating = self.settings.animating
            self.sb.prep_bullets()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                self.sb.prep_bullets()
        self._check_bullet_aliens_collisions()

    def _check_bullet_aliens_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            self.sb.prep_bullets()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    point = alien.rect.center
                    alien_score = AlienScore(self, point)
                    self.aliens_score.add(alien_score)
                    self.aliens_score_time_animating = self.settings.alien_score_time_animating
            self.sb.prep_score()
            self.sb.check_high_score()

    def _alien_score_show(self):
        if self.aliens_score_time_animating:
            for alien_score in self.aliens_score.sprites():
                alien_score.draw_alien_score()
            self.aliens_score_time_animating -= 1
        else:
            self.aliens_score .empty()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _candle_hit(self):
        if self.stats.candle_left > 0:
            self.stats.candle_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.candle.center_candle()
            self.sb.prep_candles()
            sleep(0.5)
        else:
            self.stats.game_activ = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.candle, self.aliens):
            self._candle_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._candle_hit()
                break

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        candle_height = self.candle.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - candle_height
        number_rows = available_space_y // (2 * alien_height)
        number_aliens_x = available_space_x // (2 * alien_width)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _animating_candle(self):
        if self.time_animating:
            self.candle.blitme_up()
            self.time_animating -= 1
        else:
            self.candle.blitme()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._animating_candle()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self._alien_score_show()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_activ:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
