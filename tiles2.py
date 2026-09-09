import csv
import os
import pygame

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,image,x,y,spritesheet,group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y

        group.add(self)

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))
        
class TileMap():

    def __init__(self,filename,spritesheet,IMP_tiles,P_tiles):
        self.tile_size = 64
        self.start_x,self.start_y = 0,0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename,IMP_tiles,P_tiles)
        self.map_surface = pygame.Surface((self.map_w,self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()
        
        self.IMP_tiles = IMP_tiles
        self.P_tiles = P_tiles

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def draw_map(self,surface):
        surface.blit(self.map_surface,(0,0))

    def read_csv(self,filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data,delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self,filename,IMP_tiles,P_tiles):
        tiles = []
        map = self.read_csv(filename)
        x,y =0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                    self.start_x,self.start_y = x * self.tile_size, y*self.tile_size
                elif tile == "25":
                    tiles.append(Tile("Grass Tile 1.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))
                elif tile == "32":
                    tiles.append(Tile("paved Tile 1.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))
                elif tile == "33":
                    tiles.append(Tile("paved Tile 2.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))
                elif tile == "1":
                    tiles.append(Tile("Grass Tile 1.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))
                elif tile == "8":
                    tiles.append(Tile("Pave Tile 1.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))
                elif tile == "14":
                    tiles.append(Tile("Broken Pave Tile 2.png",x*self.tile_size, y*self.tile_size,self.spritesheet,P_tiles))

                x+=1
            y+=1
        self.map_w,self.map_h = x*self.tile_size,y*self.tile_size
        return tiles
