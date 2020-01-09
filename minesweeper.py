# -*- coding: utf-8 -*-

from tkinter import *

import random
import time

class Minesweeper(object):

    def __init__(self, height, width, size, bombs):

        self.root = Tk()
        self.start_time = time.time()
        self.width = width
        self.height = height
        self.size = size
        self.bombs = bombs

        self.c = Canvas(master = self.root, width = self.width* self.size, height = self.height*self.size + self.size)
        self.c.pack()

    def run(self):

        self.board = self.create_board()

        self.bury_mines()

        self.beginning_view()

        self.c.bind("<Button-1>", self.click)

        self.root.mainloop()


    def create_board(self):
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            board.append(row)
        return board

    def bury_mines(self):
        coordinates = []
        for i in range(self.height):
            for j in range(self.width):
                coordinates.append((i,j))
        random.shuffle(coordinates)
        for y,x in coordinates[:self.bombs]:
            self.board[y][x] = -1

    def adjacent_coordinates(self, y, x):
        result = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not (i==0 and j==0):
                    if y + i >= 0 and x + j >=0 and y + i < self.height and x + j < self.width:
                       result.append((y+i, x+j))
        return result

    def get_mine_count(self,y,x):
        count = 0
        for i,j in self.adjacent_coordinates(y,x):
            if self.board[i][j] == -1:
                count += 1
        return count

    def print_board(self):
        result =""
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == -1:
                    result += "* "
                else:
                    mine_count = self.get_mine_count(i,j)
                    result += str(mine_count) + " "
            result+="\n"
        print(result)

    def uncover_board(self, y, x):
        if self.board[y][x] != None:
            return
        mine_count = self.get_mine_count(y, x)
        self.board[y][x] = mine_count
        self.user_view(y, x)
        if mine_count == 0:
            for (i,j) in self.adjacent_coordinates(y, x):
                self.uncover_board(i, j)

    def click(self, event):
        column = (event.x)// self.size
        row = (event.y - self.size) // self.size
        print("({},{})".format(row, column))

        if self.board[row][column] == -1:
            self.mine_trigger()
            return
        else:
            self.uncover_board(row, column)
            if self.test_won() == True:
#               self.c.create_rectangle(self.size )
                end_time = time.time()
                total_time = self.start_time - end_time
                self.c.create_rectangle(0, 0, self.size * self.width, self.size, fill = "black")
                self.c.create_text(self.size * self.width // 2, self.size // 2, text = ("YOU WIN! You finished in", str(int(abs(total_time))), "seconds!"), font = ("Times New Roman", self.size * self.width // 30, "bold"), fill = "white")
                return

    def beginning_view(self):
        for z in range(self.height):
            for x in range(self.width):
                    self.c.create_rectangle(self.size * x, self.size * z + self.size, self.size + self.size * x, self.size + self.size * z + self.size, fill = "pink")
                    self.c.create_text((x + 1)*self.size - (self.size / 2) ,(z + 1)*self.size - (self.size / 2), text = " ", font = ("Times New Roman", self.size))
        self.c.create_rectangle(0, 0, self.size * self.width, self.size, fill = "white")
        self.c.create_text(self.size * self.width // 2, self.size // 2, text = ("MINESWEEPER by Bernard and Albert"), font = ("Times New Roman", self.size * self.width // 25, "bold"), fill = "black")
    def user_view(self, z, x):
        if self.board[z][x] != None and self.board[z][x] >= 0:
            self.c.create_rectangle(self.size * x, self.size * z + self.size, self.size + self.size * x, self.size + self.size * z + self.size, fill = "gray")
            self.c.create_text((x + 1)*self.size - (self.size / 2) ,(z + 1)*self.size - (self.size / 2) + self.size, text = str(self.board[z][x]), font = ("Times New Roman", self.size))
        else:
            self.c.create_rectangle(self.size * x, self.size * z + self.size, self.size + self.size * x, self.size + self.size * z + self.size, fill = "pink")
            self.c.create_text((x + 1)*self.size - (self.size / 2) ,(z + 1)*self.size - (self.size / 2) + self.size, text = " ", font = ("Times New Roman", self.size))

    def test_won(self):
        for row in range(self.height):
            for cell in range(self.width):
                if self.board[row][cell] == None:
                    return False
        return True

    def mine_trigger(self):
        for z in range(self.height):
            for x in range(self.width):
                if self.board[z][x] == -1:
                    self.c.create_rectangle(self.size * x, self.size * z + self.size, self.size + self.size * x, self.size + self.size * z + self.size, fill = "red")
                    self.c.create_text((x + 1)*self.size - (self.size / 2) ,(z + 1)*self.size - (self.size / 2) + self.size, text = "X", font = ("Times New Roman", self.size))
                else:
                    self.c.create_rectangle(self.size * x, self.size * z + self.size, self.size + self.size * x, self.size + self.size * z + self.size, fill = "gray")
                    self.c.create_text((x + 1)*self.size - (self.size / 2) ,(z + 1)*self.size - (self.size / 2) + self.size, text = str(self.get_mine_count(z, x)), font = ("Times New Roman", self.size))
        self.c.create_rectangle(0, 0, self.size * self.width, self.size , fill = "black")
        self.c.create_text(self.size * self.width // 2, self.size // 2, text = "YOU LOSE HAHA SORRY ", font = ("Times New Roman", self.size * self.width // 18, "bold"), fill = "red")

#x = int(input("Enter a height: \n"))
#y = int(input("Enter a width: \n"))
#size = int(input("Enter a side length: \n"))
#bombs = int(input("How many mines do you want to plant?: \n"))
minesweeper_game = Minesweeper(8, 8, 50, 10)
minesweeper_game.run()
