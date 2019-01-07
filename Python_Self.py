import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color  
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)
        
    def draw(self, surface, eyes=False):
        dis = self.w//self.rows
        i = self.pos[0]
        j = self.pos[1]                         #  left  top  right, bottem
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2,dis-2))
        
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)        
    
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)    #
        self.dirnx = 0
        self.dirny = 1
        
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
        #loop through body with enumerate
        for i, node in enumerate(self.body):
            position_value = node.pos[:]
            print(position_value)
            if position_value in self.turns:
                turns = self.turns[position_value]
                print(turns)
                node.move(turns[0],turns[1])
                if i ==len(self.body)-1:
                    self.turns.pop(position_value)
            else:
                if node.pos[0] >= node.rows-1 and node.dirnx == 1: 
                    node.pos = (0,node.pos[1])
                elif node.dirnx == -1 and node.pos[0]<= 0:
                    node.pos = (node.rows-1,node.pos[1])
                elif node.dirny == 1 and node.pos[1]>=node.rows-1:
                    node.pos = (node.pos[0], 0)
                elif node.dirny == -1 and node.pos[1]<=0:
                    node.pos = (node.pos[0],node.rows-1)
                else:
                    node.move(node.dirnx,node.dirny)
                    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    def addCube(self):
        #select last node
        tail = self.body[-1]
        #takes x and y directions of new node
        dx, dy = tail.dirnx, tail.dirny
        #check direction of last node and add it to direction opposite of it depending on position
        #note* only appends the new cubes but does not move them
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))        
        #changes direction of the new tail so its not static
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy        
        
    def draw(self,surface):
        for i, node in enumerate(self.body):
            #draws eyes onto the first node
            if i == 0:
                node.draw(surface,True) #Bool for if draw eyes, part of cube class 
            else:
                node.draw(surface)
def message_box(subject,content):
    root=tk.Tk()
    #sets to topmost priority in view
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    #dont know what this does
    try:
        root.destroy()
    except:
        pass
    
        

def drawGrid(w, rows, surface):
    #size between lines
    sizeBtwn = w//rows
    x = 0
    y = 0
    for i in range(rows):
        y = y+sizeBtwn 
        x = x+sizeBtwn
        #draw line from point 1 to point 2, x locations for both points are same
        pygame.draw.line(surface, (255,255,255),(x,0),(x,w))
        pygame.draw.line(surface, (255,255,255),(0,y),(w,y))
        

 #surface = win; display size
def redrawWindow(surface):
    global width, rows, s, snack
    
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()
    
def randomSnack(rows, item):

    #item is snake object
    positions = item.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #checks if generated snack is on snake, checks (x,y) against positions
        #filter is used to find all that satisfy the lambda (if the generated snack is in the sam position as the snake)
        if len(list(filter(lambda z:z.pos ==(x,y), positions)))>0:
            continue
        else:
            break
    return (x,y)
            
 

def main():
    #s = snake
    global width, rows,s, snack
    width = 500
    rows = 20
    #window size set
    win = pygame.display.set_mode((width,width))
    
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color = (0,255,0))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()   #check if key has been pressed then move accordingly
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0,255,0))
            
        
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')   #params = subject, message
                #takes x and y starting positions in reset
                s.reset((10,10))
                break        
        redrawWindow(win)
    
main()
    