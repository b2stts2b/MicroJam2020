#Theme: small stuff
 
class Particle:
	def __init__(self, x, y, w, h, color, text, font):
		self.pos = [x, y]
		self.color = color #(R, G, B)
		self.text = text
		self.font = font
		self.final_text = self.font.render(self.text, True, (255-color[0], 255-color[1], 255-color[2]))
		self.text_length = self.final_text.get_rect().w
		self.rect = pygame.Rect(x-(self.text_length+6)//2, y-h//2, self.text_length+6, h)
		self.text_rect = self.final_text.get_rect()
		self.text_rect.center = self.rect.center

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)
		screen.blit(self.final_text, self.text_rect)

	def move(self, mpos):
		if mpos[0] >= self.rect.x and mpos[0] <= self.rect.x+self.rect.w and mpos[1] >= self.rect.y and mpos[1] <= self.rect.y+self.rect.h:
			self.rect.center = mpos
			self.text_rect.center = self.rect.center


	def is_inside(self, mpos):
		if mpos[0] >= self.rect.x and mpos[0] <= self.rect.x+self.rect.w and mpos[1] >= self.rect.y and mpos[1] <= self.rect.y+self.rect.h:
			return True

class Mouse:
	def __init__(self):
		self.is_pressed = False
		self.is_inside = False
		self.index = 0

		self.was_pressed = False

import pygame
pygame.init()
screen_width, screen_height = 600, 400
Screen = pygame.display.set_mode((screen_width, screen_height))
font_size = 20
font = pygame.font.SysFont("courier", font_size, True)

already_found = ["water", "earth", "wind", "fire"]
combinations = [["life", "earth", "fruit"],
				["hydrogen", "carbon", "sugar"],
				["fruit", "sugar", "jam"],
				["carbon", "water", "life"],
				["sand" , "heat", "glass"],
				["water", "earth", "tree"],
				["charcoal", "fire", "heat"],
				["water", "sand", "dirt"],
				["sand", "heat", "glass"],
				["glass", "jam", "Jam Jar"]]

splitting = [["water", "hydrogen", "oxygen"],
			 ["fire", "carbon", "energy"],
			 ["wind", "air", "energy"],
			 ["tree", "charcoal", "leaves"],
			 ["earth", "sand", "sand"]]

element_color = {"water":(50,50,255),
				 "earth":(139,69,19),
				 "life":(124, 204, 59),
				 "hydrogen":(255, 255, 255),
				 "oxygen":(200, 50, 50),
				 "wind":(102,255,255),
				 "fire":(255, 0, 0),
				 "energy":(255, 255, 51),
				 "carbon":(96, 96, 96),
				 "sugar":(255, 204, 229),
				 "fruit":(255, 51, 51),
				 "jam":(255, 51, 51),
				 "air":(153, 255, 255),
				 "glass":(204, 255, 255),
				 "heat":(255, 128, 0),
				 "sand":(255, 178, 102),
				 "tree":(0, 102, 0),
				 "charcoal":(32, 32, 32),
				 "leaves":(0, 104, 0),
				 "Jam Jar":(204, 0, 0),
				 "dirt":(102, 51, 0)}

particleSize = 40
p1 = Particle(100,50,particleSize, particleSize,element_color["water"],"water", font)
p2 = Particle(500,50,particleSize, particleSize,element_color["earth"],"earth", font)
p3 = Particle(100,350,particleSize, particleSize,element_color["wind"],"wind", font)
p4 = Particle(500,350,particleSize, particleSize,element_color["fire"],"fire", font)

mouse = Mouse()
particles = [p1,p2,p3,p4]

def main():
	jar = pygame.image.load("images/JamJar.png")
	pygame.mixer.music.load("sounds/song.mp3")
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)

	sound = pygame.mixer.Sound('sounds/element-created.wav')
	sound.set_volume(0.3)
	ratio = 2808/2275
	game_over = False
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == 27:
					run = False

		Screen.fill((0, 0, 0))
		m = pygame.mouse.get_pressed()
		if m[0] and not mouse.is_pressed:
			mouse.is_pressed = True
			#we clicked
			for i in range(len(particles)-1,-1,-1):
				if particles[i].is_inside(pygame.mouse.get_pos()):
					#We clicked and are inside particle
					mouse.is_inside = True
					mouse.index = i
		elif m[0] and mouse.is_inside:
			particles[mouse.index].move(pygame.mouse.get_pos())
		elif not m[0] and mouse.is_pressed:
			mouse.is_pressed = False
			for i in range(len(particles)-1,-1,-1):
				if mouse.index == i:
					continue
				#top-left
				if particles[i].is_inside(particles[mouse.index].rect.topleft) or particles[i].is_inside(particles[mouse.index].rect.bottomleft) or particles[i].is_inside(particles[mouse.index].rect.topright) or particles[i].is_inside(particles[mouse.index].rect.bottomright) or particles[mouse.index].is_inside(particles[i].rect.topleft) or particles[mouse.index].is_inside(particles[i].rect.bottomleft) or particles[mouse.index].is_inside(particles[i].rect.topright) or particles[mouse.index].is_inside(particles[i].rect.bottomright):
					for combination in combinations:
						if combination[0] == particles[mouse.index].text and combination[1] == particles[i].text or combination[1] == particles[mouse.index].text and combination[0] == particles[i].text:
							if combination[2] not in already_found:
								if combination[2] == "Jam Jar":
									game_over = True
								else:
									particles.append(Particle(screen_width//2, screen_height//2, 0, particleSize, element_color[combination[2]], combination[2], font))
									already_found.append(combination[2])
									pygame.mixer.Channel(0).play(sound)
	

		if m[2] and not mouse.was_pressed:
			mouse.was_pressed = True
			for i in range(len(particles)-1,-1,-1):
				if particles[i].is_inside(pygame.mouse.get_pos()):
					for split in splitting:
						if particles[i].text == split[0]:
							if split[1] not in already_found:
								particles.append(Particle(screen_width//2, screen_height//2-particleSize//2, 0, particleSize, element_color[split[1]], split[1], font))
								already_found.append(split[1])
								pygame.mixer.Channel(0).play(sound)
	
							if split[2] not in already_found:
								particles.append(Particle(screen_width//2, screen_height//2+particleSize//2, 0, particleSize, element_color[split[2]], split[2], font))
								already_found.append(split[2])
								pygame.mixer.Channel(0).play(sound)
	
		elif not m[2]:
			mouse.was_pressed = False

		for i in range(len(particles)-1,-1,-1):
			particles[i].draw(Screen)
		
		pygame.display.update()
		if game_over:
			run = False
			for i in range(1, 200, 1):
				new_jar = pygame.transform.scale(jar, (round(40*(1+i/10)), round(ratio*40*(1+i/10))))
				jar_rect = new_jar.get_rect()
				jar_rect.center = [screen_width//2, screen_height//2]
				Screen.blit(new_jar, jar_rect)
				pygame.display.update()
				pygame.time.delay(1000//60)
			for i in range(199, 20, -1):
				Screen.fill((0, 0, 0))
			
				new_jar = pygame.transform.scale(jar, (round(40*(1+i/10)), round(ratio*40*(1+i/10))))
				jar_rect = new_jar.get_rect()
				jar_rect.center = [screen_width//2, screen_height//2]
				
				you_win_text = font.render("You Win!", True, (255, 255, 255))
				explanation_text = font.render("You discovered the", True, (255, 255, 255))
				explanation_text2 = font.render("jar of Game Jam", True, (255, 255, 255))
				explanation_rect = explanation_text.get_rect()
				explanation_rect2 = explanation_text2.get_rect()
				you_win_rect = you_win_text.get_rect()
				you_win_rect.midbottom = jar_rect.midtop
				explanation_rect.midtop = jar_rect.midbottom
				explanation_rect2.midtop = explanation_rect.midbottom
				

				Screen.blit(you_win_text, you_win_rect)
				Screen.blit(new_jar, jar_rect)
				Screen.blit(explanation_text, explanation_rect)
				Screen.blit(explanation_text2, explanation_rect2)
				
				pygame.display.update()
				pygame.time.delay(1000//60)

			pygame.display.update()
			pygame.time.delay(5000)

main()