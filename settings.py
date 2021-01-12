import pygame
pygame.init()


#screen res
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Holy Knight')


pygame.mixer.pre_init(44100, -16, 2, 512)
fps = 60

#defining game variables
font = pygame.font.SysFont('arial', 90)
font_score = pygame.font.SysFont('arial', 25)

tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 5
score = 0
white = (255, 255, 255)
blue = (0, 0, 255)

#loading images
bg_img = pygame.image.load('other/bgg.png')
bg_img = pygame.transform.scale(bg_img, (1000, 1000))
restart_img = pygame.image.load('other/restart_btn.png')
start_img = pygame.image.load('other/strt_button.png')
exit_img = pygame.image.load('other/exit_btn.png')


#loading sounds
pygame.mixer.music.load('music/medieval.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
sword_equip_fx =  pygame.mixer.Sound('music/mixkit-sword-blade-swish-1506.wav')
sword_equip_fx.set_volume(0.5)
sword_hit_wall_fx =  pygame.mixer.Sound('music/mixkit-sword-cuts-a-chainmail-2790.wav')
sword_hit_wall_fx.set_volume(0.5)
sword_kill_fx =  pygame.mixer.Sound('music/mixkit-sword-slash-swoosh-1476.mp3')
sword_kill_fx.set_volume(0.5)
sword_swing_fx =  pygame.mixer.Sound('music/mixkit-dagger-woosh-1487.wav')
sword_swing_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound('music/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('music/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('music/game_over.wav')
game_over_fx.set_volume(0.5)