import pygame
import src.utils as utils
from math import ceil


class Tutorial:
    def __init__(self, player, game):
        self.game = game
        # self.load_images()
        self.starting_position = (0, 0)
        self.state_num = 0
        self.white = (255, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(self.player2.speech.message, True, self.white)
        self.textRect = self.text.get_rect()
        self.textRect.center = (805, 60)

    def load_images(self):
        self.block = pygame.image.load(f'{self.path}/block.png').convert_alpha()
        self.end = pygame.image.load(f'{self.path}/end.png').convert_alpha()
        self.start = pygame.image.load(f'{self.path}/start.png').convert_alpha()

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.J]:
            state_num = state_num + 1
        if pressed[pygame.K] and (state_num > 0):
            state_num = state_num - 1

        if(state_num == 0):
            self.text = "Hi"
        if(state_num == 1):
             self.text = "Get weapon"

    def draw(self):
            self.game.screen.blit(self.text, self.textRect)
