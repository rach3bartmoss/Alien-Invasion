import pygame

class Background:
	def	__init__(self, ai_game):
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		self.image = pygame.image.load('images/Background1.bmp')
		self.rect = self.image.get_rect()

	def	blitme(self):
		self.screen.blit(self.image, self.rect)
