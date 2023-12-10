import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion(object):
    """class which control the game"""

    def __init__(self):
        """init the game"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self._ship = Ship(self)
        self._bullets = pygame.sprite.Group()
        self._aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """start main module of the game"""

        while True:
            self._check_events()
            if self.stats.game_active:
                self._ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self._ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self._ship.moving_left = True
        elif event.key == pygame.K_UP:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self._ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self._ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            self._aliens.empty()
            self._bullets.empty()

            self._create_fleet()
            self._ship.center_ship()

    def _start_game(self):
        if not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self._aliens.empty()
            self._bullets.empty()

            self._create_fleet()
            self._ship.center_ship()

    def _fire_bullet(self) -> None:
        if len(self._bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self._bullets.add(new_bullet)

    def _update_bullets(self):
        self._bullets.update()
        # remove old bullets
        for bullet in self._bullets:
            if bullet.rect.bottom <= 0:
                self._bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check if alien hit
        collisions = pygame.sprite.groupcollide(self._bullets, self._aliens, True, True)
        if not self._aliens:
            self._bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

        self.sb.prep_score()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self._aliens.empty()
            self._bullets.empty()

            self._create_fleet()
            self._ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False

    def _check_aliens_botoom(self):
        screen_rect = self.screen.get_rect()
        for alien in self._aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _create_fleet(self) -> None:
        # create fleet of aliens
        # find out count of aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # find out how much we can place
        ship_height = self._ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2* alien_height)
        # create 1st wave of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create alien and place it into wave
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self._aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self._aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self._aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self._aliens.update()
        # find alien-ship contact
        if pygame.sprite.spritecollideany(self._ship, self._aliens):
            self._ship_hit()
        self._check_aliens_botoom()

    def _update_screen(self):
        # draw screen on new iteration
        self.screen.fill(self.settings.bg_color)
        self._ship.blitme()
        for bullet in self._bullets.sprites():
            bullet.draw_bullet()
        self._aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        # show last display
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
