import pygame, pygame.freetype, pygame.transform
import random

class rectangle:
    def __init__(self, surface, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font_size = 32
        self.surface = surface

    def draw(self, color):
        return pygame.draw.rect(self.surface, color, [self.x, self.y, self.w, self.h])
    
    def text(self, color, text):
        font = pygame.freetype.SysFont('sans', self.font_size)
        off_x = int((self.w - self.font_size) / 2)
        off_y = int((self.h - self.font_size) / 2)
        font.render_to(self.surface, (self.x + off_x , self.y + off_y), text, color)

    def picture(self, file):
        img_size = 36
        s = pygame.image.load(file)
        scaled = pygame.transform.scale(s, (img_size, img_size))
        off_x = int((self.w - img_size) / 2)
        off_y = int((self.h - img_size) / 2)
        self.surface.blit(scaled, (self.x + off_x, self.y + off_y))

class cell(rectangle):
    def __init__(self, surface, x, y, w, h, mine):
        super().__init__(surface, x, y, w, h)
        self.mine = mine
        self.nmines = 0
        self.on_call = False
    
    def draw(self, color):
        return pygame.draw.rect(self.surface, color, [self.x, self.y, self.w, self.h], 2, 2, 2, 2, 2, 2)

    def on_click(self, x, y, buttons):
        if x >= self.x and x <= (self.x + self.w) and y >= self.y and y <= (self.y + self.h):
            # mark cell by flag
            if buttons[2] == True:
                self.picture('red-flag-icon.svg')

            if buttons[0] == True:
                if self.mine == True:
                    pygame.draw.rect(self.surface, "red", [self.x, self.y, self.w, self.h])
                    pygame.draw.rect(self.surface, "white", [self.x, self.y, self.w, self.h], 2, 2, 2, 2, 2, 2)
                    return True
                else:
                    pygame.draw.rect(self.surface, "gray", [self.x, self.y, self.w, self.h])
                    pygame.draw.rect(self.surface, "white", [self.x, self.y, self.w, self.h], 2, 2, 2, 2, 2, 2)
                    
                    if self.nmines > 0:
                        self.text("black", str(self.nmines))
        
        return False

class field(rectangle):
    def __init__(self, surface, x, y, w, h, w_cells, h_cells, size_a, number_of_mines):
        self.w_cells = w_cells
        self.h_cells = h_cells
        self.size_a = size_a
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = surface
        self.fields = []

        # initialize cells
        for y in range(0, self.w_cells):
            row = []
            for x in range(0, self.h_cells):
                icell = cell(self.surface, x*size_a, y*size_a, size_a, size_a, False)
                row.append(icell)
            self.fields.append(row)
        
        # seed 10 mines on the field
        n = 0
        while(n < number_of_mines):
            x = int(random.random() * (w_cells - 1))
            y = int(random.random() * (h_cells - 1))
            if self.fields[y][x].mine == False:
                self.fields[y][x].mine = True
                n = n +1
                print('set mine at: x = ', x, ' y = ', y)

        # calculate neighbor mines for each cell
        matrix = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for y in range(0, self.w_cells):
            for x in range(0, self.h_cells):
                for t in matrix:
                    nx = x + t[0]
                    ny = y + t[1]

                    if nx < 0 or ny < 0 or nx >= self.w_cells or ny >= self.h_cells:
                        continue

                    if self.fields[ny][nx].mine:
                        self.fields[y][x].nmines += 1

    def draw(self, color):
        for y in range(0, self.w_cells):
           for x in range(0, self.h_cells):
               self.fields[y][x].draw(color)

    # draw free of mines cells around
    def show_free(self, ix, iy):
        c = self.fields[iy][ix]
        
        # don't show cell with mine
        if c.mine == True:
            return
        
        c.on_click(ix * self.size_a, iy * self.size_a, (True, True, True))

        # it's free of nearby mines cell, then check neigbors
        c.on_call = True # mark this cell that it's in progress of recursion
        matrix = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for t in matrix:
            ny = iy + t[1]
            nx = ix + t[0]
            if nx < 0 or ny < 0 or nx >= self.w_cells or ny >= self.h_cells:
                continue

            n = self.fields[ny][nx]
            if n.mine == True:
                # don't show mine to user
                continue

            if n.nmines > 0:
                # show number of near mines and continue
                n.on_click(nx * self.size_a, ny * self.size_a, (True, True, True))
                continue

            # recurse for zero nearby mines cell
            if n.on_call == False:
                self.show_free(nx, ny)
        return

    def on_click(self, x, y, buttons):
        ix = int(x / self.size_a)
        iy = int(y / self.size_a)
        ret = self.fields[iy][ix].on_click(x, y, buttons)
        print('ix = ', ix, ' iy = ', iy, 'mine = ', ret)

        # mine was found, show whole field since the game over
        if ret == True:
            for y in range(0, self.w_cells):
                for x in range(0, self.h_cells):
                    self.fields[y][x].on_click(x * self.size_a, y * self.size_a, buttons)
        else: 
            # do recursion to clean-up free of mines area            
            # clean up all cells 'on_call' flag
            for y in range(0, self.w_cells):
                for x in range(0, self.h_cells):
                    self.fields[y][x].on_call =False

            if buttons[0] == True:
                self.show_free(ix, iy)

        return ret
