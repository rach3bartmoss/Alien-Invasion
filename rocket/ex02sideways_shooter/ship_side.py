import	pygame

class Ship:
	def	__init__(self, ss_game):
		self.screen = ss_game.screen
		self.settings = ss_game.settings
		self.screen_rect = ss_game.screen.get_rect()

		self.image = pygame.image.load('images/ship.bmp')
		self.image = pygame.transform.rotate(self.image, -90)
		self.rect = self.image.get_rect()

		self.rect.midleft = self.screen_rect.midleft

		self.moving_up = False
		self.moving_down = False
		self.y = float(self.rect.y)

	def	blitme(self):
		self.screen.blit(self.image, self.rect)

	def	update(self):
		if self.moving_up and self.rect.top > 0:
			self.y -= self.settings.ship_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed
		self.rect.y = int(self.y)

	def	center_ship(self):
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
