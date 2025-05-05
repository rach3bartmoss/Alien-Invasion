import pygame
import sys
from rain import Rain

class Raindrops:
	def	__init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1200, 800))
		self.screen_rect = self.screen.get_rect()

		self.screen_width = self.screen.get_rect().width
		self.screen_height = self.screen.get_rect().height

		pygame.display.set_caption("Raindrops")

		self.rains = pygame.sprite.Group()

		self._create_rain()

	def	_create_rain(self):
		rain = Rain(self)
		rain_width, rain_height = rain.rect.size
		current_x, current_y = rain_width, rain_height

		while current_y < (self.screen_height - 3 * rain_height):
			while current_x < (self.screen_width - 2 * rain_width):
				self._create_raindrop(current_x, current_y)
				current_x += 2 * rain_width
			current_x = rain_width
			current_y += 2 * rain_height

	def	_create_raindrop(self, x_position, y_position):
		new_drop = Rain(self)
		new_drop.x = x_position
		new_drop.rect.x = x_position
		new_drop.rect.y = y_position
		self.rains.add(new_drop)

	def	_update_screen(self):
		self.screen.fill((4, 12, 36))
		self.rains.draw(self.screen)
		pygame.display.flip()

	def	_update_rains(self):
		self._change_rain_direction()
		self.rains.update()
		for rain in self.rains.copy():
			if rain.rect.bottom <= 0:
				self.rains.remove(rain)

	def	_change_rain_direction(self):
		for rain in self.rains.sprites():
			rain.rect.y += 5

	def run_game(self):
		while True:
			self._check_events()
			self._update_rains()
			self._update_screen()
			self.clock.tick(60)

	def	_check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()



if __name__ == '__main__':
	rd = Raindrops()
	rd.run_game()
