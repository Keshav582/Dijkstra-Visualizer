import pygame, sys
from collections import deque
from tkinter import messagebox, Tk
from PyQt5 import QtWidgets, uic

size = (width, height) = 800, 800

cols, rows = 50, 50

w = width//cols
h = height//rows

grid = []
queue, visited = deque(), []
path = []


class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, col, (self.x*w+w//2, self.y*h+h//2), w//3)
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)
  

def run_visualizer(start_x, start_y, end_x, end_y):

    pygame.init()

    win = pygame.display.set_mode(size)
    pygame.display.set_caption("Dijkstra's Algorithm")

    start = grid[start_x][start_y]
    end = grid[end_x][end_y]
    start.wall = False
    end.wall = False

    queue.append(start)
    start.visited = True
    
    flag = False
    noflag = True
    startflag = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  
                   if event.button in (1, 3): 
                      clickWall(pygame.mouse.get_pos(), event.button==1)
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:  
                    clickWall(pygame.mouse.get_pos(), event.buttons[0]) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (44, 62, 80))
                if spot in path:
                    spot.show(win, (192, 57, 43))
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))
                
                
        pygame.display.flip()


def checkValues():
    flag = True
    try:
        start_x = int(call.lineEdit.text())
        start_y = int(call.lineEdit_2.text())
        end_x = int(call.lineEdit_3.text())
        end_y = int(call.lineEdit_4.text())
    except:
        flag = False
    
    if start_x>=1 and start_x<=50 and start_y>=1 and start_y<=50:
        if end_x>=1 and end_x<=50 and end_y>=1 and end_y<=50 and flag:
            run_visualizer(start_x-1, start_y-1, end_x-1, end_y-1)
    else:
        Tk().wm_withdraw()
        messagebox.showinfo("Invalid Input", "Please Enter Valid Input!")


app = QtWidgets.QApplication([])
call = uic.loadUi("form_design.ui")

call.Proceed.clicked.connect(checkValues)

call.show()
app.exec()