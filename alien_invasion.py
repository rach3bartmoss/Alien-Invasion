import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background
from game_stats import GameStats

class AlienInvasion:
	"""Overall class to manage game assets and controls"""

	def	__init__(self):
		pygame.init()
		self.game_active = True
		self.clock = pygame.time.Clock()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.screen_rect = self.screen.get_rect()
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.background = Background(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.stats = GameStats(self)
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

	def	_create_alien(self, x_position, y_position):
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def	_create_fleet(self):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		current_x, current_y = alien_width, alien_height

		while current_y < (self.settings.screen_height - 3 * alien_height):
			while current_x < (self.settings.screen_width - 2 * alien_width):
				self._create_alien(current_x, current_y)
				current_x += 2 * alien_width
			current_x = alien_width
			current_y += 2 * alien_height

	def	run_game(self):
		while True:
			self._check_events()
			if self.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
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
			self.ship.firing_bullets = True
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
		elif event.key == pygame.K_SPACE:
			self.ship.firing_bullets = False

	def	_update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.background.blitme()
		if self.game_active == False:
			self.background.blitgameover()
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
		self._check_bullet_alien_collisions()
		"""for bullet in self.bullets.copy():
			collided_aliens = pygame.sprite.spritecollide(bullet, self.aliens, False)
			if collided_aliens:
				bullet.kill()  # Remove bullet so it doesn’t produce extra hits
				for alien in collided_aliens:
					alien.take_hit()
		if not self.aliens:
			self.bullets.empty()  # Clear remaining bullets
			self.settings.game_level += 1
			if self.settings.game_level == 1:
				self.settings.alien_speed += 2.0
			else:
				self.settings.alien_speed += 0.5
				self._create_fleet()"""

	def	_check_bullet_alien_collisions(self):
		"""groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict"""
		"""If either dokill argument is True, the colliding Sprites will be removed from their respective Group."""
		collisions = pygame.sprite.groupcollide(self.bullets,
			self.aliens, True, True)
		if not self.aliens:
			self.bullets.empty()
			self.settings.game_level += 1
			if self.settings.game_level == 1:
				self.settings.alien_speed += 2.0
			else:
				self.settings.alien_speed += 0.5
			self._create_fleet()

	def	_update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		self._check_aliens_bottom()

	def	_check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def	_change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def	_ship_hit(self):
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()
			sleep(0.5)
		else:
			self.game_active = False

	def	_check_aliens_bottom(self):
		for alien in self.aliens.sprites():
			if alien.rect.left >= self.settings.screen_height:
				self._ship_hit()
				break


if __name__ == '__main__':
	"""Run the code above only if the file was run as main script, not imported"""
	ai = AlienInvasion()
	ai.run_game()
