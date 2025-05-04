class Settings:
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (4, 12, 36)
		self.ship_speed = 9.0

		#Bullet Settings
		self.bullet_speed = 10.0
		self.bullet_width = 3
		self.bullet_height = 20
		self.bullet_color = (255, 0, 0)
		self.bullets_allowed = 10

		self.alien_speed = 2.0
		self.fleet_drop_speed = 10
		self.fleet_direction = 1

		self.game_level = 1
		self.ship_limit = 0
