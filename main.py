'''
Created on Jul 5, 2016

@author: Kyle
'''

import pygame, gui, random

#Colors
WHITE = pygame.Color(255, 255, 255, 255)
BLACK = pygame.Color(30, 30, 30, 255)
BLUE = pygame.Color(33, 150, 243, 255)
LIGHT_BLUE = pygame.Color(144, 202, 249, 255)
RED = pygame.Color(244, 67, 54, 255)
LIGHT_RED = pygame.Color(239, 154, 154, 255)

class Boat(object):
    '''
    A boat entity, a point with rotation and size.
    '''
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.rotation = 1
        self.size = size
    
    '''
    Sets the transformation on the boat
    '''
    def setTransform(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
    
    '''
    Rotates the boat counter-clockwise
    '''
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
    
    '''
    Gets all potential boat cell positions (These can be out of  bounds)
    '''
    def getCellPositions(self):
        cells = []
        
        #Up
        if self.rotation == 0:
            for delta in range(self.size):
                cells.append((self.x, self.y - delta))
        #Right
        elif self.rotation == 1:
            for delta in range(self.size):
                cells.append((self.x + delta, self.y))
        #Down
        elif self.rotation == 2:
            for delta in range(self.size):
                cells.append((self.x, self.y + delta))
        #Left
        elif self.rotation == 3:
            for delta in range(self.size):
                cells.append((self.x - delta, self.y))
        
        return cells

class Cell(object):
    '''
    Storage for a single cell's data
    '''
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.boatPresent = False
        self.shot = False
    
    '''
    Returns the color of this cell if a boat is present, otherwise white
    '''
    def getColor(self):
        return self.color if self.boatPresent else WHITE

class Grid(object):
    '''
    Storage for a player's grid, contains 100 cells
    '''
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.array = [[Cell(cellx, celly, color) for cellx in range(10)] for celly in range(10)]
    
    '''
    Gets a cell at the given position
    If it is out of bounds, none is returned
    
    returns: cell at specified position
    '''
    def getCell(self, x, y):
        return self.array[y][x] if -1 < x < 10 and -1 < y < 10 else None
    
    '''
    Get all cells that fit a specification
    
    boat: if the cell is occupied by a boat
    shot: if the cell has been shot at by the enemy
    
    returns: array of cell objects
    '''
    def getCells(self, boat, shot):
        array = []
        for y in range(10):
            for x in range(10):
                cell = self.array[y][x]
                if (boat != None and cell.boatPresent == boat) and(shot != None and cell.shot == shot):
                    array.append(cell)
        return array
    
    
    '''
    Get all free cells based on a boat object,
    Free cells are in bounds, and not occupied by a boat
    
    returns: array of cell objects
    '''
    def getFreeBoatCells(self, boat):
        array = []
        for cellpos in boat.getCellPositions():
            cell = self.getCell(cellpos[0], cellpos[1])
            if cell is not None and not cell.boatPresent:
                array.append(cell)
        return array
    
    '''
    Attempts to place a boat.
    
    returns: whether placing the boat was successful
    '''
    def tryPlacingBoat(self, boat):
        cells = self.getFreeBoatCells(boat)
        #Only place if all cells are free
        if len(cells) == boat.size:
            for cell in cells:
                cell.boatPresent = True
            return True
        return False
    
    '''
    Get whether or not a cursor is within the grid
    '''
    def mouseInGrid(self, x, y):
        return self.x < x < self.x + 250 and self.y < y < self.y + 250
    
    '''
    Converts a mouse coordinate to a cell position
    returns: Cell position
    '''
    def mouseCellPos(self, x, y):
        return (int((x - self.x) / 25), int((y - self.y) / 25))
    
    '''
    Renders all cells within the grid
    
    onlyShowShot: whether or not to only show cells that have been shot
    '''
    def render(self, surface, onlyShowShot):
        if onlyShowShot:
            for y in range(10):
                for x in range(10):
                    cell = self.array[y][x]
                    #Calculate cell position
                    rect = pygame.Rect(self.x + (cell.x * 25), self.y + (cell.y * 25), 25, 25)
                    
                    #Render ship only if it was shot at
                    if cell.shot:
                        pygame.draw.rect(window, cell.getColor(), rect)
                        window.blit(shotMarker, rect.topleft)
                    #Otherwise draw a white square
                    else:
                        pygame.draw.rect(window, WHITE, rect)
                    
                    #Grid outlines
                    pygame.draw.rect(window, BLACK, rect, 1)
        else:
            for y in range(10):
                for x in range(10):
                    cell = self.array[y][x]
                    #Calculate cell position
                    rect = pygame.Rect(self.x + (cell.x * 25), self.y + (cell.y * 25), 25, 25)
                    
                    #Draw ships and x if cell was shot
                    pygame.draw.rect(window, cell.getColor(), rect)
                    if cell.shot:
                        window.blit(shotMarker, rect.topleft)
                    
                    #Grid outlines
                    pygame.draw.rect(window, BLACK, rect, 1)
        
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, 250, 250), 3)
    
    
    '''
    Renders a blank white square within the grids place
    '''
    def renderBlank(self, surface):
        pygame.draw.rect(window, WHITE, pygame.Rect(self.x, self.y, 250, 250))
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, 250, 250), 3)

#Initialize pygame
pygame.display.init()
pygame.font.init()

#Create window
pygame.display.set_caption("Battle Ship")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

window = pygame.display.set_mode((270, 580))

font = pygame.font.SysFont("Segoe UI", 25)

#UI elements
title = pygame.image.load("assets/title.png")
#Main Menu elements
startBotButton = gui.TextButton(font, "Battle against the CPU", RED, LIGHT_RED, pygame.Rect(10, 350, 250, 40))
startPlayerButton = gui.TextButton(font, "Battle against a friend", RED, LIGHT_RED, pygame.Rect(10, 400, 250, 40))
exitButton = gui.TextButton(font, "Exit", BLUE, LIGHT_BLUE, pygame.Rect(10, 450, 250, 40))
#Placing & Playing elements
beginTurnButton = gui.TextButton(font, "Begin", BLUE, LIGHT_BLUE, pygame.Rect(180, 270, 80, 40))
endTurnButton = gui.TextButton(font, "End", RED, LIGHT_RED, pygame.Rect(180, 270, 80, 40))
turnText = gui.AlignedLabel(font, "Player 1's Turn", True, BLUE, 0, (10, 290))
shotMarker = pygame.image.load("assets/shot.png")
#End Game elements
winText = gui.AlignedLabel(font, "", True, WHITE, 1, (145, 350))
returnButton = gui.TextButton(font, "Return to main menu", BLUE, LIGHT_BLUE, pygame.Rect(10, 400, 250, 40))

#Grids store all cell data
grid1 = Grid(10, 10, BLUE)
grid2 = Grid(10, 320, RED)

#Gameplay variables
singleplayer = False
hidden = False

#Current state
action = 0
turn = 0
stage = 0

#Boat placement variables
boatSizes = [5, 3, 2, 2]
boatIndex = 0
currentBoat = Boat(boatSizes[0])

'''
Increases the action state (Begin turn, Select cell, End turn)
If single player, this performs a mostly random action
33% of the time, it cheats and only selects from cells it knows a boat is
These are performed this method to bypass the begin and end states
'''
def advanceAction():
    global action, stage, singleplayer
    if singleplayer:
        if stage == 2:
            #20% of the time the cpu will cheat and only look for boats, makes it more competitive
            cells = grid1.getCells(random.randint(1, 100) <= 20, False)
            #Shoot a random free cell
            cells[random.randint(0, len(cells) - 1)].shot = True
            
            advanceTurn()
            
    else:
        action = (action + 1) % 3

'''
Changes the turn to the next player
If single player, this performs randomization for ship placement
Also transitions stage to win state once a player sinks all ships
'''
def advanceTurn():
    global action, turn, stage, singleplayer, grid2, turnText
    
    if singleplayer:
        if stage == 1:
            boat = Boat(0)
            for size in boatSizes:
                boat.size = size
                
                finished = False
                while not finished:
                    boat.setTransform(random.randint(0, 9), random.randint(0, 9), random.randint(0, 3))
                    if grid2.tryPlacingBoat(boat): finished = True
            
            action = 1
            advanceStage()
    else:
        #If multiplayer, change turn
        turn = (turn + 1) % 2
        turnText.setText("Player " + str(turn + 1) + "'s Turn")
        turnText.setColor(BLUE if turn == 0 else RED)
    
    if stage == 2:
        #Check if all boat cells have been shot
        if len(grid2.getCells(True, False)) == 0:
            winText.setColor(BLUE)
            if singleplayer:
                winText.setText("You win!")
            else:
                winText.setText("Player 1 wins!")
            advanceStage()
        elif len(grid1.getCells(True, False)) == 0:
            winText.setColor(RED)
            if singleplayer:
                winText.setText("CPU wins!")
            else:
                winText.setText("Player 2 wins!")
            advanceStage()

#Increments the stage by 1
def advanceStage():
    global stage
    stage = (stage + 1) % 4

#Main game loop, continues to loop until running variable is false
running = True
while running:
    events = pygame.event.get()
    
    #Clear background
    pygame.draw.rect(window, BLACK, pygame.Rect(0, 0, 270, 580))
    
    # MAIN MENU
    if stage == 0:
        for event in events:
            #Quit game if pygame called a quit event
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEMOTION:
                #Update buttons
                startBotButton.check(event.pos)
                startPlayerButton.check(event.pos)
                exitButton.check(event.pos)
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if startBotButton.check(event.pos):
                    singleplayer = True
                    advanceStage()
                elif startPlayerButton.check(event.pos):
                    advanceStage()
                elif exitButton.check(event.pos):
                    running = False
        
        #Render title and buttons
        window.blit(title, (0, 50))
        startBotButton.render(window)
        startPlayerButton.render(window)
        exitButton.render(window)
    
    # PLACING
    elif stage == 1:
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                
                #Update buttons
                endTurnButton.check(event.pos)
                beginTurnButton.check(event.pos)
                #Move boat if within either grid
                if grid1.mouseInGrid(x, y):
                    currentBoat.x, currentBoat.y = grid1.mouseCellPos(x, y)
                elif grid2.mouseInGrid(x, y):
                    currentBoat.x, currentBoat.y = grid2.mouseCellPos(x, y)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                currentBoat.rotate()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Attempt to place boat if user left clicks
                if grid1.mouseInGrid(x, y) and turn == 0 and grid1.tryPlacingBoat(currentBoat):
                    #Change to next boat
                    boatIndex += 1
                    #Change turn if finished placing all boats
                    if boatIndex == len(boatSizes):
                        boatIndex = 0
                        advanceTurn()
                    
                    currentBoat.size = boatSizes[boatIndex]
                
                elif grid2.mouseInGrid(x, y) and turn == 1 and grid2.tryPlacingBoat(currentBoat):
                    #Change to next boat
                    boatIndex += 1
                    #Change to play mode once player 2 finishes placing all boats
                    if boatIndex == len(boatSizes):
                        boatIndex = 0
                        advanceTurn()
                        hidden = True
                        advanceStage()
                    
                    currentBoat.size = boatSizes[boatIndex]
        
        turnText.render(window)
        
        x, y = pygame.mouse.get_pos()
        
        #Render only the current player's grid
        if turn == 0:
            grid1.render(window, False)
            grid2.renderBlank(window)
        else:
            grid1.renderBlank(window)
            grid2.render(window, False)
        
        #Render the potential boat positions
        if grid1.mouseInGrid(x, y) and turn == 0:
            cells = grid1.getFreeBoatCells(currentBoat)
            if len(cells) == currentBoat.size:
                color = BLUE
            else:
                color = LIGHT_BLUE
            for cell in cells:
                pygame.draw.rect(window, color, pygame.Rect(10 + (cell.x * 25), 10 + (cell.y * 25), 25, 25))
        
        elif grid2.mouseInGrid(x, y) and turn == 1:
            cells = grid2.getFreeBoatCells(currentBoat)
            if len(cells) == currentBoat.size:
                color = RED
            else:
                color = LIGHT_RED
            for cell in cells:
                pygame.draw.rect(window, color, pygame.Rect(10 + (cell.x * 25), 320 + (cell.y * 25), 25, 25))
    #PLAYING
    elif stage == 2:
        #Quit game if pygame called a quit event
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                
                if action == 0:
                    beginTurnButton.check(event.pos)
                elif action == 2:
                    endTurnButton.check(event.pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if action == 1:
                    #Shoot cell if within correct grid
                    if turn == 0 and grid2.mouseInGrid(x, y):
                        cellx, celly = grid2.mouseCellPos(x, y)
                        if not grid2.getCell(cellx, celly).shot:
                            grid2.getCell(cellx, celly).shot = True
                            advanceAction()
                    elif turn == 1 and grid1.mouseInGrid(x, y):
                        cellx, celly = grid1.mouseCellPos(x, y)
                        if not grid1.getCell(cellx, celly).shot:
                            grid1.getCell(cellx, celly).shot = True
                            advanceAction()
                    
                    endTurnButton.check((x, y))
                
                elif action == 0 and beginTurnButton.check((x, y)):
                    advanceAction()
                    hidden = False
                
                elif action == 2 and endTurnButton.check((x, y)):
                    advanceAction()
                    advanceTurn()
                    hidden = True
        
        if action == 0:
            beginTurnButton.render(window)
        elif action == 2:
            endTurnButton.render(window)
        
        turnText.render(window)
        
        if not hidden:
            if turn == 0:
                grid1.render(window, False)
                grid2.render(window, True)
            elif turn == 1:
                grid1.render(window, True)
                grid2.render(window, False)
        else:
            grid1.renderBlank(window)
            grid2.renderBlank(window)
    #WIN
    elif stage == 3:
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEMOTION:
                returnButton.check(event.pos)
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if returnButton.check(event.pos):
                    #Reset all information in case the user wants to play again after returning to menu
                    grid1 = Grid(10, 10, BLUE)
                    grid2 = Grid(10, 320, RED)
                    singleplayer = False
                    hidden = False
                    action = 0
                    turn = 0
                    stage = 0
        
        #Render title, win text, and return button
        window.blit(title, (0, 50))
        winText.render(window)
        returnButton.render(window)
    #Swaps the screen buffer
    pygame.display.flip()