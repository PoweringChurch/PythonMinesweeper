import random
from pygame import Vector2

class Cell:
    def __init__(self, value:int):
        self.Value = value
        self.Revealed = False
        self.Flagged = False
    
    def Reveal(self):
        self.Revealed = True    
class Board:
    def __init__(self, width, length, minecount, seed = random.randint(0,9999999)):
        self.Size = Vector2(width,length)
        self.Minecount = minecount
        self.Seed = seed
        self.Cellmap = {}
    def Reveal(self, cellCoord:Vector2):
        x = cellCoord.x
        y = cellCoord.y
        if x < 0 or x >= self.Size.y or y < 0 or y >= self.Size.x:
            print('out of bounds')
            return
        cell = self.Cellmap[x][y]
        if cell.Flagged:
            print('flagged')
            return
        cell.Revealed = True
        if cell.Value != 0:
            return
        for offset in neighborsMatrix:
            cx = int(x + offset.x)
            cy = int(y + offset.y)
            if cx < 0 or cx >= self.Size.y or cy < 0 or cy >= self.Size.x:
                 continue
            neighborCell = self.Cellmap[cx][cy]
            if neighborCell.Revealed == True:
                continue
            self.Reveal(Vector2(cx,cy))
    def Flag(self,cellCoord:Vector2):
        x = cellCoord.x
        y = cellCoord.y
        if x < 0 or x >= self.Size.y or y < 0 or y >= self.Size.x:
            print('out of bounds')
            return
        cell = self.Cellmap[x][y]
        if cell.Flagged:
            cell.Flagged = False
        else:
            cell.Flagged = True
    def RevealBoard(self):
        for x in range(int(self.Size.y)):
            for y in range(int(self.Size.x)):
                cell = self.Cellmap[x][y]
                if not cell.Revealed:
                    cell.Revealed = True
    def VictoryCheck(self):
        safecells = (self.Size.x*self.Size.y)-self.Minecount
        revealedsafes = 0
        revealedMine = False
        for x in range(int(self.Size.y)):
            for y in range(int(self.Size.x)):
                if self.Cellmap[x][y].Revealed and self.Cellmap[x][y].Value < 9:
                    revealedsafes+=1
                elif self.Cellmap[x][y].Revealed and self.Cellmap[x][y].Value == 9:
                    revealedMine = True
        if revealedsafes == safecells and not revealedMine:
            return True
        return False
neighborsMatrix = [
    Vector2(-1,1), Vector2(0,1), Vector2(1,1),
    Vector2(-1,0),               Vector2(1,0),
    Vector2(-1,-1), Vector2(0,-1), Vector2(1,-1)
]

def GenClassicCellmap(board:Board,exclude:Vector2 = None):
    if int(board.Size.x*board.Size.y) < board.Minecount:
        print("err: minecount greater than board space")
        return {}
    
    random.seed(board.Seed)
    classic = {}
    positions = [(x, y) for x in range(int(board.Size.y)) for y in range(int(board.Size.x))]
    mine_positions = set(random.sample(positions, board.Minecount))

    for x in range(int(board.Size.y)):
        classic[x] = {}
        for y in range(int(board.Size.x)):
            cellValue = 9 if (x, y) in mine_positions else 0
            newCell = Cell(cellValue)
            classic[x][y] = newCell
    for x in range(int(board.Size.y)):
        for y in range(int(board.Size.x)):
            if classic[x][y].Value == 9:
                for offset in neighborsMatrix:
                    cx = int(x + offset.x)
                    cy = int(y + offset.y)
                    if cx < 0 or cx >= board.Size.y or cy < 0 or cy >= board.Size.x:
                        continue
                    if classic[cx][cy].Value == 9:
                        continue
                    classic[cx][cy].Value += 1
    
    return classic

def printBoard(board: Board):
    print(f"Seed: {board.Seed}  Dimensions: {int(board.Size.x)}x{int(board.Size.y)}  Minecount: {board.Minecount}")
    for y in range(int(board.Size.y)):
        newline = ""
        for x in range(int(board.Size.x)):
            cell = board.Cellmap[y][x]
            cellDisplay = str(cell.Value)
            if not cell.Revealed:
                cellDisplay = "#"
            newline += cellDisplay + " "
        print(newline)