#
import pygame
from os.path import join
import random

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space ship game')
left = False
# Surface
surf = pygame.Surface((100, 200))
surf.fill('BlueViolet')
x = 100

# Import an image

player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range (20)]
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomright = (WINDOW_WIDTH -10, WINDOW_HEIGHT - 10))
# Stars


while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    screen.fill('DarkGrey')
    for pos in star_positions:
        screen.blit(star_surf, pos)
    screen.blit(meteor_surf, meteor_rect)
    if (player_rect.right < WINDOW_WIDTH) and (left == False):
        player_rect.left += 0.2
    elif (player_rect.left >= 0) and (left == True):
        player_rect.left -= 0.2
    elif left == False:
        left = True
    elif left == True:
        left = False
    screen.blit(laser_surf, laser_rect)
    screen.blit(player_surf, player_rect)
    pygame.display.update()

pygame.quit()
