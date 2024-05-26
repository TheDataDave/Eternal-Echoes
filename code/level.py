import pygame

from tile import Tile
from player import Player
from debug import debug
from utils import import_csv_layout, import_folder
from settings import *
from random import choice

class Level:
    def __init__(self):

        # get the display surface
        self.display = pygame.display.get_surface()
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # create the map
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'), # boundary: 395
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects'),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': # ignore empty cells
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            # Invisible boundaries
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            # Visible grass blocks
                            Tile((x, y), [self.visible_sprites], 'grass', surface=choice(graphics['grass']))
                        if style == 'object':
                            # Visible object blocks
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                            
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.draw(self.display, self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display = pygame.display.get_surface()

        # setup the offset for the camera
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor.get_rect(topleft=(0,0))

    def draw(self, surface, player=None):
        '''
        @parameter surface: we ignore the surface object and just draw the sprites
        Overides draw: custom camera control
        '''
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

