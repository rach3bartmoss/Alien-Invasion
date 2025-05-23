import pygame
import sys
from pygame.sprite import Sprite
import random

class Rain(Sprite):
	def	__init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen_rect

		self.image = pygame.image.load('../images/raindrops.bmp')
		self.image = pygame.transform.rotate(self.image, -22)
		self.rect = self.image.get_rect()

		self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)
		self.raindrop_speed = 10

	def	update(self):
		self.x += self.raindrop_speed * 0
		self.rect.x = self.x
