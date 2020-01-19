import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from menu import *

class Game:
    def __init__(self):
        #initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT),pg.FULLSCREEN)
        # self.window = pg.display.set_mode((1920,1080),pg.FULLSCREEN)
        # self.resized_screen = pg.transform.scale(self.screen,(1920,1080))
        # self.window.blit(self.resized_screen,(0,0))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.isContact = 0
        self.running = True
        self.coder_count = 1
        self.tester_count = 1
        self.load_data()

    def load_data(self):
        gabe_spritesheet = os.path.join(assets_folder,SPRITESHEET)
        self.spritesheet = Spritesheet(gabe_spritesheet)
        main_map = os.path.join(assets_folder,MAP)
        self.map = Map(main_map)

    def new(self):
        #initialize the game
        #Load sound
        pg.mixer.music.load(os.path.join(soundtrack_folder,"Red Carpet Wooden Floor.mp3"))
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(loops = -1)
        
        #Load graphics
        self.all_sprites = pg.sprite.Group()
        self.shop = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.tutorial = pg.sprite.Group()
        self.decorations = pg.sprite.Group()
        self.maintenance = pg.sprite.Group()
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                Grass(self,col,row)
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self,col,row)
                if tile == '1':
                    Grass(self,col,row)
                    Raw_fence_top(self,col,row)
                if tile == '2':
                    Grass_edge_top(self,col,row)
                if tile == '3':
                    Grass_edge_bottom(self,col,row)
                if tile == '4':
                    Path_top(self,col,row)
                if tile == '5':
                    Path_bottom(self,col,row)
                if tile == '6':
                    Grass(self,col,row)
                    Raw_fence_left(self,col,row)
                if tile == '7':
                    Grass(self,col,row)
                    Raw_fence_right(self,col,row)
                if tile == 'k':
                    Vendor(self,col,row)
                if tile == '8':
                    Grass(self,col,row)
                    Raw_fence_bottom(self,col,row)
                if tile == '9':
                    Grass_edge_left(self,col,row)
                if tile == 'a':
                    Grass_edge_right(self,col,row)
                if tile == 'b':
                    Path_left(self,col,row)
                if tile == 'c':
                    Path_right(self,col,row)
                if tile == 'd':
                    Path(self,col,row)
                if tile == 'e':
                    Grass(self,col,row)
                if tile == 'f':
                    Path_edge_corner(self,col,row)
                if tile == 'g':
                    Path_edge_corner2(self,col,row)
                if tile == 'i':
                    Tree1(self,col,row)
                if tile == 'j':
                    Tree2(self,col,row)
                if tile == 'h':
                    House(self,col,row)
                if tile == 'l':
                    Tutorial(self,col,row)
                


        self.all_sprites.add(self.player)
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        #game loop
        # self.window.blit(pg.transform.scale(self.screen,(1920,1080)),(0,0))
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()


    def update(self):
        #game loop update
        self.all_sprites.update()
        #collision check
        self.isContact = 0
        #contact = pg.sprite.spritecollide(self.player, self.maintenance, False)
        # if contact:
        #     print("Test")
        #     self.isContact = 1
        self.camera.update(self.player)


    def events(self):
        #game loop events
        esc = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx = -1)
            #         self.direction = 0
            #         self.walking = True
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx = 1)
            #         self.direction = 1
            #         self.walking = True
            #     if event.key == pg.K_UP:
            #         self.player.move(dy = -1)
            #         self.walking = True
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy = 1)
            #         self.walking = True
                # if(abs(self.speedx) == SPEED and abs(self.speedy) == SPEED):
                #     self.speedy = self.speedy/math.sqrt(2)
                #     self.speedx = self.speedx/math.sqrt(2)

    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,WHITE,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen,WHITE,(0,y),(WIDTH,y))

    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        # if self.isContact == 1:
        #     for event in pg.event.get(): 
        #         if event.type==pg.KEYUP:
        #             if event.key==pg.K_SPACE:
        #                 menu_vendor(self.screen,self,WIDTH/2,20)

        hud_background(self.screen,self,1178,10)
        hud_background_cover(self.screen,self,1177,16)
        hud(self.screen,self)

        #last
        pg.display.flip()


    def show_start_screen(self):
        menu=True
        selected="start"
        while menu:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_UP:
                        selected="start"
                    elif event.key==pg.K_DOWN:
                        selected="quit"
                    if event.key==pg.K_RETURN:
                        if selected=="start":
                            print("Start")
                            menu = False
                            break
                        if selected=="quit":
                            pg.quit()
                            quit()
    
            # Main Menu UI
            background_image = pg.image.load(os.path.join(assets_folder,"Background.png")).convert()
            title=text_format("Software Development Simulator", font,40 , yellow)
            if selected=="start":
                text_start=text_format("START", font, 50, WHITE)
            else:
                text_start = text_format("START", font, 50, BLACK)
            if selected=="quit":
                text_quit= text_format("QUIT", font, 50, WHITE)
            else:
                text_quit = text_format("QUIT", font, 50, BLACK)
    
            title_rect=title.get_rect()
            start_rect=text_start.get_rect()
            quit_rect=text_quit.get_rect()
    
            # Main Menu Text
            self.screen.blit(background_image,(0,0))
            self.screen.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
            self.screen.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
            self.screen.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))
            pg.display.update()
            self.clock.tick(FPS)
            pg.display.set_caption(TITLE)

        menu_intro(self.screen,self,WIDTH/2,20)

    def show_go_screen(self):
        #set gameover screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()