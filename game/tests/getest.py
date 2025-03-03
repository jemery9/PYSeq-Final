# getests.py

import sys
sys.path.insert(0, './../')

import gameengine
from gameengine import *



surface = pygame.display.set_mode((480,300), pygame.DOUBLEBUF | pygame.RESIZABLE)
#gameEngine = GameEngine(surface)
#gameEngine.startLevel(1)
gameEngine = GameEngine.getInstance()
gameEngine.init(surface)
gameEngine.startLevel(1)



FPS = 60
frames = FPS / 12

black = Color('black')
clock = pygame.time.Clock()



#player = Player(board)
#player.character.move(Direction.EAST, 2)
#player.character.move(Direction.SOUTH, 100)
#print(player.character.position)


commands = [
    # Go back to 0,0
    Command(Direction.EAST, 2),
    Command(Direction.SOUTH, 1),
    Command(Direction.NORTH, 1),
    Command(Direction.WEST, 2)
]
commandQueue = CommandQueue(commands)
#gameEngine.player.runCommand(commandQueue)
#print(player.character.position)


levelConfig = LevelConfig.loadFile("level1.txt")


while True:
    for e in pygame.event.get():
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                sys.exit()
        
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            commandQueue = CommandQueue( [Command(Direction.NORTH, 1)] )
            gameEngine.player.runCommand(commandQueue)    

        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            commandQueue = CommandQueue( [Command(Direction.SOUTH, 1)] )
            gameEngine.player.runCommand(commandQueue)

        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            commandQueue = CommandQueue( [Command(Direction.EAST, 1)] )
            gameEngine.player.runCommand(commandQueue)      
        
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            commandQueue = CommandQueue( [Command(Direction.WEST, 1)] )
            gameEngine.player.runCommand(commandQueue)                        

        # Turn directions
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DELETE:
            commandQueue = CommandQueue( [Command(Direction.WEST, 0)] )
            gameEngine.player.runCommand(commandQueue)    

        if e.type == pygame.KEYDOWN and e.key == pygame.K_PAGEDOWN:
            commandQueue = CommandQueue( [Command(Direction.EAST, 0)] )
            gameEngine.player.runCommand(commandQueue)    

        if e.type == pygame.KEYDOWN and e.key == pygame.K_HOME:
            commandQueue = CommandQueue( [Command(Direction.NORTH, 0)] )
            gameEngine.player.runCommand(commandQueue)    

        if e.type == pygame.KEYDOWN and e.key == pygame.K_END:
            commandQueue = CommandQueue( [Command(Direction.SOUTH, 0)] )
            gameEngine.player.runCommand(commandQueue)                

    surface.fill(black)
    gameEngine.tick()

    pygame.display.flip()
    clock.tick(FPS) 