import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

"""PAGE 299 CRASH COURSE BUTTON FOR MORE UPGRADES"""

class AlienInvasion:
	"""Overall class to manage game assets and controls"""

	def	__init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		self.game_active = False
		self.game_over = False
		self.retries = 0

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.screen_rect = self.screen.get_rect()
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.background = Background(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.aliens = pygame.sprite.Group()

		self.play_button = Button(self, "Play")
		self.play_active = True
		self.easy_button = Button(self, "Easy")
		self.normal_button = Button(self, "Normal")
		self.hard_button = Button(self, "Hard")

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
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def	_check_keydown_events(self, event):
		if event.key == pygame.K_ESCAPE:
			sys.exit()
		elif event.key == pygame.K_p:
			self._start_game()
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
		if self.game_over == True:
			self.background.blitgameover()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)
		self.sb.show_score()
		if not self.game_active:
			if self.play_active == True:
				self.play_button.draw_button()
			else:
				self.easy_button.rect.center = (400, 540)
				self.hard_button.rect.center = (1400, 540)
				self.easy_button.msg_image_rect.center = self.easy_button.rect.center
				self.hard_button.msg_image_rect.center = self.hard_button.rect.center

				#self.easy_button.msg_image_rect.center = self.easy_button.rect.bottomleft
				#self.hard_button.msg_image_rect.center = self.hard_button.rect.bottomright
				self.easy_button.draw_button()
				self.normal_button.draw_button()
				self.hard_button.draw_button()
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
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
		if not self.aliens:
			self.bullets.empty()
			self.settings.game_level += 1
			self.settings.ship_speed += 0.5
			if self.settings.game_level == 1:
				self.settings.alien_speed += 1.0
			elif self.settings.game_level == 5:
				self.settings.alien_points = 100
			print(self.settings.ship_speed)
			print(self.settings.game_level)
			print(self.settings.alien_points)

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
		elif self.stats.ships_left == 0:
			print("ENTERED HERE2")
			self.retries += 1
			pygame.mouse.set_visible(True)
			self.game_active = False
			self.game_over = True

	def	_check_aliens_bottom(self):
		for alien in self.aliens.sprites():
			if alien.rect.left >= self.settings.screen_height:
				#self._ship_hit()
				break

	def	_check_play_button(self, mouse_pos):
		if self.play_active == False:
			diff_selected1 = self.easy_button.rect.collidepoint(mouse_pos)
			diff_selected2 = self.normal_button.rect.collidepoint(mouse_pos)
			diff_selected3 = self.hard_button.rect.collidepoint(mouse_pos)
			if diff_selected1 and not self.game_active:
				self._start_game('easy')
			elif diff_selected2 and not self.game_active:
				self._start_game('normal')
			elif diff_selected3 and not self.game_active:
				self._start_game('hard')
		else:
			button_clicked = self.play_button.rect.collidepoint(mouse_pos)
			if button_clicked and not self.game_active:
				self.play_active = False


	def	_start_game(self, lvl='easy'):
		if lvl == 'easy':
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.game_active = True
			self.game_over = False
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()
		elif lvl == 'normal' :
			if self.retries == 0:
				self.settings.alien_speed += 1.0
			else:
				self.settings.alien_speed = 3.0
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.game_active = True
			self.game_over = False
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()
		elif lvl == 'hard':
			if self.retries == 0:
				self.settings.alien_speed += 2.0
			else:
				self.settings.alien_speed = 4.0
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.game_active = True
			self.game_over = False
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()
		else:
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.game_active = True
			self.game_over = False
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()


if __name__ == '__main__':
	"""Run the code above only if the file was run as main script, not imported"""
	ai = AlienInvasion()
	ai.run_game()
