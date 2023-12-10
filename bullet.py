import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # create object bullet in ship
    def __init__(self, ai_game):
        super().__init__()
        self._screen = ai_game.screen
        self._settings = ai_game.settings
        self._color = self._settings.bullet_color
        #  create rect of bullet in 0,0 and place
        self.rect = pygame.Rect(0, 0, self._settings.bullet_width, self._settings.bullet_height)
        self.rect.midtop = ai_game._ship.rect.midtop
        # save bullet pos
        self.y = float(self.rect.y)

    def update(self):
        # move bullet ot top
        self.y -= self._settings.bullet_speed
        # update rect
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullet
        pygame.draw.rect(self._screen, self._color, self.rect)
