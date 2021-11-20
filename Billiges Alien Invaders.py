from math import fabs
import pygame
from pygame.draw import circle
from pygame.version import PygameVersion
from random import randint
import os


class Settings:             #Klasse in der Variablen gespeichert werden
    window_width = 550 
    window_height = 1000
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "Billiges Alien Invaders"
    score = 0
    nof_asteroids1 = 5
    nof_asteroids2 = 5
    HP = 3
    

class Background(object):       #erstellt den Hintergrund
    def __init__(self, filename="background.jpg") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Player(pygame.sprite.Sprite):     #erstellt den Spieler
    def __init__(self) -> None:
        super().__init__()
        self.height = 100
        self.width = 100
        self.image = pygame.image.load(os.path.join(Settings.path_image, "Spaceship.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.stop()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height


    def Rand_Kollision(self):       #sorgt dafür das man nicht über den Fenster Rand hinaus kann
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.stop()
        if self.rect.right + self.speed_h > Settings.window_width:
            self.stop()
        if self.rect.left + self.speed_h < 0:
            self.stop()
        if self.rect.top + self.speed_v < 0:
            self.stop()



    def down(self):         #sorgt für die Bewegung des Spielers
        self.speed_v = 5

    def up(self):
        self.speed_v = -5
        
    def left(self):
        self.speed_h = -5

    def right(self):
        self.speed_h = 5

    def stop(self):
        self.speed_v = self.speed_h = 0

    def update(self):       #kontrolliert ob der Spieler den Rand berührt
        self.Rand_Kollision()
        self.rect.move_ip((self.speed_h, self.speed_v))


    def draw(self, screen): 
        screen.blit(self.image, self.rect)


class Asteroid1(pygame.sprite.Sprite):      #erstellt den ersten Asteroiden
    def __init__(self) -> None:
        super().__init__()
        self.height = randint(30, 100)
        self.width = randint(30, 100)
        self.image = pygame.image.load(os.path.join(Settings.path_image, "asteroid_1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, Settings.window_width - 20)
        self.rect.top = 0
        self.speed_v = randint(1, 5)
        self.score = 0


    def update(self):       #kontrolliert ob der Asteroid unten ankommt und updatet den Score
        self.rect.move_ip(0, self.speed_v)
        if self.rect.right + self.speed_v > Settings.window_height:
            self.kill()
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.kill()
            Settings.score += 1
           


    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroid2(pygame.sprite.Sprite):      #erstellt den zweiten Asteroiden
    def __init__(self) -> None:
        super().__init__()
        self.height = randint(30, 100)
        self.width = randint(30, 100)
        self.image = pygame.image.load(os.path.join(Settings.path_image, "asteroid_2.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, Settings.window_width - 20)
        self.rect.top = 0
        self.speed_v = randint(1, 5)
        self.score = 0


    def update(self):       #kontrolliert ob der Asteroid unten ankommt und updatet den Score
        self.rect.move_ip(0, self.speed_v)
        if self.rect.right + self.speed_v > Settings.window_height:
            self.kill()
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.kill()
            Settings.score += 1
           


    def draw(self, screen):
        screen.blit(self.image, self.rect)






class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "650,30"
        pygame.init()       # PyGame-Setup / Init
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.players = pygame.sprite.GroupSingle()
        self.player = Player()
        self.background = Background()
        self.Asteroids1 = pygame.sprite.Group()
        self.asteroid1 = Asteroid1()
        self.Asteroids2 = pygame.sprite.Group()
        self.asteroid2 = Asteroid2

    def run(self):
        self.running = True
        self.start()
        while self.running: #while schleife die immer wiederholt wird
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self):     	#Kontrolliert wenn man eine taste drückt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.player.down()
                elif event.key == pygame.K_UP:
                    self.player.up()
                elif event.key == pygame.K_LEFT:
                    self.player.left()
                elif event.key == pygame.K_RIGHT:
                    self.player.right()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.stop()
                elif event.key == pygame.K_UP:
                    self.player.stop()
                elif event.key == pygame.K_LEFT:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT:
                    self.player.stop()

    
    def respawn(self):  #resetet den spieler wenn der getroffen wird
        self.players.add(Player())


    def update(self):   #respawnt Asteroiden wenn es unter 5 sind
        #self.collision()
        self.player.update()
        self.Asteroids1.update()
        self.Asteroids2.update()
        if len(self.Asteroids1.sprites()) < 5:
            self.Asteroids1.add(Asteroid1())
        if len(self.Asteroids2.sprites()) < 5:
            self.Asteroids2.add(Asteroid2())


    def draw(self):
            self.background.draw(self.screen)
            self.player.draw(self.screen)
            self.Asteroids1.draw(self.screen)
            self.Asteroids2.draw(self.screen)
            text_surface_score = self.font.render("Punkte: {0}".format(Settings.score), True, (0, 255, 255))    # erstellt die punktestand anzeige
            self.screen.blit(text_surface_score, dest=(20, 20))
            pygame.display.flip()

    def start(self):    #spawnt die Asteroiden
        self.players.add(Player())
        for f in range(Settings.nof_asteroids1):
            self.Asteroids1.add(Asteroid1())
        for f in range(Settings.nof_asteroids2):
            self.Asteroids2.add(Asteroid2())



    def Game_Over(self):    #schließt das Spiel
        self.running = False

    #def collision(self):       #zieht einem ein Leben ab wenn man mit einem Asteroiden kollidiert und setzt den Spieler wieder an den anfang zurück
        #print("lol")
        #self.players.hit = pygame.sprite.groupcollide(self.players, self.Asteroids1, True, False, pygame.sprite.collide_mask)
        #if self.players.hit:
            #print("treffer")
            #Settings.HP -= 1
            #self.respawn()
            #if Settings.HP <= 0:
                #self.Game_Over()



    


if __name__ == "__main__":

    game = Game()
    game.run()


