import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self._screen = ai_game.screen
        self.settings = ai_game.settings

        # load image and set rect
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()

        # start each alien in top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # save pos
        self.x = float(self.rect.x)

    def check_edges(self):
        # returns true if alien is on border
        screen_rect = self._screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
