import pygame, time, random,sys
from pygame.locals import *

class Eggy(pygame.sprite.Sprite):

    def __init__(self):
        super(Eggy, self).__init__()
        self.image = pygame.image.load('eggy_.png').convert()
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        #to keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 0

        #to win game
        if self.rect.right == 800:
            self.kill()


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super(Cat, self).__init__()
        self.image = pygame.image.load('cat_.png').convert()
        self.rect = self.image.get_rect(center=(random.randint(820,900),random.randint(-600,600)))
        self.speed = random.randint(1,5)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill() #kills cat once it leaves screen

pygame.init()
start = time.time()
screen = pygame.display.set_mode((800,600))

class Luna(pygame.sprite.Sprite):
    def __init__(self):
        super(Luna, self).__init__()
        self.image = pygame.image.load('luna_.png').convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(random.randint(810, 850), random.randint(0, 600)))

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()

def text_display(size,colour,word):
    font = pygame.font.SysFont(None, size)
    text_to_display = font.render(word, True, (colour), back)
    display = text_to_display.get_rect()
    display.centerx = screen.get_rect().centerx
    display.centery = screen.get_rect().centery
    screen.blit(text_to_display,display)

def header_display(size,colour,word):
    font = pygame.font.SysFont(None, size)
    text_to_display = font.render(word, True, colour, back)
    display = text_to_display.get_rect()
    display.right = screen.get_rect().right
    display.top = screen.get_rect().top
    screen.blit(text_to_display,display)

def score_display(size,colour,word):
    font = pygame.font.SysFont(None, size)
    text_to_display = font.render(word, True, colour, back)
    display = text_to_display.get_rect()
    display.left = screen.get_rect().left
    display.top = screen.get_rect().top
    screen.blit(text_to_display,display)

def game_over():
    end_game = time.time() + 3
    while time.time() < end_game:
        text_display(80, (255, 255, 255), "Game Over!")

game_name = 'Luna, Eggy & The Cat!'
rgb_1 = random.randint(1,255)
rgb_2 = random.randint(1,255)
rgb_3 = random.randint(1,255)
back = (rgb_1,rgb_2,rgb_3) #background colour


ADDCATS = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCATS, 500) #adds a cat every .5 seconds

ADDLUNAS = pygame.USEREVENT + 2
pygame.time.set_timer(ADDLUNAS, 2000) #adds a luna every 2 seconds

player = Eggy() #creates the player 'Eggy'

background = pygame.Surface(screen.get_size())
background.fill((back))

cats = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
lunas = pygame.sprite.Group()
lives = 4

running = True
#game loop
while running and lives > 0:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDCATS:
            new_cat = Cat()
            cats.add(new_cat)
            all_sprites.add(new_cat)
        elif event.type == ADDLUNAS:
            new_luna = Luna()
            all_sprites.add(new_luna)
            lunas.add(new_luna)
    screen.blit(background, (0, 0))

    header_display(20, (89, 89, 89), game_name)

    font = pygame.font.SysFont(None, 30)
    text_to_display = font.render(str(lives), True, (255,0,0), back)
    display = text_to_display.get_rect()
    display.left = screen.get_rect().left
    display.top = screen.get_rect().top
    screen.blit(text_to_display,display)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    cats.update()
    lunas.update()

    score = time.time() - start
    basicfont = pygame.font.SysFont(None, 30)
    game_score = basicfont.render('{}'.format(int(score * 10)), True, (255, 0, 0), back)
    score_display = game_score.get_rect()
    score_display.centerx = screen.get_rect().centerx
    score_display.top = screen.get_rect().top
    screen.blit(game_score, score_display)


    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)


    if pygame.sprite.spritecollideany(player,cats):
        lives -=1

        if lives <= 0:
            game_over()
            player.kill()
            running = False
        else:
            running = True

    pygame.display.flip()


