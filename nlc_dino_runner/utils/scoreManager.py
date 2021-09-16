from nlc_dino_runner.utils import text_utils
from nlc_dino_runner.utils.constants import ICON, SCREEN_WIDTH, SCREEN_HEIGHT


class ScoreManager:
    def __init__(self):
        self.death_count = 0
        self.points = 0
        self.last_score = 0
        self.max_points = 0

    def update_points(self):
        self.points += 1

    def update_at_the_end(self):
        self.last_score = self.points
        self.max_points = max(self.max_points, self.points)
        self.points = 0

    def restart_points(self):
        self.points = 0

    def draw_points(self, screen):
        half_screen_height = SCREEN_HEIGHT // 2
        death_score, death_score_rect = text_utils.get_centered_message("Death count: " + str(self.death_count),
                                                                        height=half_screen_height + 50)
        screen.blit(death_score, death_score_rect)
        screen.blit(ICON, ((SCREEN_WIDTH // 2) - 40, half_screen_height - 150))
        max_points, max_points_rect = text_utils.get_centered_message("Max Points: " + str(self.max_points),
                                                                      height=half_screen_height + 100)
        screen.blit(max_points, max_points_rect)
        last_score, last_score_rect = text_utils.get_centered_message("Last Score: " + str(self.last_score),
                                                                      height=half_screen_height + 150)
        screen.blit(last_score, last_score_rect)

    def score(self, screen):
        self.points += 1
        score_element, score_element_rect = text_utils.get_score_element(self.points)
        screen.blit(score_element, score_element_rect)

    def new_game_speed(self, game):
        if self.points % 100 == 0:
            game.game_speed += 1
