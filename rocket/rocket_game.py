import pygame
import sys
from settings import Settings
from rocket import Rocket

class	RocketGame:
	def	__init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((1200, 800))
		pygame.display.set_caption("Rocket Dash")

		self.rocket = Rocket(self)

	def	run_game(self):
		while True:
			self._check_events()
			self.rocket.update()
			self._update_screen()
			self.clock.tick(60)

	def	_update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.rocket.blitme()
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
		elif event.key == pygame.K_RIGHT:
			self.rocket.rotate_right = True
		elif event.key == pygame.K_LEFT:
			self.rocket.rotate_left = True

	def	_check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.rocket.rotate_right = False
		elif event.key == pygame.K_LEFT:
			self.rocket.rotate_left = False



if	__name__ == '__main__':
	rd = RocketGame()
	rd.run_game()
