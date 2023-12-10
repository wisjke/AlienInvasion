import pygame


class Ship(object):

    def __init__(self, ai_game):
        # init ship and his pos
        self._screen = ai_game.screen
        self._settings = ai_game.settings
        self._screen_rect = ai_game.screen.get_rect()

        # set new ship in mid of screen
        self._image = pygame.image.load('images/ship.png')
        self.rect = self._image.get_rect()
        self.rect.midbottom = self._screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        # save float of pos of ship
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self._screen_rect.right:
            self.x += self._settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self._settings.ship_speed

        # update rect
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self._screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self._screen.blit(self._image, self.rect)

