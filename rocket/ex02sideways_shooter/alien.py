import pygame
import random
from pygame.sprite import Sprite
from explosion import Explosion

class	Alien(Sprite):
	def	__init__(self, ai_game):
		super().__init__()
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen_rect
		self.settings = ai_game.settings

		self.image = pygame.image.load('images/alien2.bmp')

		self.rect = self.image.get_rect()

		"""Appears at a random x coordinate"""
		self.rect.x = self.screen_rect.width - self.rect.width - random.randint(0, 50)
		self.rect.y = random.randint(0, self.screen_rect.height - self.rect.height)

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		self.hits_taken = 0

	def	update(self):
		#self.x -= self.settings.alien_speed * self.settings.fleet_direction
		self.y += self.settings.alien_speed * self.settings.fleet_direction
		self.rect.y = self.y

	def	check_edges(self):
		screen_rect = self.screen.get_rect()
		return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
	
	def	take_hit(self):
		self.hits_taken += 1
		if self.hits_taken >= 2:
			explosion = Explosion(5)
			explosion.rect.center = self.rect.center
			self.ai_game.explosions.add(explosion)
			self.kill()
	

