import pygame
from nlc_dino_runner.components.dinosaur import Dinosaur
from nlc_dino_runner.components.powerups.power_up_manager import PowerUpManager
from nlc_dino_runner.utils import text_utils
from nlc_dino_runner.components.obstacles.obstaclesManager import ObstaclesManager
from nlc_dino_runner.utils.constants import TITLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS
from nlc_dino_runner.utils.scoreManager import ScoreManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
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
        # self.death_count = 0
        # self.points = 0
        # self.max_points = 0

    def run(self):
        self.playing = True
        self.obstacles_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.score_manager.points)
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
        self.screen.fill((255, 255, 255))
        # self.score() #las imagenes se sobreponen segun el momento de impresion
        self.score_manager.score(self.screen)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
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
