class Settings:
    def __init__(self, ai_game):
        self.screen_width = ai_game.screen.get_rect().width
        self.screen_height = ai_game.screen.get_rect().height
        self.bg_color = (2, 230, 230)
        self.candle_limit = 3
        self.bullet_allowed = 3
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()
        self.animating = 50
        self.alien_score_time_animating = 100

    def initialize_dynamic_settings(self):
        self.candle_speed_factor = 1.0
        self.bullet_speed_factor = 1.0
        self.alien_speed_factor = 1.5
        self.fleet_direction = 1
        self.alien_points = 1

    def increase_speed(self):
        self.candle_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= 2

