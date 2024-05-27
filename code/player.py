import pygame
from settings import *
from utils import import_folder, Status

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):

        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_asssets()

        # state management
        self.status = Status("down") # default

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        self.obstacle_sprites = obstacle_sprites

    def import_player_asssets(self):
        '''
        Imports the different player animations for the 4 direction and 3 different states
        '''
        character_path = 'graphics/player/'
        self.animations = {
            'up': [],'down': [],'left': [],'right': [],
            'right_attack': [],'left_attack': [],'up_attack': [],'down_attack': [],
            'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            self.status += 'idle'


        # attack status
        if self.attacking:
            # don't allow movement when attacking
            self.direction.x = 0
            self.direction.y = 0
            self.status += 'attack'


    def input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status.status = 'down'
        else:
            self.direction.y = 0

        # Attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("attack")
            
        # Magic
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("magic")

    def cooldowns(self):
        '''
        Custom timer
        
        @update: turn into custom class later (?)
        '''
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x  > 0: # moving right
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.rect.right


        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)