import pygame

import pickle
from os import path
from settings import *


clock = pygame.time.Clock()


def getSpriteByPosition(position,group):
    for index,spr in enumerate(group):
        if (index == position):
            return spr
    return False

    return False

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



def reset_level(level):
	global score
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	spike_group.empty()
	exit_group.empty()

	score = 0

	#load in level data and create world
	if path.exists(f'img/data/level{level}_data'):
		pickle_in = open(f'img/data/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	# create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world






class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:

            self.idle_counter += 1

            # get keypresses
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
                self.jump_counter += 1
            if key[pygame.K_SPACE] == False:
                self.jumped = False

            if key[pygame.K_a] and self.equiped:
                sword_swing_fx.play()
                self.attacking = True
                self.attack_counter += 1
            if key[pygame.K_d] and self.equiped:
                self.attacking = True
                # sword_swing_fx.play()
                self.attack_counter += 1
            if key[pygame.K_s] and self.equiped:
                self.attacking = True
                # sword_swing_fx.play()
                self.attack_counter += 1

            if key[pygame.K_LEFT]:
                self.attacking = False
                dx -= 5
                self.counter += 1
                self.direction = -1

            if key[pygame.K_RIGHT]:
                self.attacking = False
                dx += 5
                self.counter += 1
                self.direction = 1

            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_a] == False \
                    and key[pygame.K_d] == False and key[pygame.K_s] == False and key[pygame.K_SPACE] == False:
                self.counter = 0
                self.index = 0
                self.attack_index = 0

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.jump_counter > 0 and self.jumped:
                self.jump_counter = 0
                self.jump_index += 1
                if self.jump_index >= len(self.images_jump_right):
                    self.jump_index = 0
                if self.direction == 1:
                    self.image = self.images_jump_right[self.jump_index]
                if self.direction == -1:
                    self.image = self.images_jump_left[self.jump_index]



            elif self.attack_counter > 5:
                self.attack_counter = 0
                self.attack_index += 1
                if self.attack_index >= len(self.attack_images_right) or self.attack_index >= len(
                        self.attack_images_left) \
                        and self.attack_index >= len(self.attack_images_right_2) and self.attack_index >= len(
                    self.attack_images_left_2) \
                        and self.attack_index >= len(self.attack_images_right_3) and self.attack_index >= len(
                    self.attack_images_left_3):
                    self.attack_index = 0
                if self.attacking and self.direction == 1 and key[pygame.K_a]:
                    self.image = self.attack_images_right[self.attack_index]
                if self.attacking and self.direction == -1 and key[pygame.K_a]:
                    self.image = self.attack_images_left[self.attack_index]
                if self.attacking and self.direction == 1 and key[pygame.K_d]:
                    self.image = self.attack_images_right_2[self.attack_index]
                if self.attacking and self.direction == -1 and key[pygame.K_d]:
                    self.image = self.attack_images_left_2[self.attack_index]
                if self.attacking and self.direction == 1 and key[pygame.K_s]:
                    self.image = self.attack_images_right_3[self.attack_index]
                if self.attacking and self.direction == -1 and key[pygame.K_s]:
                    self.image = self.attack_images_left_3[self.attack_index]

            if self.idle_counter > 10:
                self.idle_counter = 0
                self.idle_index += 1
                if self.idle_index >= len(self.idle_images) or self.idle_index >= len(
                        self.idle_images_left) or self.idle_index >= len(self.idle_images_equiped_right) \
                        or self.idle_index >= len(self.idle_images_equiped_left):
                    self.idle_index = 0
                if self.direction == 1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[
                    pygame.K_a] == False and key[pygame.K_d] == False \
                        and self.equiped == False and key[pygame.K_s] == False and self.dead == False and key[
                    pygame.K_SPACE] == False:
                    self.image = self.idle_images[self.idle_index]
                if self.direction == -1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[
                    pygame.K_a] == False \
                        and self.equiped == False and key[pygame.K_d] == False and key[
                    pygame.K_s] == False and self.dead == False and key[pygame.K_SPACE] == False:
                    self.image = self.idle_images_left[self.idle_index]
                if self.direction == 1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[
                    pygame.K_a] == False \
                        and key[pygame.K_d] == False and self.equiped and key[
                    pygame.K_s] == False and self.dead == False and key[pygame.K_SPACE] == False:
                    self.image = self.idle_images_equiped_right[self.idle_index]
                if self.direction == -1 and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[
                    pygame.K_a] == False \
                        and key[pygame.K_d] == False and self.equiped and key[
                    pygame.K_s] == False and self.dead == False and key[pygame.K_SPACE] == False:
                    self.image = self.idle_images_equiped_left[self.idle_index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            # check for collision
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + 5, self.rect.y, self.width, self.height) and self.equiped and key[
                    pygame.K_a]:
                    # if key[pygame.K_a] and self.destroy_counter <=5 :
                    # 	world.tile_list.remove(tile)
                    # 	self.destroy_counter +=1
                    # 	dx = 0
                    # 	print("attack")
                    world.tile_list.remove(tile)
                    sword_hit_wall_fx.play()
                    self.destroy_counter += 1
                    print("attack")
                if tile[1].colliderect(self.rect.x - 5, self.rect.y, self.width, self.height) and self.equiped and key[
                    pygame.K_a]:
                    world.tile_list.remove(tile)
                    sword_hit_wall_fx.play()
                    self.destroy_counter += 1
                    print("attack")

                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

                # check for collision with enemies
                if pygame.sprite.spritecollide(self, blob_group, False) and self.attacking == False:
                    self.dead = True

                    game_over = -1

                # check for collision with sword
                if pygame.sprite.spritecollide(self, sword_group, False):
                    self.equiped = True
                    sword_equip_fx.play()
                    sword_group.empty()

                if pygame.sprite.spritecollide(self, blob_group, False) and key[pygame.K_d]:
                    a = getSpriteByPosition(0, blob_group)
                    sword_kill_fx.play()
                    blob_group.remove(a)

                # check for collision with spikes
                if pygame.sprite.spritecollide(self, spike_group, False):
                    game_over = -1
                    self.dead = True

                # check for collision with exit
                if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over = 1

                # check for collision with platforms
                for platform in platform_group:
                    # collision in the x direction
                    if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    # collision in the y direction
                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        # check if below platform
                        if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                            self.vel_y = 0
                            dy = platform.rect.bottom - self.rect.top
                        # check if above platform
                        elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                            self.rect.bottom = platform.rect.top - 1
                            self.in_air = False
                            dy = 0
                        # move sideways with the platform
                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction

        elif game_over == -1:
            if self.direction == 1 and self.dead:
                self.image = self.dead_images_right[4]

            if self.direction == -1 and self.dead:
                self.image = self.dead_images_left[4]

            draw_text('GAME OVER!', font, "red", (screen_width // 2) - 200, screen_height // 2)
        # if self.rect.y > 200:
        # 	self.rect.y -= 5

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.dead_images_right = []
        self.dead_images_left = []
        self.attack_images_right = []
        self.attack_images_left = []
        self.attack_images_right_2 = []
        self.attack_images_left_2 = []
        self.attack_images_right_3 = []
        self.attack_images_left_3 = []
        self.idle_images = []
        self.idle_images_left = []
        self.idle_images_equiped_right = []
        self.idle_images_equiped_left = []
        self.index = 0
        self.equiped = False
        self.attacking = False
        self.counter = 0
        self.attack_counter = 0
        self.attack_index = 0
        self.idle_counter = 0
        self.idle_index = 0
        self.jump_counter = 0
        self.jump_index = 0
        self.dead = False
        self.destroy_counter = 0

        for num in range(0, 2):
            img_idle_right = pygame.image.load(f'img/idle/idle-{num}.png')
            img_idle_right = pygame.transform.scale(img_idle_right, (40, 80))
            self.idle_images.append(img_idle_right)
            img_idle_left = pygame.transform.flip(img_idle_right, True, False)
            self.idle_images_left.append(img_idle_left)
        for num in range(2, 3):
            img_jump_right = pygame.image.load(f'img/jump/adventurer-jump-0{num}.png')
            img_jump_right = pygame.transform.scale(img_jump_right, (40, 80))
            img_jump_left = pygame.transform.flip(img_jump_right, True, False)
            self.images_jump_right.append(img_jump_right)
            self.images_jump_left.append(img_jump_left)

        for num in range(0, 2):
        	img_idle_right2 = pygame.image.load(f'img/idle/idle-2-{num}.png')
        	img_idle_right2 = pygame.transform.scale(img_idle_right2, (40, 80))
        	self.idle_images_equiped_right.append(img_idle_right2)
        	img_idle_left2 = pygame.transform.flip(img_idle_right2, True, False)
        	self.idle_images_equiped_left.append(img_idle_left2)

        for num in range(1, 6):
            img_right = pygame.image.load(f'img/run/run{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(0, 5):
            dead_img_right = pygame.image.load(f'img/die/die-{num}.png')
            dead_img_right = pygame.transform.scale(dead_img_right, (40, 80))
            dead_img_left = pygame.transform.flip(img_right, True, False)
            self.dead_images_right.append(dead_img_right)
            self.dead_images_left.append(dead_img_left)

        for num in range(0, 5):
            attack_right_3 = pygame.image.load(f'img/attack/attack{num}.png')
            attack_right_3 = pygame.transform.scale(attack_right_3, (40, 80))
            attack_left_3 = pygame.transform.flip(attack_right_3, True, False)
            self.attack_images_right_3.append(attack_right_3)
            self.attack_images_left_3.append(attack_left_3)
        for num in range(0, 5):
            attack_right = pygame.image.load(f'img/attack/adventurer-attack3-0{num}.png')
            attack_right = pygame.transform.scale(attack_right, (40, 80))
            attack_left = pygame.transform.flip(attack_right, True, False)
            self.attack_images_right.append(attack_right)
            self.attack_images_left.append(attack_left)

        for num in range(0, 5):
            attack_right_2 = pygame.image.load(f'img/attack/attack-2-{num}.png')
            attack_right_2 = pygame.transform.scale(attack_right_2, (40, 80))
            attack_left_2 = pygame.transform.flip(attack_right_2, True, False)
            self.attack_images_right_2.append(attack_right_2)
            self.attack_images_left_2.append(attack_left_2)

        # self.dead_image = pygame.image.load('img/ghost.png')
        self.image = pygame.image.load('img/run/run0.png')
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)

		return action


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('other/dirt.PNG')
        grass_img = pygame.image.load('other/grass.PNG')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size -25)
                    blob_group.add(blob)

                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    spike = Spike(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spike_group.add(spike)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 9:
                    # sword
                    sword = Sword(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    sword_group.add(sword)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)







class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('other/enemy.png')
		self.image = pygame.transform.scale(self.image, (30, 80))
		self.image = self.image.convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1
		#pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
	def dead(self):
		transparent = (0, 0, 0, 0)
		self.image.fill(transparent)



class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('other/p1.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y

	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1




class Spike(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('other/spikes.png')
		self.image = pygame.transform.scale(img, (tile_size +10, tile_size // 2 ))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('other/coin.png')
		# self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)



class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('other/castledoors.png')
		self.image = pygame.transform.scale(img, (int(tile_size * 1.5), int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y






class Sword(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('other/sword.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)











player = Player(100, screen_height - 130)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
sword_group = pygame.sprite.Group()
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)




if path.exists(f'img/data/level{level}_data'):
	pickle_in = open(f'img/data/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)

restart_button = Button(screen_width // 2 - 250, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 500, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 100, screen_height // 1.82, exit_img)





run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))


	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			blob_group.update()
			platform_group.update()
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				#coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

		blob_group.draw(screen)
		platform_group.draw(screen)
		spike_group.draw(screen)
		exit_group.draw(screen)
		coin_group.draw(screen)
		sword_group.draw(screen)

		game_over = player.update(game_over)

		# if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0

		# if player has completed the level
		if game_over == 1:
			# reset game and go to next level
			level += 1
			if level <= max_levels:
				# reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				if restart_button.draw():
					level = 1
					# reset level
					world_data = []
					world = reset_level(level)
					game_over = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False






	pygame.display.update()

pygame.quit()