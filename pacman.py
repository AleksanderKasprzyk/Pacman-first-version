"""
Część I - Importowanie modułów bibliotek (zbiory funkcji, klas i zmiennych
z innych plików). Do skorzystania z konkretnych elementów z danego modułu
korzysta się z zapisu "from ... import ...". Natomiast, aby skorzystać ze
wszystkich elementów z danego modułu trzeba wtedy wykorzystać
zapis "from ... import *".
"""
import copy
import math
import pygame
from board import boards

"""
Wywołanie funkcji poniżej jest często pierwszym krokiem w programie 
korzystającym z biblioteki Pygame. Ta funkcja inicjuje wszystkie moduły 
biblioteki Pygame, które są potrzebne do korzystania z jej funkcji.

Dokładniej mówiąc, pygame.init() wykonuje następujące czynności:

-Inicjuje moduł odpowiedzialny za obsługę ekranu i wyświetlanie grafiki.
-Inicjuje moduł obsługujący dźwięk.
-Inicjuje moduł obsługujący obsługę zdarzeń (np. naciśnięcia klawiszy, 
ruch myszy).
-Inicjuje moduł obsługujący czcionki i tekst.
-Inicjuje moduł obsługujący inne funkcje, takie jak obsługa czasu.
"""
pygame.init()

width = 900                                                 #Szerokość okna gry (w pikselach)
height = 950                                                #Wysokość okna gry (również podawana w pikselach)
screen = pygame.display.set_mode([width, height])           #Jest to obiekt ekranu (przy skorzystaniu funkcji i rozmiarów wyżej)
timer = pygame.time.Clock()                                 #Zegar do kontrolowania ilości klatek na sekundę
fps = 60                                                    #Ilość klatek na sekundę
font = pygame.font.Font("freesansbold.ttf", 20)             #Font - czcionka używana np. do wyświetlenia punktów o rozmiarze 20
level = copy.deepcopy(boards)
color = "blue"
flicker = False
game_over = False
game_won = False

                #  R,    L,     U,     D
turns_allowed = [False, False, False, False]
direction_command = 0

pi = math.pi
player_image = []
direction = 0
counter = 0

for i in range(1, 5):
    player_image.append(pygame.transform.scale(pygame.image.load(f"player_image/{i}.png"), (45, 45)))

player_x = 450
player_y = 663
player_speed = 2
ghost_speed = [2, 2, 2, 2]
lives = 3
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0
# startup_counter += 1

blinky_image = pygame.transform.scale(pygame.image.load(f"ghost_images/red.png"), (45, 45))
blinky_x = 56
blinky_y = 58
blinky_direction = 0
blinky_dead = False
blinky_box = False

inky_image = pygame.transform.scale(pygame.image.load(f"ghost_images/blue.png"), (45, 45))
inky_x = 440
inky_y = 388
inky_direction = 2
inky_dead = False
inky_box = False

pinky_image = pygame.transform.scale(pygame.image.load(f"ghost_images/pink.png"), (45, 45))
pinky_x = 440
pinky_y = 438
pinky_direction = 2
pinky_dead = False
pinky_box = False

clyde_image = pygame.transform.scale(pygame.image.load(f"ghost_images/orange.png"), (45, 45))
clyde_x = 440
clyde_y = 438
clyde_direction = 2
clyde_dead = False
clyde_box = False

ghost_speed = 2
spooked_image = pygame.transform.scale(pygame.image.load(f"ghost_images/powerup.png"), (45, 45))
dead_image = pygame.transform.scale(pygame.image.load(f"ghost_images/dead.png"), (45, 45))

targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, image, direct, dead, box, id):
        self.x_position = x_coord
        self.y_position = y_coord
        self.center_x_position = self.x_position + 22
        self.center_y_position = self.y_position + 22
        self.target = target
        self.speed = speed
        self.image = image
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()



    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.image, (self.x_position, self.y_position))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_image, (self.x_position, self.y_position))
        else:
            screen.blit(dead_image, (self.x_position, self.y_position))

        ghost_rect = pygame.rect.Rect((self.center_x_position - 18, self.center_y_position - 18), (36, 36))
        return  ghost_rect

    def check_collisions(self):
        number1 = ((height - 50) // 32)
        number2 = (width // 30)
        number3 = 15

        self.turns = [False, False, False, False]
        if 0 < self.center_x_position // 30 < 29:
            if level[(self.center_y_position - number3) // number1][self.center_x_position // number2] == 9:
                self.turns[2] = True

            if level[self.center_y_position // number1][(self.center_x_position - number3) // number2] < 3 \
                    or level[self.center_y_position // number1][(self.center_x_position - number3) // number2] == 9 \
                    and (self.in_box or self.dead):
                self.turns[1] = True

            if level[self.center_y_position // number1][(self.center_x_position + number3) // number2] < 3 \
                    or level[self.center_y_position // number1][(self.center_x_position + number3) // number2] == 9 \
                    and (self.in_box or self.dead):
                self.turns[0] = True

            if level[(self.center_y_position + number3) // number1][(self.center_x_position // number2)] < 3 \
                    or level[(self.center_y_position + number3) // number1][(self.center_x_position // number2) // number2] == 9 \
                    and (self.in_box or self.dead):
                self.turns[3] = True

            if level[self.center_y_position // number1][(self.center_x_position + number3) // number2] < 3 \
                    or level[self.center_y_position // number1][(self.center_x_position + number3) // number2] == 9 \
                    and (self.in_box or self.dead):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x_position % number2 <= 18:
                    if level[(self.center_y_position + number3) // number1][self.center_x_position // number2] <3 \
                        or (level[(self.center_y_position + number3) // number1][self.center_x_position // number2] == 9 and \
                            self.in_box or self.dead):
                        self.turns[3] = True

                    if level[(self.center_y_position - number3) // number1][self.center_x_position // number2] <3 \
                        or (level[(self.center_y_position - number3) // number1][self.center_x_position // number2] == 9 and \
                            self.in_box or self.dead):
                        self.turns[2] = True

                if 12 <= self.center_y_position % number1 <= 18:
                    if level[self.center_y_position // number1][(self.center_x_position - number3) // number2] < 3 \
                            or (level[self.center_y_position // number1][(self.center_x_position - number3) // number2] == 9 and \
                                self.in_box or self.dead):
                        self.turns[1] = True

                    if level[self.center_y_position // number1][(self.center_x_position + number3) // number2] < 3 \
                            or (level[self.center_y_position // number1][(self.center_x_position + number3) // number2] == 9 and \
                                self.in_box or self.dead):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x_position % number2 <= 18:
                    if level[(self.center_y_position + number3) // number1][self.center_x_position // number2] <3 \
                        or (level[(self.center_y_position + number3) // number1][self.center_x_position // number2] == 9 and \
                            self.in_box or self.dead):
                        self.turns[3] = True

                    if level[(self.center_y_position - number3) // number1][self.center_x_position // number2] <3 \
                        or (level[(self.center_y_position - number3) // number1][self.center_x_position // number2] == 9 and \
                            self.in_box or self.dead):
                        self.turns[2] = True

                if 12 <= self.center_y_position % number1 <= 18:
                    if level[self.center_y_position // number1][(self.center_x_position - number3) // number2] < 3 \
                            or (level[self.center_y_position // number1][(self.center_x_position - number3) // number2] == 9 and \
                                self.in_box or self.dead):
                        self.turns[1] = True

                    if level[self.center_y_position // number1][(self.center_x_position + number3) // number2] < 3 \
                            or (level[self.center_y_position // number1][(self.center_x_position + number3) // number2] == 9 and \
                                self.in_box or self.dead):
                        self.turns[0] = True

        else:
            self.turns[0] = True
            self.turns[1] = True

        if 350 < self.x_position < 550 and 370 < self.y_position < 490:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_clyde(self):
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                if self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                else:
                    self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_position and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                if self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                else:
                    self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_position and self.turns[1]:
                self.direction = 1
                self.x_position -= self.speed
            elif self.target[1] < self.y_position and self.turns[2]:
                self.direction = 2
                self.y_position -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_position -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_position and self.turns[3]:
                self.y_position += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_position += self.speed
        if self.x_position < -30:
            self.x_position = 900
        elif self.x_position > 900:
            self.x_position - 30
        return self.x_position, self.y_position, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                self.x_position += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_position and self.turns[2]:
                self.direction = 2
                self.y_position -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[2]:
                self.y_position -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_position and self.turns[3]:
                self.y_position += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[3]:
                self.y_position += self.speed
        if self.x_position < -30:
            self.x_position = 900
        elif self.x_position > 900:
            self.x_position - 30
        return self.x_position, self.y_position, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                if self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                else:
                    self.x_position += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_position and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                if self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                else:
                    self.x_position -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_position and self.turns[2]:
                self.direction = 2
                self.y_position -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[2]:
                self.y_position -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_position and self.turns[3]:
                self.y_position += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[3]:
                self.y_position += self.speed
        if self.x_position < -30:
            self.x_position = 900
        elif self.x_position > 900:
            self.x_position - 30
        return self.x_position, self.y_position, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_position and self.turns[0]:
                self.x_position += self.speed

            elif not self.turns[0]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
            elif self.turns[0]:
                self.x_position += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y_position and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_position and self.turns[1]:
                self.x_position -= self.speed

            elif not self.turns[1]:
                if self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
            elif self.turns[1]:
                self.x_position -= self.speed

        elif self.direction == 2:
            if self.target[0] < self.x_position and self.turns[1]:
                self.direction = 1
                self.x_position -= self.speed
            elif self.target[1] < self.y_position and self.turns[2]:
                self.direction = 2
                self.y_position -= self.speed

            elif not self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] > self.y_position and self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_position += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed

            elif self.turns[2]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_position -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_position and self.turns[3]:
                self.y_position += self.speed

            elif not self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.target[1] < self.y_position and self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_position -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed

            elif self.turns[3]:
                if self.target[0] > self.x_position and self.turns[0]:
                    self.direction = 0
                    self.x_position += self.speed
                elif self.target[0] < self.x_position and self.turns[1]:
                    self.direction = 1
                    self.x_position -= self.speed
                else:
                    self.y_position += self.speed

        if self.x_position < -30:
            self.x_position = 900
        elif self.x_position > 900:
            self.x_position - 30

        return self.x_position, self.y_position, self.direction

def draw_board(lvl):
    number1 = ((height - 50) // 32)
    number2 = (width // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, "white", (j * number2 + (0.5 * number2), i * number1 + (0.5 * number1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, "white", (j * number2 + (0.5 * number2), i * number1 + (0.5 * number1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * number2 + (0.5 * number2), i * number1), (j * number2 + (0.5 * number2), i * number1 + number1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * number2, i * number1 + (0.5 * number1)), (j * number2 + number2, i * number1 + (0.5 * number1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * number2 - (number2 * 0.4)), (i * number1 + (0.5 * number1)), number2, number1], 0, pi/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * number2 + (number2 * 0.5)), (i * number1 + (0.5 * number1)), number2, number1], pi/2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * number2 + (number2 * 0.5)), (i * number1 - (0.4 * number1)), number2, number1], pi, 3*pi/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * number2 - (number2 * 0.4)) - 2, (i * number1 - (0.4 * number1)), number2, number1], 3*pi/2, 2*pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, "white", (j * number2, i * number1 + (0.5 * number1)), (j * number2 + number2, i * number1 + (0.5 * number1)), 3)

def draw_player():
    if direction == 0:
        screen.blit(player_image[counter//5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_image[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_image[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_image[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    number1 = (height - 50) // 32
    number2 = (width // 30)
    number3 = 15

    if centerx // 30 < 29:
        if direction == 0:
            if level[int(centery / number1)][int((centerx - number3) // number2)] < 3:
                turns[1] = True
        if direction == 1:
            if level[int(centery / number1)][int((centerx + number3) // number2)] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + number3) // number1][centerx // number2] < 3:
                turns[3] = True
        if direction == 3:
            if level[int((centery - number3) // number1)][int(centerx // number2)] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % number2 <= 18:
                if level[(centery + number3) // number1][centerx // number2] < 3:
                    turns[3] = True
                if level[(centery - number3) // number1][centerx // number2] < 3:
                    turns[2] = True
            if 12 <= centery % number1 <= 18:
                if level[centery // number1][(centerx - number2) // number2] < 3:
                    turns[1] = True
                if level[centery // number1][(centerx + number2) // number2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= centerx % number2 <= 18:
                if level[(centery + number1) // number1][centerx // number2] < 3:
                    turns[3] = True
                if level[(centery - number1) // number1][centerx // number2] < 3:
                    turns[2] = True
            if 12 <= centery % number1 <= 18:
                if level[centery // number1][(centerx - number3) // number2] < 3:
                    turns[1] = True
                if level[centery // number1][(centerx + number2) // number2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True
    return turns

def check_collisions(scores, power, power_counter, eaten_ghosts):
    number1 = (height - 50) // 32
    number2 = width // 30
    if 0 < player_x < 870:
        if level[center_y // number1][center_x // number2] == 1:
            level[center_y // number1][center_x // number2] = 0
            scores += 10

        if level[center_y // number1][center_x // number2] == 2:
            level[center_y // number1][center_x // number2] = 0
            scores += 50
            power = True
            power_counter = 0
            eaten_ghosts = [False, False, False, False]

    return scores, power, power_counter, eaten_ghosts

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def draw_misc():
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_image[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

run = True                                                  #W tym przypadku "run = True" oznacza, że pętla gry będzie działać, dopóki nie zostanie zmieniony stan logiczny na False.
while run:
    timer.tick(fps)
    screen.fill("black")

    draw_board(level)
    draw_player()
    draw_misc()

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_image, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_image, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_image, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_image, clyde_direction, clyde_dead, clyde_box, 3)

    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    center_x = player_x + 23
    center_y = player_y + 24
    # pygame.draw.circle(screen, "white", (center_x, center_y), 2)
    turns_allowed = check_position(center_x, center_y)
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    if moving:
        player_x, player_y = move_player(player_x, player_y)

        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

        if direction_command == 0 and turns_allowed[0]:
            direction = 0
        if direction_command == 1 and turns_allowed[1]:
            direction = 1
        if direction_command == 2 and turns_allowed[2]:
            direction = 2
        if direction_command == 3 and turns_allowed[3]:
            direction = 3

        if player_x > 900:
            player_x = -47
        elif player_x < - 50:
            player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()