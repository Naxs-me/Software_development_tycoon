import pygame as pg
from settings import *
from menu import menu_vendor, menu_shop, menu_tutorial
import os
import math
import random

# Assets
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder,"assets")
chars_folder = os.path.join(assets_folder,"chars")
gabe_folder = os.path.join(chars_folder,"gabe")
hat_guy_folder = os.path.join(chars_folder,"hat-guy")
soundtrack_folder = os.path.join(assets_folder,"soundtrack")
font_name = os.path.join(assets_folder,"PixelEmulator-xq08.ttf")
font = font_name
# Sprite Classes
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name,size)
    text_surface = pg.Surface((100,100))
    text = font.render(text, True, WHITE)
    text_surface.fill(BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    t_rect = text.get_rect()
    t_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)
    surf.blit(text,t_rect)

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.vx = 0
        self.vy = 0
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.direction = 1
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
            self.direction = 0
            self.walking = True
        if keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
            self.direction = 1
            self.walking = True
        if keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
            self.walking = True
        if keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED
            self.walking = True
        if(abs(self.vx) == PLAYER_SPEED and abs(self.vy) == PLAYER_SPEED):
            self.vy = self.vy/math.sqrt(2)
            self.vx = self.vx/math.sqrt(2)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(273,64,24,24)]
        self.standing_frames.append(pg.transform.flip(self.standing_frames[0],True,False))
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walking_frames_r = [self.game.spritesheet.get_image(196,91,24,24),
                                self.game.spritesheet.get_image(298,64,24,24),
                                self.game.spritesheet.get_image(221,91,24,24),
                                self.game.spritesheet.get_image(246,91,24,24),
                                self.game.spritesheet.get_image(271,91,24,24),
                                self.game.spritesheet.get_image(296,91,24,24)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

    def update(self):
        self.get_keys()
        self.animate()
        self.speedx = 0
        self.speedy = 0
        self.walking = False
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        house_contact = pg.sprite.spritecollide(self, self.game.maintenance, False)
        if house_contact:
            menu_vendor(self.game.screen,self.game,WIDTH/2,20)
        vendor_contact = pg.sprite.spritecollide(self,self.game.shop,False)
        if vendor_contact:
            menu_shop(self.game.screen,self.game,WIDTH/2,20)
        tutorial_contact = pg.sprite.spritecollide(self,self.game.tutorial,False)
        if tutorial_contact:
            menu_tutorial(self.game.screen,self.game,WIDTH/2,20)
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
            

    def collide_with_walls(self,dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def animate(self):
        now = pg.time.get_ticks()
        current_center = self.rect.center 
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                #bottom = self.rect.bottom
                if self.direction == 1:
                    self.image = self.walking_frames_r[self.current_frame]
                if self.direction == 0:
                    self.image = self.walking_frames_l[self.current_frame]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom
        else:
            self.image = self.standing_frames[1-self.direction]

        self.image = pg.transform.scale(self.image,(48,48))
        self.rect = self.image.get_rect()
        self.rect.center = current_center


class Developer(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(474,50,16,22)
        self.image = pg.transform.scale(self.image,(32,44))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.bottom = HEIGHT - 50

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image

class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(389,108,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Raw_fence_top(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(324,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Raw_fence_bottom(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(222,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Raw_fence_left(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(171,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Raw_fence_right(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(69,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(439,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass_edge_top(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(456,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path_top(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(473,132,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path_bottom(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(307,168,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass_edge_bottom(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(120,168,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# up

class Path_left(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(103,150,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass_edge_left(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(120,150,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path_right(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(205,168,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass_edge_right(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(52,168,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(103,186,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path_edge_corner(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(494,150,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path_edge_corner2(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.decorations
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(443,168,16,16)
        self.image = pg.transform.scale(self.image,(48,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class House(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.maintenance, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(1,1,70,88)
        self.image = pg.transform.scale(self.image,(140,176))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tree1(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(219,1,53,74)
        self.image = pg.transform.scale(self.image,(106,148))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tree2(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(165,1,53,74)
        self.image = pg.transform.scale(self.image,(106,148))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Dialog_box(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(57,91,112,32)
        self.image = pg.transform.scale(self.image,(1008,576))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Vendor(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.shop, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(400,1,56,51)
        self.image = pg.transform.scale(self.image,(112,102))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tutorial(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.tutorial, game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(323,64,16,23)
        self.image = pg.transform.scale(self.image,(32,46))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

