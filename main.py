import pygame
import json
from random import randint, randrange
from os import path
from sys import exit

try:
    pygame.init()
except:
    print("PyGame wasn't initialized!")

MID_BLUE = (25, 25, 112)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 40, 0)
WIDTH = 500
HEIGHT = 800
VIRUS_HEAL_SPEED = 5
SOAP_SPEED = 5


class Doctor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(path.join('sprites', 'doctor.png'))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 700

    def update(self):
        self.rect.x += player_speed_x
        if self.rect.x > WIDTH - 64:
            self.rect.x = WIDTH - 64
        elif self.rect.x < 0:
            self.rect.x = 0

        self.rect.y += player_speed_y
        if self.rect.y < 100:
            self.rect.y = 100
        elif self.rect.y > HEIGHT - 100:
            self.rect.y = HEIGHT - 100


class Virus(pygame.sprite.Sprite):

    def __init__(self, image_num):
        super().__init__()

        self.images = []

        for i in range(1, 8):
        	self.images.append(pygame.image.load(path.join('sprites', 'virus ' + str(i) + '.png')))

        self.image = self.images[image_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, WIDTH, 71)
        self.rect.y = -100

    def update(self):
        self.rect.y += VIRUS_HEAL_SPEED


class Soap(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(path.join('sprites', 'soap.png'))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = -64

    def update(self):
        self.rect.y -= SOAP_SPEED


class HealObject(pygame.sprite.Sprite):

    def __init__(self, image_num):
        super().__init__()

        self.images = []

        for i in range(1, 9):
            self.images.append(pygame.image.load(path.join('sprites', 'heal' + str(i) + '.png')))

        self.image = self.images[image_num]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, WIDTH, 71)
        self.rect.y = -100

    def update(self):
        self.rect.y += VIRUS_HEAL_SPEED


def get_events():
    global running, player_speed_x, player_speed_y, fire_soap
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_speed_x = 10
            if event.key == pygame.K_LEFT:
                player_speed_x = -10
            if event.key == pygame.K_UP:
                player_speed_y = -10
            if event.key == pygame.K_DOWN:
                player_speed_y = 10
            if event.key == pygame.K_SPACE:
                fire_soap = True
                new_soap()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_speed_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed_y = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return 0, 0


def new_virus():
    global virus_group
    image_num = randint(0, 6)
    virus = Virus(image_num)
    virus_group.add(virus)


def new_soap():
    global soap_group
    soap = Soap()
    soap_group.add(soap)
    soap.rect.x = doctor.rect.x + 17
    soap.rect.y = doctor.rect.y


def new_healing_object():
    global heal_group
    image_num = randint(0, 7)
    heal = HealObject(image_num)
    heal_group.add(heal)
    pygame.sprite.groupcollide(heal_group, virus_group, False, True)


def show_life_bar(x):
	if x > -100:
		color = GREEN
	else:
		color = RED
	pygame.draw.rect(screen, color, (WIDTH - 250 - x, 10, 200 + x, 15))
	screen.blit(heart, (WIDTH - 45, 0))


def show_score():
    score = font.render("Score: " + str(points), True, WHITE)
    screen.blit(score, (10, 10))


def start_screen():
    screen.blit(welcome_text[0], (20, 160))
    screen.blit(welcome_text[1], (20, 190))
    screen.blit(welcome_text[2], (20, 220))
    screen.blit(welcome_text[3], (20, 250))
    screen.blit(welcome_text[4], (20, 280))
    pygame.draw.rect(screen, BLACK, (20, 390, 80, 40))
    pygame.draw.rect(screen, BLACK, (20, 440, 150, 40))
    pygame.draw.rect(screen, BLACK, (20, 490, 70, 40))
    screen.blit(start_text, (30, 400))
    if mute:
        screen.blit(sound_off, (30, 450))
    else:
        screen.blit(sound_on, (30, 450))
    screen.blit(leave, (30, 500))


def beginning_screen():
    global beginning, mute
    while beginning:
        screen.blit(start_background, (0, 0))
        start_screen()
        event = get_events()
        pygame.display.update()
        if event[0] > 0:
            if 20 < event[0] < 100 and 390 < event[1] < 430:
                beginning = False
            elif 20 < event[0] < 170 and 440 < event[1] < 480:
                mute = not mute
            elif 20 < event[0] < 90 and 490 < event[1] < 530:
                pygame.quit()
                exit()


def game_over():
    screen.blit(over_text, (50, 250))
    screen.blit(still_play_text[0], (40, 350))
    screen.blit(still_play_text[1], (40, 380))
    screen.blit(still_play_text[2], (80, 440))
    pygame.draw.rect(screen, BLACK, (140, 490, 60, 40))
    pygame.draw.rect(screen, BLACK, (290, 490, 50, 40))
    pygame.draw.rect(screen, BLACK, (200, 570, 85, 40))
    screen.blit(record_text, (10, 40))
    screen.blit(yes_text, (150, 500))
    screen.blit(no_text, (300, 500))
    screen.blit(menu_text, (210, 580))


def open_json():
	with open('records.txt', 'r') as json_file:
		return json.load(json_file)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_background = pygame.image.load('start_background.jpg')
game_background = pygame.image.load('game_background.jpg')
pygame.display.set_caption("Quarantine")
icon = pygame.image.load(path.join('sprites', 'virus 2.png'))
pygame.display.set_icon(icon)

# Start Screen
welcome = pygame.font.Font("freesansbold.ttf", 20)
options = pygame.font.Font("freesansbold.ttf", 25)
welcome_text = (welcome.render("Welcome! Your mission is to kill as many", True, BLACK),
                welcome.render('viruses as you can. Do not let them touch you', True, BLACK),
                welcome.render('or you will die. Take the cleaning products to', True, BLACK),
                welcome.render('stay safe and heal yourself. Press the arrow', True, BLACK),
                welcome.render('keys to move and the space bar to fire soap.', True, BLACK)
                )
start_text = options.render("Start", True, WHITE)
sound_on = options.render("Sound: on", True, WHITE)
sound_off = options.render("Sound: off", True, WHITE)
leave = options.render("Exit", True, WHITE)

# Sounds
cardi_b = pygame.mixer.Sound(path.join('sounds', 'cardi_b.wav'))
damage = pygame.mixer.Sound(path.join('sounds', 'damage.wav'))
heal_sound = pygame.mixer.Sound(path.join('sounds', 'heal.wav'))
background_song = pygame.mixer.Sound(path.join('sounds', 'background_song.wav'))
background_song.set_volume(0.3)

# Player
doctor = Doctor()
doctor_group = pygame.sprite.Group()
doctor_group.add(doctor)
player_speed_x = 0
player_speed_y = 0
hurt_or_heal = 0
new_enemy_range = 100

# Score
points = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# Heart
heart = pygame.image.load(path.join('sprites', 'heart.png'))

# Enemies
virus_group = pygame.sprite.Group()
new_virus()

# Bullet: soap
soap_group = pygame.sprite.Group()
fire_soap = False

# Healing Objects
heal_group = pygame.sprite.Group()

# Game Over
over = pygame.font.Font("freesansbold.ttf", 64)
still_play = pygame.font.Font("freesansbold.ttf", 25)
yes = pygame.font.Font("freesansbold.ttf", 25)
no = pygame.font.Font("freesansbold.ttf", 25)
menu = pygame.font.Font("freesansbold.ttf", 25)
over_text = over.render("GAME OVER", True, WHITE)
still_play_text = (still_play.render("You died Doctor! Thank you for", True, WHITE),
                   still_play.render("fighting for us. You did a great job.", True, WHITE),
                   still_play.render("Do you want to play again?", True, WHITE))

yes_text = yes.render("Yes", True, WHITE)
no_text = no.render("No", True, WHITE)
menu_text = menu.render("Menu", True, WHITE)

list_of_soap = []
list_of_virus = []
list_of_healing = []

running = True
mute = False
beginning = True
end_game = False

beginning_screen()

if not mute:
    background_song.play(-1)
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    events = get_events()
    if end_game and events[0] > 0:
        if 140 < events[0] < 200 and 490 < events[1] < 530:
            end_game = False
            points = 0
            new_enemy_range = 100
            hurt_or_heal = 0
            new_virus()
            if not mute:
                background_song.play(-1)
        elif 290 < events[0] < 340 and 490 < events[1] < 530:
            running = False
        elif 200 < events[0] < 285 and 570 < events[1] < 610:
            beginning = True
            end_game = False
            points = 0
            hurt_or_heal = 0
            new_virus()
            beginning_screen()
            if not mute:
            	background_song.play(-1)

    screen.blit(game_background, (0, 0))

    if end_game:
        game_over()
        show_score()
        pygame.display.update()
        continue

    if (int(pygame.time.get_ticks() / 1000) + 1) % 5 == 0 and not list_of_healing:
        new_healing_object()

    list_of_soap = soap_group.sprites()
    list_of_virus = virus_group.sprites()
    list_of_healing = heal_group.sprites()

    if list_of_virus and list_of_virus[0].rect.y > (HEIGHT + 64):
        virus_group.remove(list_of_virus[0])

    if list_of_healing and list_of_healing[0].rect.y > (HEIGHT + 64):
        heal_group.remove(list_of_healing[0])

    if list_of_virus and (list_of_virus[0].rect.y % new_enemy_range) == 0:
        new_virus()
        pygame.sprite.groupcollide(heal_group, virus_group, False, True)

    if not list_of_soap:
        fire_soap = False

    if fire_soap:
        if pygame.sprite.groupcollide(soap_group, virus_group, False, False):
            if pygame.sprite.groupcollide(soap_group, virus_group, True, True,
                                          pygame.sprite.collide_mask):
                if not mute:
                    damage.play()
                points += 1
                if (points % 50) == 0:
                	new_enemy_range -= 10
                	if new_enemy_range < 50:
                		new_enemy_range = 50
        if list_of_soap[0].rect.y < 0:
            soap_group.remove(list_of_soap[0])

    if pygame.sprite.groupcollide(doctor_group, virus_group, False, False):
        if pygame.sprite.groupcollide(doctor_group, virus_group, False, True,
                                      pygame.sprite.collide_mask):
            if not mute:
                cardi_b.play()
            hurt_or_heal -= 50
            if hurt_or_heal < -200:
                pygame.sprite.Group.empty(virus_group)
                pygame.sprite.Group.empty(heal_group)
                pygame.sprite.Group.empty(soap_group)
                pygame.mixer.stop()

                if path.exists('records.txt'):
                	last_record = open_json()
                	if last_record['record'] < points:
                		last_record['record'] = points
                else:
                	last_record = {'record': points}

                with open('records.txt', 'w') as outfile:
                	json.dump(last_record, outfile)

                record = pygame.font.Font("freesansbold.ttf", 32)
                record_text = record.render('Record: ' + str(last_record['record']), True, WHITE)
                	
                end_game = True

    if pygame.sprite.groupcollide(doctor_group, heal_group, False, False):
        if pygame.sprite.groupcollide(doctor_group, heal_group, False, True,
                                      pygame.sprite.collide_mask):
            if not mute:
                heal_sound.play()
            hurt_or_heal += 25
            if hurt_or_heal > 0:
                hurt_or_heal = 0

    doctor_group.draw(screen)
    virus_group.draw(screen)
    soap_group.draw(screen)
    heal_group.draw(screen)

    doctor_group.update()
    soap_group.update()
    virus_group.update()
    heal_group.update()

    show_life_bar(hurt_or_heal)
    show_score()

    pygame.display.update()

pygame.quit()
