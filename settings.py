class Settings(object):

    def __init__(self):
        # default settings
        # screen settings

        self._screen_width = 1280
        self._screen_height = 960
        self._bg_color = (10, 0, 26)

        # ship settings
        self._ship_speed = 2
        self.ship_limit = 2
        # bullet settings
        self._bullet_speed = 1.0
        self._bullet_width = 3
        self._bullet_height = 20
        self._bullet_color = (255, 0, 0)
        self._bullets_allowed = 5
        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction 1 - right -1 - left
        self.fleet_direction = 1

        # variable setting
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

    @property
    def screen_width(self):
        return self._screen_width

    @property
    def screen_height(self):
        return self._screen_height

    @property
    def bg_color(self):
        return self._bg_color

    @property
    def ship_speed(self):
        return self._ship_speed

    @ship_speed.setter
    def ship_speed(self, value):
        self._ship_speed = value

    @property
    def bullet_speed(self):
        return self._bullet_speed

    @property
    def bullet_width(self):
        return self._bullet_width

    @property
    def bullet_height(self):
        return self._bullet_height

    @property
    def bullet_color(self):
        return self._bullet_color

    @property
    def bullets_allowed(self):
        return self._bullets_allowed

    @bullet_speed.setter
    def bullet_speed(self, value):
        self._bullet_speed = value
