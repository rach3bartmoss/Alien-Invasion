import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Overall class to manage game assets and controls"""

	def	__init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.screen_rect = self.screen.get_rect()
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

	def	_create_alien(self, x_position):
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		self.aliens.add(new_alien)

	def	_create_fleet(self):
		alien = Alien(self)
		alien_width = alien.rect.width
		current_x = alien_width

		while current_x < (self.settings.screen_width - 2 * alien_width):
			self._create_alien(current_x)
			current_x += 2 * alien_width

	def	update_bg_color(self, new_color: tuple):
		if not isinstance(new_color, tuple):
			raise ValueError("error: update_bg_color() -> expects a tuple")
		else:
			self.settings.bg_color = new_color

	def	run_game(self):
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()
			self.clock.tick(60)

	def	_check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def	_check_keydown_events(self, event):
		if event.key == pygame.K_ESCAPE:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True

	def	_check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def	_update_screen(self):
		self.screen.fill(self.settings.bg_color)
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)
		pygame.display.flip()

	def	_fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def	_update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

if __name__ == '__main__':
	"""Run the code above only if the file was run as main script, not imported"""
	ai = AlienInvasion()
	ai.run_game()
