import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
	def	__init__(self, num_frames):
		super().__init__()

		self.sheet = pygame.image.load('images/explosion1.bmp')
		self.sheet_rect = self.sheet.get_rect()

		self.frame_width = self.sheet_rect.width // num_frames #unlike '/', return a non-float element
		self.frame_height = self.sheet_rect.height // 2

		self.frames = []
		for i in range(num_frames):
			rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
			frame = self.sheet.subsurface(rect)
			self.frames.append(frame)

		self.current_frame = 0
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()
		self.frame_rate = 50 #in ms
		self.last_update = pygame.time.get_ticks() #Return the number of milliseconds since pygame.init() was called.

	def	update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.current_frame += 1
			if self.current_frame < len(self.frames):
				self.image = self.frames[self.current_frame]
				center = self.rect.center
				self.rect = self.image.get_rect()
				self.rect.center = center
			else:
				self.kill()
