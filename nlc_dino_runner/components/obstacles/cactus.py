from nlc_dino_runner.components.obstacles.obstacles import Obstacles
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
import random


class Cactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 305
