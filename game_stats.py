import json


class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_activ = False
        with open('high_score.json') as f:
            self.high_score = json.load(f)

    def reset_stats(self):
        self.candle_left = self.settings.candle_limit
        self.score = 0
        self.level = 1

