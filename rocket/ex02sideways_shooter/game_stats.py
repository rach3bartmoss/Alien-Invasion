import pygame

class GameStats:
	def	__init__(self, ss_game):
		self.settings = ss_game.settings
		self.reset_stats()

	def	reset_stats(self):
		self.ships_left = self.settings.ship_limit
