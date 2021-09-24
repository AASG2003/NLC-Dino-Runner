import pygame.time
import random

from nlc_dino_runner.components.obstacles.bird import Bird
from nlc_dino_runner.components.obstacles.cactus import Cactus
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, DINO_DEAD


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
            if game.power_up_manager.hammer.rect.colliderect(obstacle.rect):
                if obstacle in self.obstacles_list:
                    self.obstacles_list.remove(obstacle)

            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                    self.obstacles_list.remove(obstacle)
                elif game.life_manager.life_counter() == 1:
                    game.playing = False
                    game.player.image = DINO_DEAD
                    game.score_manager.death_count += 1
                    game.life_manager.delete_life()
                    game.death()
                    game.power_up_manager.hammer.hammers_left = 0
                    pygame.time.delay(500)
                    break
                else:
                    game.life_manager.delete_life()
                    if obstacle in self.obstacles_list:
                        self.obstacles_list.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles_list:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles_list = []
