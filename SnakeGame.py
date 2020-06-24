import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#Defines the cubes that makes up the grid, as well as... sorta, singling out the one that is a 'snack' and the ones that make up a snake - including its head.
class cube(object):
    rows = 20
    sL = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,87,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.sL // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


#Defins the snake object.
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    #Press directional keys to move the snake, it logs this.
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
        
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    #Enter the same coordinates as a cube/snack object, add length to snake
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    #Draw snake with number of cubes as in body array.
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

#Draw the grid that's between boxes by floor division to the nearest whole number. It then draws based on coordinates.
def drawGrid(sL, rows, surface):
    sizeBtwn = sL // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0),(x,sL))
        pygame.draw.line(surface, (255,255,255), (0,y),(sL,y))
        
#Basically, keep drawing the game borad, over and over, as the player moves, new snacks are made, and the player loses and is reset to a new, random position.
def redrawWindow(surface):
    global rows, sideLength, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(sideLength,rows, surface)
    pygame.display.update()

#Defining the proccess by which a new 'snack' is deployed onto the field after the last one was eaten.
def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

#Defining the the content box that will display the losing message
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    #sideLength determines dimensions of window, rows determins number of... rows.
    global sideLength, rows, s, snack
    sideLength = 500
    #width = 500
    #height = 500
    #Rows need to divide down evenly from sideLength, or it looks weird and the play doesn't work.
    rows = 20
    #The Window is a pygame display set to x, y length and height
    win = pygame.display.set_mode((sideLength, sideLength))
    pygame.display.set_caption('Coen Snake Game')
    #Snake is a thing, as is snack, and a flag is made the default that the system is based on.
    #While it's true, the loop of - play game, lose, play game - will continue until the Close Tab button on the top rigth is clicked.
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(112,128,144))
    flag = True
    #Creates a clock for the game to operate on.
    clock = pygame.time.Clock()
    while flag:
        #Game is on a delay, based on the clock, moving at 8FPS, the snake moves.
        pygame.time.delay(50)
        clock.tick(8)
        s.move()
        #Snake moves ont cube, gets additional cube to its length, cube is added to random place on surface.
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(112,128,144))
        #Snake moves onto a space that contains a portion of its body, it loses. The score is displayed in a consol that was opened at the start.
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break
        redrawWindow(win)
main()
