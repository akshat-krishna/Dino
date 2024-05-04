# Dino

import random
import pygame
import asyncio

# from objects import Ground, Dino, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 200)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)

# IMAGES *********************************************************************

start_img = pygame.image.load('Assets/start_img.png')
start_img = pygame.transform.scale(start_img, (60, 64))

game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('Assets/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('Assets/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

# CLASSES ******************************************************************
class Ground():
	def __init__(self):
		self.image = pygame.image.load('Assets/ground.png')
		self.rect = self.image.get_rect()

		self.width = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width
		self.y = 150

	def update(self, speed):
		self.x1 -= speed
		self.x2 -= speed

		if self.x1 <= -self.width:
			self.x1 = self.width

		if self.x2 <= -self.width:
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))

class Dino():
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.duck_list = []

		for i in range(1, 4):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			img = pygame.transform.scale(img, (52, 58))
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			img = pygame.transform.scale(img, (70, 38))
			self.duck_list.append(img)

		self.dead_image = pygame.image.load(f'Assets/Dino/8.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (52,58))

		self.reset()

		self.vel = 0
		self.gravity = 1
		self.jumpHeight = 15
		self.isJumping = False

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.bottom = self.base

		self.alive = True
		self.counter = 0

	def update(self, jump, duck):
		if self.alive:
			if not self.isJumping and jump:
				self.vel = -self.jumpHeight
				self.isJumping = True

			self.vel += self.gravity
			if self.vel >= self.jumpHeight:
				self.vel = self.jumpHeight

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.isJumping = False

			if duck:
				self.counter += 1
				if self.counter >= 6:
					self.index = (self.index + 1) % len(self.duck_list)
					self.image = self.duck_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			elif self.isJumping:
				self.index = 0
				self.counter = 0
				self.image = self.run_list[self.index]
			else:
				self.counter += 1
				if self.counter >= 4:
					self.index = (self.index + 1) % len(self.run_list)
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

		else:
			self.image = self.dead_image

	def draw(self, win):
		win.blit(self.image, self.rect)

class Cactus(pygame.sprite.Sprite):
	def __init__(self, type):
		super(Cactus, self).__init__()

		self.image_list = []
		for i in range(5):
			scale = 0.65
			img = pygame.image.load(f'Assets/Cactus/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 165

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Ptera(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ptera, self).__init__()

		self.image_list = []
		for i in range(2):
			scale = 0.65
			img = pygame.image.load(f'Assets/Ptera/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.counter += 1
			if self.counter >= 6:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Cloud(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Cloud, self).__init__()
		self.image = pygame.image.load(f'Assets/cloud.png')
		self.image = pygame.transform.scale(self.image, (60, 18))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Star(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Star, self).__init__()
		image = pygame.image.load(f'Assets/stars.png')
		self.image_list = []
		for i in range(3):
			img = image.subsurface((0, 20*(i), 18, 18))
			self.image_list.append(img)
		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

# OBJECTS & GROUPS ***********************************************************

ground = Ground()
dino = Dino(50, 160)

cactus_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()


SCREEN = WIDTH, HEIGHT = (600, 200)

# VARIABLES ******************************************************************

counter = 0
enemy_time = 100
cloud_time = 500
stars_time = 175

SPEED = 5
score = 0
high_score = 0

keys = []
GODMODE = False
DAYMODE = False
AUTO = False
		
# FUNCTIONS ******************************************************************

def reset():
	global counter, SPEED, score, high_score, enemy_time, cloud_time, stars_time, keys, GODMODE, DAYMODE, AUTO

	if score and score >= high_score:
		high_score = score

	counter = 0
	SPEED = 5
	score = 0
	enemy_time = 100
	cloud_time = 500
	stars_time = 175
	keys = []
	GODMODE = False
	DAYMODE = False
	AUTO = False

	cactus_group.empty()
	ptera_group.empty()
	cloud_group.empty()
	stars_group.empty()

	dino.reset()

# CHEATCODES *****************************************************************

# GODMODE -> immortal jutsu ( can't die )
# DAYMODE -> Swap between day and night
# AUTOMOD -> automatic jump and duck
# IAMRICH -> add 10,000 to score
# HISCORE -> highscore is 99999
# SPEEDUP -> increase speed by 2
# SPEEDLO -> decrease speed by 2

async def main():
	global counter, SPEED, score, high_score, enemy_time, cloud_time, stars_time, keys, GODMODE, DAYMODE, AUTO
	# keys = []
	# GODMODE = False
	# DAYMODE = False
	# AUTO = False

	jump = False
	duck = False

	start_page = True
	mouse_pos = (-1, -1)

	running = True
	while running:
		jump = False
		if DAYMODE:
			win.fill(WHITE)
		else:
			win.fill(GRAY)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					running = False

				if event.key == pygame.K_SPACE:
					if start_page:
						start_page = False
					elif dino.alive:
						jump = True
					else:
						reset()

				if event.key == pygame.K_UP:
					jump = True

				if event.key == pygame.K_DOWN:
					duck = True

				key = pygame.key.name(event.key)
				keys.append(key)
				keys = keys[-7:]
				if ''.join(keys).upper() == 'GODMODE':
					GODMODE = not GODMODE

				if ''.join(keys).upper() == 'DAYMODE':
					DAYMODE = not DAYMODE

				if ''.join(keys).upper() == 'AUTOMOD':
					AUTO = not AUTO

				if ''.join(keys).upper() == 'SPEEDUP':
					SPEED += 2
				
				if ''.join(keys).upper() == 'SPEEDLO':
					if SPEED > 5:
						SPEED -= 2

				if ''.join(keys).upper() == 'IAMRICH':
					score += 10000

				if ''.join(keys).upper() == 'HISCORE':
					high_score = 99999

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
					jump = False

				if event.key == pygame.K_DOWN:
					duck = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos

			if event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = (-1, -1)

		if start_page:
			win.blit(start_img, (50, 100))
		else:
			if dino.alive:
				counter += 1
				if counter % int(enemy_time) == 0:
					if random.randint(1, 10) == 5:
						y = random.choice([85, 130])
						ptera = Ptera(WIDTH, y)
						ptera_group.add(ptera)
					else:
						type = random.randint(1, 4)
						cactus = Cactus(type)
						cactus_group.add(cactus)

				if counter % cloud_time == 0:
					y = random.randint(40, 100)
					cloud = Cloud(WIDTH, y)
					cloud_group.add(cloud)

				if counter % stars_time == 0:
					type = random.randint(1, 3)
					y = random.randint(40, 100)
					star = Star(WIDTH, y, type)
					stars_group.add(star)

				if counter % 500 == 0:
					SPEED += 0.1
					enemy_time -= 0.5

				if counter % 5 == 0:
					score += 1


				if not GODMODE:
					for cactus in cactus_group:
						if AUTO:
							dx = cactus.rect.x - dino.rect.x
							if 0 <= dx <= (70 + (score//100)):
								jump = True

						if pygame.sprite.collide_mask(dino, cactus):
							SPEED = 0
							dino.alive = False

					for cactus in ptera_group:
						if AUTO:
							dx = ptera.rect.x - dino.rect.x
							if 0 <= dx <= 70:
								if dino.rect.top <= ptera.rect.top:
									jump = True
								else:
									duck = True
							else:
								duck = False

						if pygame.sprite.collide_mask(dino, ptera):
							SPEED = 0
							dino.alive = False

			ground.update(SPEED)
			ground.draw(win)
			cloud_group.update(SPEED-3, dino)
			cloud_group.draw(win)
			stars_group.update(SPEED-3, dino)
			stars_group.draw(win)
			cactus_group.update(SPEED, dino)
			cactus_group.draw(win)
			ptera_group.update(SPEED-1, dino)
			ptera_group.draw(win)
			dino.update(jump, duck)
			dino.draw(win)

			string_score = str(score).zfill(5)
			for i, num in enumerate(string_score):
				win.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

			if high_score:
				win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
				string_score = f'{high_score}'.zfill(5)
				for i, num in enumerate(string_score):
					win.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

			if not dino.alive:
				win.blit(game_over_img, (WIDTH//2-100, 55))
				win.blit(replay_img, replay_rect)

				if replay_rect.collidepoint(mouse_pos):
					reset()

		pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
		clock.tick(FPS)
		pygame.display.update()
		await asyncio.sleep(0)
	pygame.quit()

# if __name__ == "__main__":
# 	main()


asyncio.run( main())