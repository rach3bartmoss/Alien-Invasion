import pygame

class	Rocket:
	def	__init__(self, rd_game):
		self.screen = rd_game.screen
		self.settings = rd_game.settings
		self.screen_rect = rd_game.screen.get_rect()

		self.original_image = pygame.image.load('images/rocket.bmp')
		self.image = self.original_image
		self.rect = self.image.get_rect()

		self.rect.center = self.screen_rect.center

		self.rotate_left = False
		self.rotate_right = False
		self.angle = 0

	def	blitme(self):
		self.screen.blit(self.image, self.rect)

	def	update(self):
		if self.rotate_right:
			self.angle += 4
		if self.rotate_left:
			self.angle -= 4
		self.image = pygame.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)
