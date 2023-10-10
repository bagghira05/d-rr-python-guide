import pygame, sys, settings
import button
from random import randint
from pygame import Vector2

UP = Vector2(0,-1)
DOWN = Vector2(0,1)
LEFT = Vector2(-1,0)
RIGHT = Vector2(1,0)

enable_crunch_sound = True
# Game state
game_paused:bool = False
menu_state = "main"
game_over_state = False

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
		self.direction = Vector2(1,0)
		self.new_block = False
		# Snake Sprite Imports + Sound
		self.head_up = pygame.image.load(settings.SPRITE_DIR/"head_up.png").convert_alpha()
		self.head_down = pygame.image.load(settings.SPRITE_DIR/"head_down.png").convert_alpha()
		self.head_right = pygame.image.load(settings.SPRITE_DIR/"head_right.png").convert_alpha()
		self.head_left = pygame.image.load(settings.SPRITE_DIR/"head_left.png").convert_alpha()
		
		self.tail_up = pygame.image.load(settings.SPRITE_DIR/"tail_up.png").convert_alpha()
		self.tail_down = pygame.image.load(settings.SPRITE_DIR/"tail_down.png").convert_alpha()
		self.tail_right = pygame.image.load(settings.SPRITE_DIR/"tail_right.png").convert_alpha()
		self.tail_left = pygame.image.load(settings.SPRITE_DIR/"tail_left.png").convert_alpha()

		self.body_vertical = pygame.image.load(settings.SPRITE_DIR/"body_vertical.png").convert_alpha()
		self.body_horizontal = pygame.image.load(settings.SPRITE_DIR/"body_horizontal.png").convert_alpha()

		self.body_tr = pygame.image.load(settings.SPRITE_DIR/"body_tr.png").convert_alpha()
		self.body_tl = pygame.image.load(settings.SPRITE_DIR/"body_tl.png").convert_alpha()
		self.body_br = pygame.image.load(settings.SPRITE_DIR/"body_br.png").convert_alpha()
		self.body_bl = pygame.image.load(settings.SPRITE_DIR/"body_bl.png").convert_alpha()
		self.crunch_sound = pygame.mixer.Sound(settings.SOUND_DIR/"crunch.wav")
	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index, block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical, block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal, block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)
	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down
	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
	def move_snake(self):
		if self.new_block:
			body_copy = self.body[:]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]
	def add_block(self):
		self.new_block = True
	def play_crunch_sound(self):
		self.crunch_sound.play()
	def reset(self):
		self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
		self.direction = Vector2(1,0)


class FRUIT:
	def __init__(self) -> None:
		self.randomize()
	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
		screen.blit(apple, fruit_rect)
		#pygame.draw.rect(screen,(255,0,0),fruit_rect)
	def randomize(self):
		self.x = randint(0,cell_number-1)
		self.y = randint(0,cell_number-1)
		self.pos = Vector2(self.x,self.y)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.game_over_state:bool = False
	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()
	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()
	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			if enable_crunch_sound:
				self.snake.play_crunch_sound()
		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()
	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()
		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0:
				for col in range(cell_size):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_size):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
	def game_over(self):
		self.snake.reset()
		self.game_over_state = True
	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(f"x{score_text}",True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption("Snake Game")
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load(settings.SPRITE_DIR / "apple.png").convert_alpha()
game_font = pygame.font.Font(settings.FONT_DIR / "BAHNSCHRIFT.TTF", 25)
#Button Imgs
resume_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_resume.png").convert_alpha()
options_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_options.png").convert_alpha()
quit_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_quit.png").convert_alpha()
back_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_back.png").convert_alpha()
keys_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_keys.png").convert_alpha()
audio_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_audio.png").convert_alpha()
video_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_video.png").convert_alpha()
reset_img = pygame.image.load(settings.SPRITE_DIR/"buttons"/"button_reset.png").convert_alpha()
#Buttons
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(304, 225, options_img, 1)
quit_button = button.Button(304, 325, quit_img, 1)
quit_button_2 = button.Button(304, 525, quit_img, 1)
reset_button = button.Button(304, 425, reset_img, 1)
back_button = button.Button(304, 425, back_img, 1)
keys_button = button.Button(304, 225, keys_img, 1)
audio_button = button.Button(304, 325, audio_img, 1)
video_button = button.Button(304, 125, video_img, 1)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			if not game_paused:
				main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_paused ^= True
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = UP
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = DOWN
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = LEFT
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = RIGHT

	screen.fill((175,215,70))
	if main_game.game_over_state == True:
		if reset_button.draw(screen):
			print("reset Game")
		if quit_button_2.draw(screen):
			pygame.quit()
			sys.exit()
	elif game_paused == True:
		screen.fill((52,87,91))
		if menu_state == "main":
			if resume_button.draw(screen):
				game_paused = False
			elif options_button.draw(screen):
				menu_state = "options"
			elif quit_button.draw(screen):
				pygame.quit()
				sys.exit()
		elif menu_state == "options":
			if back_button.draw(screen):
				menu_state = "main"
			elif keys_button.draw(screen):
				pass
			elif audio_button.draw(screen):
				pass
			elif video_button.draw(screen):
				pass
	else:	
		main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)