import pygame
import sys

class Settings:
	def	__init__(self):
		self.bg_color = (4, 12, 36)
		self.ship_speed = 7.0
		self.screen_width = 1200
		self.screen_height = 800

		self.bullet_speed = 10.0
		self.bullet_width = 20
		self.bullet_height = 3
		self.bullet_color = (255, 186, 186)
		self.bullets_allowed = 20

		self.alien_speed = 3.0
		self.fleet_drop_speed = 5
		self.fleet_direction = 1
		self.number_of_aliens = 10

		self.game_level = 1
		self.ship_limit = 0
