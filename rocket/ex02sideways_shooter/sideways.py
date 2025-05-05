import pygame
import sys
from time import sleep
from settings import Settings
from ship_side import Ship
from buttet import Bullet
from background import Background
from alien import Alien
from game_stats import GameStats
from explosion import Explosion

class Sideways:
	def	__init__(self):
		pygame.init()
		self.game_active = True

		self.settings = Settings()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1200, 800))
		self.screen_rect = self.screen.get_rect()
		pygame.display.set_caption("Sideways Shooters")
	
		self.background = Background(self)
		self.bullets = pygame.sprite.Group()
		self.ship = Ship(self)
		self.aliens = pygame.sprite.Group()
		self.stats = GameStats(self)
		self.explosions = pygame.sprite.Group()

		self._create_fleet()

	def	run_game(self):
		while True:
			self._check_events()
			if self.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
				self.explosions.update()
			self._update_screen()
			self.clock.tick(60)

	def	_update_screen(self):
		self.background.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)
		self.explosions.draw(self.screen)
		if self.game_active == False:
			self.background.blitgameover()
		pygame.display.flip()

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
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True

	def	_check_keyup_events(self, event):
		if event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def	_fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def	_update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.left >= self.screen_rect.right:
				self.bullets.remove(bullet)
		#self._check_bullet_alien_collisions()
	
		"""
		To target a individual sprite use spritecollide()
			it takes a single sprite(bullet) and detects this target within a group(self.aliens)
			you can set False or True to eliminate right the way, is not our intent here
			the spritecollide() will return a list of the group elements that were hit
			then we call the take_hit directly over the element

		Here the .kill() method is quite useful to eliminate the target sprite from its group
		"""
		for bullet in self.bullets.copy():
			collided_aliens = pygame.sprite.spritecollide(bullet, self.aliens, False)
			if collided_aliens:
				bullet.kill()
				for alien in collided_aliens:
					alien.take_hit()

		if not self.aliens:
			self.bullets.empty()
			self.settings.game_level += 1
			if self.settings.game_level == 1:
				self.settings.alien_speed += 2.0
			else:
				self.settings.alien_speed += 0.5
				self._create_fleet()
	
	def	_check_bullet_alien_collisions(self):
		collisions = pygame.sprite.groupcollide(self.bullets,
										self.aliens, True, True)
		if not self.aliens:
			self.bullets.empty()
			self.settings.number_of_aliens += 10
			self._create_fleet()
			print(self.settings.number_of_aliens)

	def	_create_alien(self, x_position, y_position):
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def _create_fleet(self):
		for _ in range(self.settings.number_of_aliens):
			self.aliens.add(Alien(self))


	"""def	_create_fleet(self):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		gap_y = alien_height + 15

		current_x = self.settings.screen_width - alien_width
		current_y = alien_height

		while current_x > (3 * alien_width):
			while current_y < (self.settings.screen_height - 2 * alien_height):
				self._create_alien(current_x, current_y)
				current_y += gap_y
			current_y = alien_height
			current_x -= 2 * alien_width"""


	def	_update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		self._check_aliens_left()

	def	_check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.rect.top <= 0 or alien.rect.bottom >= self.settings.screen_height:
				self._change_fleet_direction()
				break
	
	def	_change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.x -= self.settings.fleet_drop_speed
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

	def	_check_aliens_left(self):
		for alien in self.aliens.sprites():
			if alien.rect.width <= 0:
				self._ship_hit()
				break

if __name__ == '__main__':
	ss = Sideways()
	ss.run_game()
