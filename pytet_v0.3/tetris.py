from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
		
    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
	self.state = TetrisState.NewBlock	
	self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
	self.top = 0
        return

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self): # To be implemented!!
        range_c = self.currBlk.get_dy()

        if self.top + self.currBlk.get_dy() >= self.iScreenDy:
            range_c = self.iScreenDy - self.top

        remove = 0
        arrayScreen = self.createArrayScreen()
        nScreen = Matrix(arrayScreen)
        blankLine = nScreen.clip(0, 0, 1, nScreen.get_dx())

        for i in range(range_c - 1, -1, -1):
            check = self.top + i + remove
            line = self.oScreen.clip(check, 0, check + 1, self.oScreen.get_dx())
            if line.sum() == self.oScreen.get_dx():
                temp = self.oScreen.clip(0, 0, check, self.oScreen.get_dx())
                self.oScreen.paste(temp, 1, 0)
                self.oScreen.paste(blankLine, 0, 0)
                remove += 1

        return self.oScreen

    def accept(self, key): # To be implemented!!
        if self.state == TetrisState.NewBlock:
            self.idxBlockType = int(key)

        self.state = TetrisState.Running

        if key == 'a':
            self.left -= 1
        elif key == 'd':
            self.left += 1
        elif key == 's':
            self.top += 1
        elif key == 'w':
            self.idxBlockDegree = (self.idxBlockDegree + 1) % Tetris.nBlockDegrees
        elif key == ' ':
            while not self.tempBlk.anyGreaterThan(1):
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
                self.tempBlk = self.tempBlk + self.currBlk
        else:
            printf("Wrong key!!!")

        self.currBlk = Matrix(Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree])
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):
            if key == 'a':
                self.left += 1
            elif key == 'd':
                self.left -= 1
            elif key == 's':
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w':
                self.idxBlockDegree = (self.idxBlockDegree - 1) % Tetris.nBlockDegrees
            elif key == ' ':
                self.top -= 1
                self.state = TetrisState.NewBlock

            self.currBlk = Matrix(Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree])
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk

            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)

            if self.state == TetrisState.NewBlock:
                self.oScreen = self.deleteFullLines()
                self.iScreen = Matrix(self.oScreen)
                self.top = 0
                self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
                self.idxBlockDegree = 0

            if self.tempBlk.anyGreaterThan(1):
                self.state = TetrisState.Finished
                self.oScreen = Matrix(self.iScreen)

            return self.state

### end of class Tetris():
    
