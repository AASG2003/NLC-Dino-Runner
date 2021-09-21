from nlc_dino_runner.components.obstacles.obstacles import Obstacles


class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 240
        self.step_index = 0

    def update(self, game_speed, obstacles_list):
        if self.step_index >= 10:
            self.step_index = 0
        self.run()
        super().update(game_speed, obstacles_list)

    def run(self):
        self.obstacle_type = self.step_index // 5
        last_x = self.rect.x
        last_y = self.rect.y
        self.rect = self.image[self.obstacle_type].get_rect()
        self.rect.x = last_x
        self.rect.y = last_y
        self.step_index += 1
