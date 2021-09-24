import pygame
import random
from nlc_dino_runner.components.dinosaur import Dinosaur
from nlc_dino_runner.components.life.life_manager import LifeManager
from nlc_dino_runner.components.powerups.power_up_manager import PowerUpManager
from nlc_dino_runner.utils import text_utils
from nlc_dino_runner.components.obstacles.obstaclesManager import ObstaclesManager
from nlc_dino_runner.utils.constants import TITLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, GAME_OVER, DARK_MODE, \
    NORMAL_MODE, CLOUD
from nlc_dino_runner.utils.scoreManager import ScoreManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.separation = random.randint(350, 450)
        self.x_pos_cloud1 = 0 + self.separation
        self.x_pos_cloud2 = 0 + self.separation * 2
        self.x_pos_cloud3 = 0 + self.separation * 3
        self.x_pos_cloud4 = 0 + self.separation * 4
        self.y_pos_cloud1 = random.randint(100, 250)
        self.y_pos_cloud2 = random.randint(100, 250)
        self.y_pos_cloud3 = random.randint(100, 250)
        self.y_pos_cloud4 = random.randint(100, 250)
        self.separation = 250
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.playing = False
        self.x_pos_bg = 0
        self.y_pos_bg = 360
        self.game_speed = 20
        self.player = Dinosaur()
        self.obstacles_manager = ObstaclesManager()
        self.running = True
        self.score_manager = ScoreManager()
        self.power_up_manager = PowerUpManager()
        self.life_manager = LifeManager()
        # self.death_count = 0
        # self.points = 0
        # self.max_points = 0

    def run(self):
        self.playing = True
        self.obstacles_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.score_manager.points, self.player)
        self.game_speed = 20
        self.life_manager.refull_lives()
        while self.playing:
            self.event()
            self.update()
            self.draw()
        self.score_manager.update_at_the_end()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacles_manager.update(self)
        self.power_up_manager.update(self.score_manager.points, self.game_speed, self.player)
        self.score_manager.update_points()
        self.score_manager.new_game_speed(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(NORMAL_MODE)
        # self.score() #las imagenes se sobreponen segun el momento de impresion
        self.score_manager.score(self.screen, self.player)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.life_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    # def score(self):
    #     self.points += 1
    #     if self.points % 100 == 0:
    #         self.game_speed += 1
    #     score_element, score_element_rect = text_utils.get_score_element(self.points)
    #     self.screen.blit(score_element, score_element_rect)

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))

        self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        self.draw_clouds()

    def draw_clouds(self):  # drawing the clouds
        self.screen.blit(CLOUD, (self.x_pos_cloud1, self.y_pos_cloud1))
        self.screen.blit(CLOUD, (self.x_pos_cloud2, self.y_pos_cloud2))
        self.screen.blit(CLOUD, (self.x_pos_cloud3, self.y_pos_cloud3))
        self.screen.blit(CLOUD, (self.x_pos_cloud4, self.y_pos_cloud4))
        self.x_pos_cloud1 -= self.game_speed // 2
        self.x_pos_cloud2 -= self.game_speed // 2
        self.x_pos_cloud3 -= self.game_speed // 2
        self.x_pos_cloud4 -= self.game_speed // 2
        if self.x_pos_cloud1 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud1 = SCREEN_WIDTH
            self.y_pos_cloud1 = random.randint(100, 250)
        if self.x_pos_cloud2 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud2 = SCREEN_WIDTH
            self.y_pos_cloud2 = random.randint(100, 250)
        if self.x_pos_cloud3 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud3 = SCREEN_WIDTH
            self.y_pos_cloud3 = random.randint(100, 250)
        if self.x_pos_cloud4 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud4 = SCREEN_WIDTH
            self.y_pos_cloud4 = random.randint(100, 250)

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        # mostrar el menu
        self.print_menu_elements()

        pygame.display.update()

        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.player = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        self.screen.blit(ICON, ((SCREEN_WIDTH // 2) - 40, half_screen_height - 150))
        if self.score_manager.death_count == 0:
            self.first_menu()
        else:
            self.second_menu()

    def first_menu(self):
        text, text_rect = text_utils.get_centered_message("Press any Key to Start")
        self.screen.blit(text, text_rect)

    def second_menu(self):
        text, text_rect = text_utils.get_centered_message("Press any Key to ReStart")
        self.screen.blit(text, text_rect)
        self.score_manager.draw_points(self.screen)

    def death(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.score_manager.score(self.screen, self.player)
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.life_manager.draw(self.screen)
        self.game_over()
        pygame.display.update()
        pygame.display.flip()

    def game_over(self):
        self.screen.blit(GAME_OVER, ((SCREEN_WIDTH // 2) - 180, (SCREEN_HEIGHT // 2) - 180))
