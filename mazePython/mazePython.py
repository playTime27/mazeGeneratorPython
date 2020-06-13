import random
from os import system
EAST = "east"
SOUTH = "south"
NORTH = "north"
WEST = "west"
START = "\u25CB"
END = "\u25A9"
class Cell:
    def __init__(self, row,col):
        self.row=row
        self.col=col
        self.links = {}
        self.adjacent = {'north':[self.row-1,self.col],'east':[self.row,self.col+1],'south':[self.row+1,self.col],'west':[self.row,self.col-1]}
    def getCoordinates(self):
        return (self.row,self.col);
    def getAdjacent(self,direction):
        return self.adjacent[direction.lower()];
    def link(self,connectedCell,connected=True):
        self.links[connectedCell] = True;
        if ( connected ):
            connectedCell.link(self, False)
    def linked(self,connectedCell):
        if( self.links.get(connectedCell,False) == False):
            return False;
        else:
            return True;
    def neighbors(self, grid):
        self.list = [];
        self.appendNeighbor(NORTH,grid);
        self.appendNeighbor(EAST,grid);
        self.appendNeighbor(SOUTH,grid);
        self.appendNeighbor(WEST,grid);
    def appendNeighbor(self,direction,grid):
        if ( self.isAdjacent(direction, grid) ):
            self.list.append(self.getCell(direction,grid));
    def getCell(self,direction, grid):
        if (self.isAdjacent(direction,grid)):
            return grid.getCell(self.getX(direction),self.getY(direction))
        else:
            return None
    def getRandomIndex(self):
        return random.randrange(0,2);
    def getX(self, direction):
        return self.getAdjacent(direction)[0];
    def getY(self, direction):
        return self.getAdjacent(direction)[1];
    def isAdjacent(self,direction,grid):
        return grid.inBounds(self.getX(direction), self.getY(direction));
    def isDirectionAvailable(self, linkCell, direction):
        if ( self.getX(direction) == linkCell[0] and self.getY(direction) == linkCell[1]):
            return True;
        return False;
    def selectLink(self,grid):
            northCell = self.getCell(NORTH,grid);
            eastCell = self.getCell(EAST,grid);
            isNorth = (northCell != None)
            isEast = (eastCell != None)
            if (not isEast and not isNorth):
                return;
            elif (isEast != isNorth):
                if (isEast):
                    self.link(eastCell);
                else:
                    self.link(northCell);
            else:
                randomCell = self.list[self.getRandomIndex()];
                self.link(randomCell);
class Grid:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.cells = [[Cell(i,j) for j in range(cols)] for i in range(rows)]
    def inBounds(self,row,column):
        if ( row >= self.rows or column >= self.cols ):
            return False;
        if ( row < 0 or column < 0 ):
            return False;
        return True;
    def size(self):
        return self.rows * self.cols;
    def getCell(self, x, y):
        return self.cells[x][y];
    def randomCell(self):
        row = random.randrange(0,self.rows)
        col = random.randrange(0,self.cols)
        return self.cells[row][col];
    def eachCell(self,func,grid):
        for i in range(self.rows):
            for j in range(self.cols):
                if ( func == "neighbors"):
                    self.cells[i][j].neighbors(grid);
                if ( func == "selectLink"):
                    self.cells[i][j].selectLink(grid);
    def printMaze(self):
        output = "+" + "---+" * self.cols + "\n";
        for row in range(self.rows):
            top = "|"
            bottom = '+'
            for col in range(self.cols):
                cell = self.cells[row][col];
                body = "   ";
                eastCoordinates = cell.getAdjacent(EAST);
                southCoordinates = cell.getAdjacent(SOUTH);
                eastCell = self.getCell(eastCoordinates[0],eastCoordinates[1]) if self.inBounds(eastCoordinates[0],eastCoordinates[1]) else None;
                southCell = self.getCell(southCoordinates[0],southCoordinates[1]) if self.inBounds(southCoordinates[0],southCoordinates[1]) else None;
                eastBoundary = " " if cell.linked(eastCell) else "|"
                southBoundary = "   " if cell.linked(southCell) else "---"
                top = top + body + eastBoundary
                bottom = bottom + southBoundary + "+"
            output = output + top + "\n"
            output = output + bottom + "\n"
        print(output)
class IO:
    def printGreeting():
        print("Traverse the Maze!")
    def printRules():
        print("Use the w,a,s,d keys to manuever to the endpoint, to give up press q.")
        print(" w : north , a : south, d : east, a : west")
        print("The start is " + START + " and the end is " + END)
    def printQuit():
        print("Don't think you get nothing from quitting. You get guilt, anger, depression, confusion, etc..")
    def requestInput():
        return "Enter the direction you would like to go or q to quit: ";
    def printVictory():
        print("Congratulations, you won!")
class Game:
    def __init__(self,row,col):
        grid = Grid(row,col)
        grid.eachCell("neighbors", grid);
        grid.eachCell("selectLink", grid);
        grid.eachCell("links", grid);
        self.grid = grid;
    def setEndPoints(self):
        self.start = self.grid.randomCell();
        self.end = self.start;
        while(self.start == self.end):
            self.end = self.grid.randomCell();
    def getStart(self):
        return self.start.getCoordinates()
    def getPositionCell(self):
        return self.start;
    def getEnd(self):
        return self.end.getCoordinates();
    def winGame(self):
        return self.start == self.end;
    def gameLoop(self):
        direction = "z"
        while (not self.winGame() and direction != "q"):
            try:
                system('cls')
                IO.printGreeting()
                IO.printRules()
                self.printGame()
                direction = input(IO.requestInput())
                positionCell = self.getPositionCell()
                cell = None
                if( direction == "q"):
                    IO.printQuit()
                    break;
                if ( direction == "w"):
                    cell= positionCell.getCell(NORTH, self.grid)
                elif (direction == "a"):
                    cell= positionCell.getCell(WEST, self.grid)

                elif (direction == "s"):
                    cell= positionCell.getCell(SOUTH, self.grid)
                elif (direction == "d"):
                    cell= positionCell.getCell(EAST, self.grid)
                else:
                    continue;

                if( positionCell.linked(cell) ):
                        self.start=cell;
            except Exception as e:
                print("Invalid input. Error : " + e)
        if(self.winGame()):
            IO.printVictory()

    def printGame(self):
        start = self.getStart()
        end = self.getEnd()
        output = "+" + "---+" * self.grid.cols + "\n";
        for row in range(self.grid.rows):
            top = "|"
            bottom = '+'
            for col in range(self.grid.cols):
                cell = self.grid.cells[row][col];
                char = START if (row == start[0] and col == start[1]) else " "
                if ( char != START ):
                    char = END if (row == end[0] and col == end[1]) else " "
                body = " " + char + " ";
                eastCoordinates = cell.getAdjacent(EAST);
                southCoordinates = cell.getAdjacent(SOUTH);
                eastCell = self.grid.getCell(eastCoordinates[0],eastCoordinates[1]) if self.grid.inBounds(eastCoordinates[0],eastCoordinates[1]) else None;
                southCell = self.grid.getCell(southCoordinates[0],southCoordinates[1]) if self.grid.inBounds(southCoordinates[0],southCoordinates[1]) else None;
                eastBoundary = " " if cell.linked(eastCell) else "|"
                southBoundary = "   " if cell.linked(southCell) else "---"
                top = top + body + eastBoundary
                bottom = bottom + southBoundary + "+"
            output = output + top + "\n"
            output = output + bottom + "\n"
        print(output)
game = Game(10,10)
game.setEndPoints()
game.gameLoop()
