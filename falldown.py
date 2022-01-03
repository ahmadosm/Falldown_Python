import pygame
import sys
import random

#Ahmad Osman
#Copyrights all reserved to Ahmadosm_projects
#Further inquiries ahmadosmwork@gmail.com

# Initalizes screen, clock and font
from pygame.locals import *
pygame.font.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

# Initialize pygame font
smallFont = pygame.font.Font(None, 25)
sentenceFont = pygame.font.Font(None, 50)
bigFont = pygame.font.Font(None, 100)
mediumFont = pygame.font.Font(None, 75)

class ballSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.position = position
        self.k_left = self.k_right = 0
        # make sure the initial sprite has a rect so the collision detection works
        self.rect = self.image.get_rect()
    def update(self, speed_limitation, collisions, wallSpeed):  
        x, y = self.position
        
        if len(collisions) != 0:
            # if there's something in the collisions list, it's getting hit by a wall
            # The collision detection is a bit slow, so the ball will fall through the platform without this
            bottom = self.rect.bottom - 15
            # if the ball is trying to go out the left side of the screen, push it back. also, since there's a collision,
            # the ball has to be pushed up as well
            if x <= 10:
                x = 20
                y -= 3
            if x >= 1014:
                x = 1004
                y -= 3
            # if the y value of the bottom of the ball is greater than the y value of the top of the platform
            # this means the ball is INSIDE the platform
            if bottom > collisions[0].rect.top:
                # the total is equal to the x value of the rightmost part of the ball minus the x value of the leftmost part
                # of the platform. the absolute value is then taken of the answer
                total = self.rect.right - collisions[0].rect.left
                total = abs(total)
                # when the ball is coming from the right, the absolute value of the difference of the total is large, so
                if total > 20:
                    # ball coming from the right
                    x += 25
                else:
                    # ball coming from left
                    x -= 25
            # if the ball is NOT caught inside the platform
            else:
                # ball gets pushed up with the platform
                y -= wallSpeed
                
        elif y >= 740: 
        	# if the ball gets to the bottom of the screen
        	pass
        	
        elif x <= 10:
        	# so the ball can't go off the side of the screen (no y movement because no collision)
            x = 20
        elif x >= 1014:
            x = 994
            
        # gravity    
        else: y += 5
            
        # If the ball reaches the top of the screen, thou loseth
        if y <= 0: gameOver = 1
            
        # if no collisions are happening, and the ball isn't trying to escape off the side of the screen
        else:
            # x is changed depending on whether or not user presses left key or right key
            x += self.k_right
            x -= self.k_left
            self.position = (x, y)
            self.rect.center = self.position
            gameOver = 0
        return gameOver
        
class wallSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.position = position
        self.rect = self.image.get_rect()
    def update(self, speed_limitation, wallSpeed):
        x, y = self.position
        y -= wallSpeed
        # if wall reaches the top of the screen, kill it
        if y < -40: 
            self = self.kill
        else:
            self.position = (x, y)
            self.rect.center = (self.position)
        
        
# Adds walls to the screen at random. There are usually 2 gaps in the line of walls, and occasionally 1, 3 or 4      
def wallAdd():
    gap = random.randint(1,8)
    if gap == 1: wallList = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    elif gap == 2: wallList = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    elif gap == 3: wallList = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    elif gap == 4: wallList = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    elif gap == 5: wallList = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    else: wallList = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    random.shuffle(wallList)
    rect = pygame.Rect(0, 0, 85, 1538)
    for x in wallList:
        if x == 1: 
            wall = wallSprite('wall.png', rect.center)
            wall_group.add(wall)
            rect.width += 170
        else: 
            rect.width += 170

# Create the ball, with ball.png as the image for the sprite, and at the top-center of the screen      

def menuScreen(startGame):
    # The Title screen
    if startOver != 1:
        initialize = 1
        
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RETURN: 
            startGame = 1 
            initialize = 0
        if event.key == K_ESCAPE: sys.exit()
    
    title = pygame.font.Font.render(bigFont, "Falldown", 1, (255,255,255), (0,0,0))  
    screen.blit(title, (300,200))
    begin = pygame.font.Font.render(sentenceFont, "Press Return to begin", 1, (255,255,255), (0,0,0)) 
    screen.blit(begin, (285, 400))
    version = pygame.font.Font.render(smallFont, "Version 0.2", 1, (255,255,255), (0,0,0))  
    screen.blit(version, (400, 670))
    programmer = pygame.font.Font.render(smallFont, "Programmed by Allan Lavell", 1, (255,255,255), (0,0,0))  
    screen.blit(programmer, (330, 700))
    pygame.display.flip() 
        
    return startGame, initialize

def gameOverScreen(score, keypress):
    screen.fill((0,0,0))
    highScoreFile = open("highscore.txt", 'r')
    highScore = highScoreFile.readline()
    highScore = int(highScore)
    startOver = 0
    initialize = 0 
        
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        if highScore < score:
            highScoreFile.close()
            highScoreFile = open("highscore.txt", 'w')
            scoreString = str(score)
            highScoreFile.write(scoreString)
        down = event.type == KEYDOWN
        if event.key == K_ESCAPE: 
            # This is here because when the user presses ESC to exit the main game, it sends him to this screen
            # The user is sent here faster than they can stop holding the escape key, so unless there's some sort of mechanism
            # in place, then the game is exited as soon as it gets to this screen. The keypress system stops that.
            if keypress > 1: pass
            else: sys.exit()
        if event.key == K_RETURN:
            # To continue the game... 
            startOver = 1
            initialize = 1

    # If the player's score beats the recorded high score, display this text
    if highScore < score:
        newScore = pygame.font.Font.render(mediumFont, "New High Score!", 1, (255,255,255), (0,0,0)) 
        screen.blit(newScore, (260,120))
        previousScore = pygame.font.Font.render(sentenceFont, "Previous High Score: %s" %(highScore), 1, (255,255,255), (0,0,0)) 
        screen.blit(previousScore, (260, 185))
    else:
        highScoreDisplay = pygame.font.Font.render(sentenceFont, "High Score: %s" %(highScore), 1, (255,255,255), (0,0,0)) 
        screen.blit(highScoreDisplay, (330, 185))
    yourScore = pygame.font.Font.render(bigFont, "Your score: %i" %(score), 1, (255,255,255), (0,0,0))  
    returnToExit = pygame.font.Font.render(sentenceFont, "Press Return to play again, or Escape to quit", 1, (255,255,255), (0,0,0))  
    screen.blit(yourScore, (250,270))
    screen.blit(returnToExit, (120, 400))
    pygame.display.flip()
    keypress -= 1
    return keypress, startOver, initialize
    

def mainGame(wallNow, score, speedUp, wallTiming, gameOver, escGameOver):
    # Sets Frames per second to x
    fps = 60
    speed_limitation = clock.tick(fps)
    
    for event in pygame.event.get():
        # If the event is not a keypress, don't do anything
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        # If right arrow is pressed, make the ball go x spaces right, same thing with left
        if event.key == K_RIGHT: ball.k_right = down * 10
        elif event.key == K_LEFT: ball.k_left = down * 10
        # If ESC pressed, exit game
        elif event.key == K_ESCAPE: escGameOver = 1
            
    # makes it so that the walls appear every x frame
    wallNow += 1 
    if wallNow == wallTiming:
        score +=  10 
        wallAdd()
        rect = pygame.Rect(0, 0, 85, 1538)
    if wallNow == wallTiming * 2:
        score +=  10  
        wallAdd()
        speedUp += 1
        wallNow = 0
           
    # Every x sets of walls, walls are created more quickly  
    if speedUp == 15:
        # So that the walls can't get too crazy
        if wallTiming >= 18: wallTiming -= 2
        else: pass
        speedUp = 0
            
    screen.fill((0,0,0))
        
    # check for collisions, use this variable for more accurate collision checking as well
    collisions = pygame.sprite.spritecollide(ball, wall_group, 0)
    # Gets value for stop from ball.update to prevent the user from moving if caught by platform
    gameOver= ball.update(speed_limitation, collisions, wallSpeed)
    ball_group.draw(screen)
    wall_group.update(speed_limitation, wallSpeed)
    wall_group.draw(screen)
    pygame.display.flip()
    return wallNow, score, speedUp, wallTiming, gameOver, escGameOver

# Make sure the base variables initialize, but doesn't think it has to start over (that comes later)
initialize = 1
startOver = 0

while 1:
    if initialize == 1:
        startGame = 0
        
        if startOver == 1:
            ball_group = ball_group.empty()
            wall_group = wall_group.empty()
            screen.fill((0,0,0))
            startGame = 1
            
        origBallPos = pygame.Rect(0, 0, 512, 40)
        ball = ballSprite('ball.png', origBallPos.center)
        ball_group = pygame.sprite.RenderPlain(ball)
        
        # Initialize wall group
        wall_group = pygame.sprite.RenderPlain()
        
        # Set up some default variables for the main game loop
        wallNow = 0
        score = 0
        speedUp = 0
        wallSpeed = 5
        gameOver = 0
        escGameOver = 0
        wallTiming = 36
        keypress = 50
            
        startOver = 0
        initialize = 0
            
    if startGame == 0:
        startGame, initialize = menuScreen(startGame)
    
    elif gameOver == 1 or escGameOver == 1: 
        keypress, startOver, initialize = gameOverScreen(score, keypress)
    
    #elif gameOver == 0 and startGame == 1: 
    else:
        wallNow, score, speedUp, wallTiming, gameOver, escGameOver = mainGame(wallNow, score, speedUp, wallTiming, gameOver, escGameOver)
            
