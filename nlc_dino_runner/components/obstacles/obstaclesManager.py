import pygame.time
import random

from nlc_dino_runner.components.obstacles.bird import Bird
from nlc_dino_runner.components.obstacles.cactus import Cactus
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


def select_cactus():
    cactus_list = [LARGE_CACTUS, SMALL_CACTUS]
    return random.choice(cactus_list)


def random_obstacle():
    new_cactus = Cactus(select_cactus())
    new_bird = Bird(BIRD)
    random_obstacles = [new_cactus, new_bird]
    return random.choice(random_obstacles)


class ObstaclesManager:

    def __init__(self):
        self.obstacles_list = []

    def update(self, game):
        if len(self.obstacles_list) == 0:
            self.obstacles_list.append(random_obstacle())

        for obstacle in self.obstacles_list:
            obstacle.update(game.game_speed, self.obstacles_list)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                    self.obstacles_list.remove(obstacle)
                else:
                    pygame.time.delay(500)
                    game.playing = False
                    game.score_manager.death_count += 1
                    break

    def draw(self, screen):
        for obstacle in self.obstacles_list:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles_list = []
