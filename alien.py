import pygame
import random
from pygame.sprite import Sprite

class	Alien(Sprite):
	def	__init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen_rect
		self.settings = ai_game.settings

		self.image = pygame.image.load('images/alien2.bmp')
		self.image = pygame.transform.rotate(self.image, -90)

		self.rect = self.image.get_rect()

		"""Appears at a random x coordinate"""
		self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)

	def	update(self):
		self.x += self.settings.alien_speed * self.settings.fleet_direction
		self.rect.x = self.x

	def	check_edges(self):
		screen_rect = self.screen.get_rect()
		return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
