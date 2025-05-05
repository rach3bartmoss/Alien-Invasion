import pygame
import sys

class	Keys:
	def	__init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((1200, 800))
		pygame.display.set_caption("Key strokes visualizer")

	def	_check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					print(f"{event.key}(KEY RIGHT) pressed.")
				elif event.key == pygame.K_LEFT:
					print(f"{event.key}(KEY LEFT) pressed.")
				elif event.key == pygame.K_UP:
					print(f"{event.key}(KEY UP) pressed.")
				elif event.key == pygame.K_DOWN:
					print(f"{event.key}(KEY DOWN) pressed.")

	def	run_game(self):
		while True:
			pygame.display.flip()
			self._check_events()

if __name__ == '__main__':
	kg = Keys()
	kg.run_game()
