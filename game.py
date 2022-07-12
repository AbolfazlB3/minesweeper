import numpy as np
import sys
import json

class Game:

    def __init__(self, w:int, h:int):
        sys.setrecursionlimit(100000000)

        self.p = 0.3
        self.w = w
        self.h = h

        self.lost = False

        self.grid = np.zeros((h, w), dtype=np.int8)
        # -1 bomb, 0 empty, 1 2 3 ... numbers

        self.grid_known = np.zeros((h, w), dtype=np.int8)
        # 0 not known, 1 known empty, 2 known number

        self.init()

        pass

    def init(self):
        for i in range(self.h):
            for j in range(self.w):
                self.grid_known[i, j] = 0
                self.grid[i, j] = -1 if np.random.random() < self.p else 0

        for i in range(self.h):
            for j in range(self.w):
                if(self.grid[i, j] != -1):
                    self.grid[i, j] = self.get_number(j, i)
    
    def dfs(self, x, y):
        if self.grid_known[y, x] != 1:
            return
        print(x, y)
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                xp, yp = x+j, y+i
                if not self.is_cell_valid(xp, yp) or \
                    (xp==x and yp==y) or \
                    self.grid_known[yp, xp] != 0: continue
                if self.grid[yp, xp] == 0:
                    self.grid_known[yp, xp] = 1
                    self.dfs(xp, yp)
                else:
                    self.grid_known[yp, xp] = 2

        
    def get_number(self, x:int, y:int):
        if(not self.is_cell_valid(x, y)):
            return 0
        res = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                xp, yp = x+j, y+i
                if(self.is_cell_valid(xp, yp)):
                    res += self.grid[yp, xp] == -1
        return res

    
    def reveal(self, x:int, y:int):
        if(not self.is_cell_valid(x, y)): return

        if self.grid[y, x] == 0:
            print("0")
            self.grid_known[y, x] = 1
            self.dfs(x, y)

        elif self.grid[y, x] == -1:
            
            print("1")

            self.lost = True
        
        else:

            print("2")
            self.grid_known[y, x] = 2
    

    def get_state(self):

        grid = self.grid.copy()

        if not self.lost:
            for i in range(self.h):
                for j in range(self.w):
                    if self.grid_known[i, j] == 0:
                        grid[i, j] = -2
        

        res = {
            'w': self.w,
            'h': self.h,
            'grid': grid.flatten().tolist(),
            'lost': self.lost
        }

        return res


    def is_cell_valid(self, x:int, y:int):
        return (x >= 0 and x < self.w and y >= 0 and y < self.h)
