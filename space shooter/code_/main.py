#
import pygame
from os.path import join
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        

        self.laser_cooldown()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
    def update(self, dt):
        screen.blit(self.image, self.rect)

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, laser_surf, pos):
        super().__init__(groups)
        self.image = laser_surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, meteor_surf, pos):
        super().__init__(groups)
        self.image = meteor_surf
        self.rect = self.image.get_frect(center = pos)
        self.kill_timer = 3000
        self.spawn_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.kill_timer:
            self.kill()


# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space ship game')
Clock = pygame.time.Clock()



# Imports
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = Clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surf, (x, y))

    
    all_sprites.update(dt)
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if collision_sprites:
        player.kill()
    pygame.sprite.groupcollide(meteor_sprites, laser_sprites, True, True)

    # draw the game
    screen.fill('DarkGrey')
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
