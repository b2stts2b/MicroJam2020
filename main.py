#Theme: small stuff

class Particle:
	def __init__(self, x, y, rad, color):
		self.pos = [x, y]
		self.rad = rad
		self.color = color #(R, G, B)

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.pos, self.rad)

import pygame

screen_width, screen_height = 600, 400
Screen = pygame.display.set_mode((screen_width, screen_height))

p = Particle(300, 200, 25, (50, 250, 0))

def main():
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		p.draw(Screen)


		pygame.display.update()

main()