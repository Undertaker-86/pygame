import pygame
from random import randint, choice
import sys

class Player(pygame.sprite.Sprite):
		
	def __init__(self):
		super().__init__()
		
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.3)

		self.hit_sound = pygame.mixer.Sound('audio/doorhit-98828.mp3')
		self.hit_sound.set_volume(0.3)

		self.jump_counter = 0
		self.newColor = [0,0,0,0]
		self.value = 0

		self.cp = self.image.copy()
	
	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.jump_counter == 0:
			self.gravity = -20
			self.jump_sound.play()
			self.jump_counter = 1
		elif self.jump_counter == 1 and keys[pygame.K_SPACE] and self.gravity >= 0:
			self.gravity = -15
			self.jump_sound.play()
			self.jump_counter = 2

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()
		
		self.value += 50
		self.newColor[0] = self.value % 255 
		self.cp.fill(self.newColor[0:3] + [0,], None, pygame.BLEND_RGBA_ADD)		
		
		if self.rect.bottom == 300:
			self.jump_counter = 0
		
	def hit(self,screen):
		screen.blit(self.cp,self.rect)
		self.hit_sound.play()


class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
		# self.spawn_time = pygame.time.get_ticks()

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= (6 + speed_add)
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def main():

	# Import global variable
	global game_active, score, music, spawn_time, start_time

	# Intro screen
	player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
	player_stand = pygame.transform.rotozoom(player_stand,0,2)
	player_stand_rect = player_stand.get_rect(center = (400,200))

	game_name = test_font.render('Pixel Runner',False,(111,196,169))
	game_name_rect = game_name.get_rect(center = (400,80))

	game_message = test_font.render('Press space to run',False,(111,196,169))
	game_message_rect = game_message.get_rect(center = (400,330))


	# Timer 
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer,1500)

	while True:
		
		speed_add = get_current_time() / 10

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				pygame.mixer_music.unload()
				sys.exit()

			pygame.display.update()
			
			if obstacle_timer and pygame.time.get_ticks() % 25 == 0:
				spawn_time = pygame.time.get_ticks()

			if game_active:
				if event.type == obstacle_timer:
					obstacle_group.add(Obstacle(choice(['fly','snail'])))
					elapsed = pygame.time.get_ticks() - spawn_time				
					spawn_rate = max(5000 - speed_add, 500)
					
					if elapsed >= spawn_rate:
						obstacle_group.add(Obstacle(choice(['fly','snail'])))
			else:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game_active = True
					start_time = int(pygame.time.get_ticks() / 1000)
					lives = 3

				if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
					music = toggle_music(music)


		if game_active:
			screen.blit(sky_surface,(0,0))
			screen.blit(ground_surface,(0,300))
			score = display_score()

			player.draw(screen)
			player.update()
			
			obstacle_group.draw(screen)
			obstacle_group.update()

			# player.sprite.blink = True
			# animObj.blit(screen, player.sprite.rect)

			if not collision_sprite():
				player.sprite.hit(screen)
				lives -= 1

			if lives == 0:
				game_active = False

			
		else:
			screen.fill((94,129,162))
			screen.blit(player_stand,player_stand_rect)

			score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
			score_message_rect = score_message.get_rect(center = (400,330))
			screen.blit(game_name,game_name_rect)
			
			if music:
				music_state = test_font.render(f'Music: "p" to toggle', False, 'Green')
			else:
				music_state = test_font.render(f'Music: "p" to toggle', False, 'Red')

			music_state_rect = music_state.get_rect(midleft = (30, 30))
			screen.blit(music_state,music_state_rect)

			#Plays music or not
			if not music:
				pygame.mixer.music.pause()
				# background_music.stop()
			else:
				pygame.mixer.music.unpause()
				# background_music.play()

			if score == 0: screen.blit(game_message,game_message_rect)
			else: screen.blit(score_message,score_message_rect)

		pygame.display.update()
		clock.tick(60)


def get_current_time():
	return int(pygame.time.get_ticks() / 1000) - start_time

def display_score():
	# current_time = int(pygame.time.get_ticks() / 1000) - start_time
	current_time = get_current_time()
	score_surf = score_font.render(f'{current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: 
		return True

def toggle_music(music):
	if music:
		return False
	else:
		return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Pixeltype.ttf', 50)
score_font = pygame.font.Font('Pixeltype.ttf', 80)

# Constant

game_active = False
start_time = 0
score = 0
music = True
speed_add = 0
spawn_time = 0
lives = 3

pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.3)

# background_music = pygame.mixer.Sound('audio/music.wav')
# background_music.set_volume(0.3)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

if __name__ == "__main__":
	main()