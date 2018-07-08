"""
Created on Fri Junly 05 14:20:05 2018
@author: Md Rashad Al Hasan Rony
"""

import pygame
import random

class Breakout():
       
    def build_wall(self, width):
        
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

        # padding of walls from the top screen
        xpos = 0
        ypos = 30
        adj = 0
        
        #collection of all the bricks
        self.brickrect = []
        
        # generating bricks
        for i in range (0, 65): 
            
            #If the brick corossed the screen width
            if xpos > width:
                if adj == 0:
                    xpos = -(self.bricklength / 2)
                    xpos = 0
                    
                ypos += self.brickheight  # moving to next row
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength
            
            
    
    def fuzzy_paddle_controller(self,h,w,ballrect,paddlerect,xspeed): #TASK
        if(ballrect.bottom < (h/2)):
            paddlerect = paddlerect.move(xspeed+0.3, 0)
        elif (ballrect.bottom > (h/2)):
            paddlerect = paddlerect.move(xspeed,0)
        else:
            paddlerect = paddlerect.move(xspeed,0)
            
        if (paddlerect.left < 0):                          
                paddlerect.left = 0
        if (paddlerect.right > w):                            
                paddlerect.right = w
        return paddlerect                 
   
    def play(self):
          
        xspeed_init = 6
        yspeed_init = 6
        max_lives = 7
        score = 0 
        
        #Color initialization
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        RED = (255,0,0)
        
        #screen height and width
        WIDTH = 640
        HEIGHT = 480

        pygame.init()            
        screen = pygame.display.set_mode((WIDTH,HEIGHT))


        #Load paddle and ball
        paddle = pygame.image.load("bar.png").convert()
        paddlerect = paddle.get_rect()

        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey(WHITE)
        ballrect = ball.get_rect()
       
        
        #Build wall for the game
        self.build_wall(WIDTH)
        

        # Initialise ready for game loop
        paddlerect = paddlerect.move((WIDTH / 2) - (paddlerect.right / 2), HEIGHT - 12) # initially moving paddle to center
        ballrect = ballrect.move(WIDTH / 2, HEIGHT / 2)       
        xspeed = xspeed_init
        yspeed = yspeed_init
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)  # if keys are hold down paddle  will move repeatedly
        
        gameOver = False

        while not gameOver:
            yspeed+=0.1
            
            # 60 frames per second
            clock.tick(60)

            
            # process key presses [Will be replaced by paddle_controller function]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    

            # check if bat has hit ball    
            if ballrect.bottom >= paddlerect.top and ballrect.bottom <= paddlerect.bottom and ballrect.right >= paddlerect.left and ballrect.left <= paddlerect.right:
                yspeed = -yspeed                  
                offset = ballrect.center[0] - paddlerect.center[0]                          
                # offset > 0 means ball has hit RHS of bat                   
                # vary angle of ball depending on where ball hits bat                      
                if offset > 0:
                    if offset > 30:  
                        xspeed +=3
                    elif offset > 23:                 
                        xspeed +=2
                    elif offset > 17:
                        xspeed +=1 
                else:  
                    if offset < -30:                             
                        xspeed +=3
                    elif offset < -23:
                        xspeed +=2
                    elif xspeed < -17:
                        xspeed +=1    
                        
# =============================================================================
#             Paddle spped is getting adjusted with ballspeed
#                                     
# =============================================================================
            paddlerect=self.fuzzy_paddle_controller(HEIGHT,WIDTH,ballrect,paddlerect,xspeed)
            
            
            
            # move bat/ball
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > WIDTH:
                xspeed = xspeed                
                #pong.play(0)            
            if ballrect.top < 0:
                yspeed = -yspeed                       

            # check if ball has gone past bat - lose a life
            if ballrect.top > WIDTH:
                lives -= 1
                # start a new ball
                xspeed = xspeed_init             
                if random.random() > 0.5:
                    xspeed = -xspeed 
                yspeed = yspeed_init            
                ballrect.center = WIDTH * random.random(), HEIGHT / 3                                
                if lives == 0:                    
                    msg = pygame.font.Font(None,70).render("Game Over", True, RED, WHITE)
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(WIDTH / 2 - (msgrect.center[0]), HEIGHT / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()
                    gameOver=True
                    # process key presses
                    #     - ESC to quit
                    #     - any other key to restart game
                    while 1:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    quit()
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True      
                        if restart:                   
                            screen.fill(WHITE)
                            self.build_wall(WIDTH)
                            lives = max_lives
                            score = 0
                            break
            
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed                                
                #pong.play(0)

            if xspeed > 0 and ballrect.right > WIDTH:
                xspeed = -xspeed                               
                #pong.play(0)
           
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
            index = ballrect.collidelist(self.brickrect)       
            if index != -1: 
                if ballrect.center[0] > self.brickrect[index].right or ballrect.center[0] < self.brickrect[index].left:
                    xspeed = (xspeed+1)
                else:
                    yspeed = -yspeed                
                #pong.play(0)              
                self.brickrect[index:index + 1] = []
                score += 10
                
             
            print "x = "+str(xspeed)+", y = "+str(yspeed)
            #print str(paddlerect.left) + " - "+ str(ballrect.left)
            
            # Displaying Score    
            screen.fill(WHITE)
            scoretext = pygame.font.Font(None,30).render("Score: "+str(score), True, BLACK, WHITE)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(WIDTH - scoretextrect.right, 0)
            screen.blit(scoretext, scoretextrect)

            for i in range(0, len(self.brickrect)):
                screen.blit(self.brick, self.brickrect[i])    

            # if walls are gone show game over notification
            if self.brickrect == []:              
                 msg = pygame.font.Font(None,70).render("Game Over", True, RED, WHITE)
                 msgrect = msg.get_rect()
                 msgrect = msgrect.move(WIDTH / 2 - (msgrect.center[0]), HEIGHT / 3)
                 screen.blit(msg, msgrect)
                 pygame.display.flip()
                 gameOver=True
                 xspeed=xspeed_init
                 yspeed=yspeed_init
                 for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    quit()
         
            screen.blit(ball, ballrect)
            screen.blit(paddle, paddlerect)
            pygame.display.flip()
            
        
        screen.fill((255,255,255))
        msg = pygame.font.Font(None,40).render("Press Space button to play again?", True, (255,0,0), (255,255,255))
        msgrect = msg.get_rect()
        msgrect = msgrect.move(WIDTH / 2 - (msgrect.center[0]), HEIGHT / 3)
        screen.blit(msg, msgrect)
        pygame.display.update()
        
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    self.play()


 

if __name__ == '__main__':
    
    br = Breakout()
    br.play()
            
          

