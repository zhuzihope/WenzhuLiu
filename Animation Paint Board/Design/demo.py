# Wenzhu Liu + wenzhul + section L

# This is the main class which makes the paint board work well.
# We could draw like pencil, pen, and dropper. It also includes eraser, images
# and the method how to draw a regular line.
# What's more, we could put some images on the canvas and make them move 
# in different directions and different speeds. But what a pity that only the two different images 
# could move on the canvas. The number of one image could be just one.

import pygame
from pygame.locals import *
from sys import exit
from loader import Loader

from PaintBrush import PaintBrush
                       
class demo(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600),1)
        #  load image and font on the canvas
        self.loader = Loader()
        # load the palette
        self.palette = self.loader.load_image("palette.png",True)
        # the knob which change the transparency of color
        self.knob = self.loader.load_image("knob.png",True)
        self.knob_rect = self.knob.get_rect()
        self.knob_rect.topleft = (14,215)
        # the origninal paint board on the canvas
        self.back = self.loader.load_image("paintboard.png", True)
        # the 2 backgrounds to choose
        self.back1_back = self.loader.load_image("back1.jpg",False)
        self.back2_back = self.loader.load_image("back2.jpg",False)
        # load the animation pictures
        self.sprite1 = self.loader.load_image("sprite1.png", True)
        self.sprite2 = self.loader.load_image("sprite2.png", True)
        # load the different brushes 
        self.b1 = self.loader.load_image("brush_1.png", True) 
        self.b2 = self.loader.load_image("brush_2.png", True) 
        self.b3 = self.loader.load_image("brush_3.png", True) 
        self.b5 = self.loader.load_image("brush_5.png", True) 
        self.b6 = self.loader.load_image("brush_6.png", True)
        self.b7 = self.loader.load_image("brush_7.png", True)
        self.b8 = self.loader.load_image("brush_8.png", True)
        self.b9 = self.loader.load_image("brush_9.png", True)
        # draw the icon
        self.icon = self.loader.load_image("Paint.png", True)
        # the current color is black
        self.cur_color = pygame.Color(0,0,0)
        # put the canvas which could be drawed things on it
        self.paper_rect = pygame.Rect(127,12,659,574)
        self.paper = self.loader.load_image("paper.png",True)
        # draw regular line, initially, it is false 
        self.draw_lines = False
        # before choose a brush, user could not draw anything
        # on the canvas
        self.painting = False
        # load the palette 
        self.pal_rect = pygame.Rect(12,12,101,200)
        # different brushes on different positions on the board
        self.brush_rect = pygame.Rect(12,231,101,355)
        self.brush_rects = [] 
        self.brush_rects.append(pygame.Rect(12,231,101,200))
        self.brush_rects.append(pygame.Rect(12,332,50,50))
        self.brush_rects.append(pygame.Rect(63,332,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*1,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*1,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*2,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*2,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*3,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*3,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*4,50,50))
        self.lines_rect = pygame.Rect(12,332+51*4,50,50)
        # input the class PaintBrush
        self.brush = PaintBrush(self.paper)
        # the positions about animation part
        self.sprite1_rect = pygame.Rect(826,122,72,72)
        self.sprite2_rect = pygame.Rect(905,122,72,72)
        self.left_rect = pygame.Rect(818,306,46,43)
        self.right_rect = pygame.Rect(938,305,42,45)
        self.down_rect = pygame.Rect(876,305,48,48)
        self.slow_rect = pygame.Rect(835,427,69,27)
        self.quick_rect = pygame.Rect(910,427,67,30)
        # the data and parameter of the animation
        self.slow_speed = 40
        self.quick_speed = 140 
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.keep_move_left1 = False
        self.keep_move_right1 = False
        self.keep_move_down1 = False
        self.keep_move_left2 = False
        self.keep_move_right2 = False
        self.keep_move_down2 = False
        self.sprite1_move = False
        self.sprite2_move = False
        self.keep_sprite1_move = False
        self.keep_sprite2_move = False
        self.keep_slow_speed1 = False
        self.keep_slow_speed2 = False
        self.keep_quick_speed1 = False
        self.keep_quick_speed2 = False
        # the positions of 2 sprites, first, they are none
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
            
    # give the choosed color to brush
    def set_color(self,c):
        self.cur_color = c
        self.brush.set_color(c)

    # the transparency of the color
    def set_alpha(self,a):
        if a <= 0.0:
            a = 0.005
            x = 20
        elif a >= 1.0:
            a = 1.0
            x = 100
        else:
            x = int(round(20.0+100.0*a))
        self.brush.set_alpha(a)
        self.knob_rect.left = x

    # when choose different brush, let the brush draw sth on the canvas
    def set_brush(self,idx):
        # draw the pencil
        if idx == 1:
            self.brush.set_brush(self.b1)
            self.brush.set_space(0.5)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        # draw the brush pen
        elif idx == 2:
            self.brush.set_brush(self.b2)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(0.1)
        # draw like dropper
        elif idx == 3:
            self.brush.set_brush(self.b3)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        # draw the break line 
        elif idx == 4:
            self.brush.set_brush(self.b1)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.brush.set_pattern([2,20])
            self.set_alpha(1.0)
        # it is the eraser
        elif idx == 5:
            self.cur_color = pygame.Color(255,255,255)
            self.brush.set_brush(self.b5)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(0.2)
        # draw the picture which is snow
        elif idx == 6:
            self.brush.set_brush(self.b6,True)
            self.brush.set_space(65.0)
            self.set_alpha(1.0)
        # draw the picture which is heart
        elif idx == 7:
            self.brush.set_brush(self.b7,True)
            self.brush.set_space(65.0)
            self.set_alpha(1.0)
        # draw the picture which is star
        elif idx == 8:
            self.brush.set_brush(self.b8,True)
            self.brush.set_space(65.0)
            self.set_alpha(1.0)
        # draw the moon
        elif idx == 9:
            self.brush.set_brush(self.b9,True)
            self.brush.set_space(80.0)
            self.set_alpha(1.0)

    # choose which image on the right column of the board should move
    def set_image1(self):
        self.brush.set_brush(self.sprite1)
        self.brush.set_space(65.0)
        self.set_alpha(1.0)
    def set_image2(self):
        self.brush.set_brush(self.sprite2)
        self.brush.set_space(65.0)
        self.set_alpha(1.0)
        
    # start drawing    
    def paint_start(self):
        self.painting = True
        ###self.save_paper()
    # stop drawing  
    def paint_stop(self):
        self.painting = False

    # the sprite 1 moves left
    def moveLeft1(self,speed):
        self.screen.blit(self.sprite1, (self.x1-240, self.y1-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.x1 -= self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.x1 < 300.:
            self.x1 += 290.

    # the sprite 2 move left
    def moveLeft2(self,speed):
        self.screen.blit(self.sprite2, (self.x2-240, self.y2-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.x2 -= self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.x2 < 350.:
            self.x2 += 300.

    #  the sprite 1 move right
    def moveRight1(self,speed):
        self.screen.blit(self.sprite1, (self.x1-240, self.y1-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.x1 += self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.x1 > 610.:
            self.x1 -= 350.

    # the sprite 2 move right   
    def moveRight2(self,speed):
        self.screen.blit(self.sprite2, (self.x2-240, self.y2-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.x2 += self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.x2 > 650.:
            self.x2 -= 300.

    # the sprite 1 move down
    def moveDown1(self,speed):
        self.screen.blit(self.sprite1, (self.x1-240, self.y1-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.y1 += self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.y1 > 500.:
            self.y1 -= 350.

    # the sprite 2 move down
    def moveDown2(self,speed):
        self.screen.blit(self.sprite2, (self.x2-240, self.y2-150))
        self.clock = pygame.time.Clock()
        self.time_passed = self.clock.tick(30)
        self.time_passed_seconds = self.time_passed / 1000.0
        self.distance_moved = self.time_passed_seconds * speed
        self.y2 += self.distance_moved

        # If the image goes off the end of the screen, move it back
        if self.y2 > 450.:
            self.y2 -= 375.


    # this is refer to some code from the web           
    def main_loop(self): 
        # set the time            
        clock = pygame.time.Clock()
        
        line_from = None
        line_to = None
        circle_from = None
        circle_to = None

        cur_color = pygame.Color(0,0,0)

        next_update = pygame.time.get_ticks()
        drag_knob = False
        # make the brushes and sprites work
        while 1:   
            # draw the title of the window and the icon
            pygame.display.set_caption("Paint Board")
            pygame.display.set_icon(self.icon)

            # working follows the keyboard and the mouse 
            for event in pygame.event.get():
                # when press one key
                if event.type == KEYDOWN:
                    # change backgrounds
                    if event.key == K_F1:
                        self.paper = self.back1_back
                    elif event.key == K_F2:
                        self.paper = self.back2_back
                    elif event.key == K_F3:
                        # this is a white drawing board
                        self.paper = (pygame.Surface(self.paper_rect.size,1)).convert()
                        self.paper.fill((255,255,255))
                    # the brush could be used on these backgrounds
                    self.brush = PaintBrush(self.paper)
                    
                # mouse pressed 
                if event.type == MOUSEBUTTONDOWN:
                    # check if the user press the direction button on the board
                    # move left
                    if self.left_rect.collidepoint(event.pos):
                        self.move_left = True
                        self.move_right = False
                        self.move_down = False
                        # if press the sprite 1 before, then the sprite 1 moves
                        if self.sprite1_move:
                            self.keep_move_left1 = True
                            self.keep_move_right1 = False
                            self.keep_move_down1 = False
                        else:
                            self.keep_move_left2 = True
                        
                            self.keep_move_right2 = False
                            self.keep_move_down2 = False
                    # move right
                    if self.right_rect.collidepoint(event.pos):
                        self.move_right = True
                        self.move_left = False
                        self.move_down = False
                        if self.sprite1_move:
                            self.keep_move_right1 = True
                            self.keep_move_left1 = False
                            self.keep_move_down1 = False
                        else:
                            self.keep_move_right2 = True
                        
                            self.keep_move_left2 = False
                            self.keep_move_down2 = False
                    # move down
                    if self.down_rect.collidepoint(event.pos):
                        self.move_down = True
                        self.move_left = False
                        self.move_right = False
                        if self.sprite1_move:
                            self.keep_move_down1 = True
                            self.keep_move_left1 = False
                            self.keep_move_right1 = False
                        if self.sprite2_move:
                            self.keep_move_down2 = True
                            self.keep_move_left2 = False
                            self.keep_move_right2 = False
                    # set the speed
                    # slow
                    if self.slow_rect.collidepoint(event.pos):
                        if self.sprite1_move:
                            self.keep_slow_speed1 = True
                            self.keep_quick_speed1 = False
                        if self.sprite2_move:
                            self.keep_slow_speed2 = True
                            self.keep_quick_speed2 = False
                    # quickly
                    elif self.quick_rect.collidepoint(event.pos):
                        if self.sprite1_move:
                            self.keep_quick_speed1 = True
                            self.keep_slow_speed1 = False
                        if self.sprite2_move:
                            self.keep_quick_speed2 = True
                            self.keep_slow_speed2 = False

                    # if click on the palette
                    if self.pal_rect.collidepoint(event.pos):
                        self.move_left = False
                        self.move_right = False
                        self.move_down = False
                        self.draw_lines = False
                        # choose the painting color
                        c = self.back.get_at(event.pos)
                        self.set_color(c)

                    # if click on the brush
                    elif self.brush_rect.collidepoint(event.pos):
                        self.move_left = False
                        self.move_right = False
                        self.move_down = False
                        self.draw_lines = False
                        # the mouse press on the brush rectangle, 
                        # except the last two, because they draw regular graphics
                        if self.lines_rect.collidepoint(event.pos):
                            self.draw_lines = True
                        else:
                            i = 0
                            for r in self.brush_rects:
                                if r.collidepoint(event.pos):
                                    self.set_brush(i)
                                i+=1

                    # when mouse press on the sprite which should move
                    # sprite 1 moves
                    elif self.sprite1_rect.collidepoint(event.pos):
                        self.sprite1_move = True
                        self.sprite2_move = False
                        self.keep_sprite1_move = True 
                    # sprite 2 moves 
                    elif self.sprite2_rect.collidepoint(event.pos):
                        self.sprite2_move = True
                        self.sprite1_move = False
                        self.keep_sprite2_move = True
                    
                    # click the knob
                    elif self.knob_rect.collidepoint(event.pos):
                        self.draw_lines = False
                        # change the transparency of the color
                        drag_knob = True

                    # draw things on the canvas
                    elif self.paper_rect.collidepoint(event.pos):
                        # the mouse press on the canvas,
                        # set the start point of drawing
                        if self.draw_lines:
                            # draw regular lines
                            #self.move_left = False
                            line_from = event.pos

                        # give the start position to the sprite
                        elif self.move_left or self.move_right or self.move_down:
                            # sprite 1
                            if self.sprite1_move:
                                self.x1 = event.pos[0]
                                self.y1 = event.pos[1]
                                self.sprite1_move = False
                            # sprite 2   
                            elif self.sprite2_move:
                                self.x2 = event.pos[0]
                                self.y2 = event.pos[1]
                                self.sprite2_move = False
                                
                        else:
                            # use brush draw everything you want
                            self.paint_start()
                            x = event.pos[0]-self.paper_rect.x
                            y = event.pos[1]-self.paper_rect.y
                            self.brush.paint_from((x,y))
                    
                            
                elif event.type == MOUSEMOTION:
                    # when mouse motions 
                    if event.buttons[0]:
                        if drag_knob:
                            self.knob_rect.left+=event.rel[0]
                            # the knob could only move during (15,100)
                            # change the transparency of the color
                            if self.knob_rect.left < 15:
                                self.knob_rect.left = 15
                            if self.knob_rect.left > 100:
                                self.knob_rect.left = 100

                        elif self.draw_lines == True:
                            # draw regular lines
                            line_to = event.pos 
                            painting = False
                        

                        elif self.paper_rect.collidepoint(event.pos):
                            # draw whatever the user wants
                            if self.painting:
                                x = event.pos[0]-self.paper_rect.x
                                y = event.pos[1]-self.paper_rect.y
                                self.brush.paint_to((x,y))    
                           
                elif event.type == MOUSEBUTTONUP:
                    # when the mouse button is up
                    if drag_knob:
                        # stop changing tranparency
                        drag_knob = False
                        a = float(self.knob_rect.left-14)/83.0
                        self.set_alpha(a)
                    
                    if event.button == 1 and self.painting:
                        # stop painting
                        self.paint_stop()

                    elif line_from:
                    # load the regular line on the canvas
                        self.paint_start()
                        fx = line_from[0]-self.paper_rect.x
                        fy = line_from[1]-self.paper_rect.y
                        tx = event.pos[0]-self.paper_rect.x
                        ty = event.pos[1]-self.paper_rect.y
                        
                        self.brush.paint_line((fx,fy),(tx,ty))
                        self.paint_stop()
                        line_from = None
                        line_to = None       
                                                          
            if pygame.time.get_ticks() >= next_update:
                # update the board all the time
                next_update+=33
                # the interval is 33
                self.screen.blit(self.back,(0,0))
                # load the whole paint board
                self.screen.blit(self.paper,self.paper_rect.topleft)
                # load the canvas
                
                if line_from and line_to:
                # when draw regular line, it is the assistant line
                    pygame.draw.line(self.screen, (0,0,0), line_from, line_to)

                self.screen.blit(self.knob,self.knob_rect.topleft)
                # show the knob 
                pygame.draw.circle(self.screen,self.cur_color,(62,281),25,0)
                # show the color which the user choose 

                # make the sprite 1 move
                if self.x1 != None and self.y1 != None:
                    if self.keep_move_left1 ==True:
                        if self.keep_sprite1_move == True:
                            # sprite 1 moves left in different speeds
                            if self.keep_slow_speed1:
                                self.moveLeft1(self.slow_speed)
                    
                            if self.keep_quick_speed1:
                                self.moveLeft1(self.quick_speed)

                    elif self.keep_move_right1 == True:
                        if self.keep_sprite1_move == True:
                            # sprite 1 moves right in different speeds
                            if self.keep_slow_speed1:
                                self.moveRight1(self.slow_speed)
                            if self.keep_quick_speed1:
                                self.moveRight1(self.quick_speed)

                    elif self.keep_move_down1 == True:
                        if self.keep_sprite1_move == True:
                            if self.keep_slow_speed1:
                                self.moveDown1(self.slow_speed)
                            if self.keep_quick_speed1:
                                self.moveDown1(self.quick_speed)

                # make the sprite 2 moves
                if self.x2 != None and self.y2 != None:
                    if self.keep_move_left2 ==True:
                        if self.keep_sprite2_move == True:
                            if self.keep_slow_speed2:
                                self.moveLeft2(self.slow_speed)
                            if self.keep_quick_speed2:
                                self.moveLeft2(self.quick_speed)
                            
                    elif self.keep_move_right2 == True:
                        if self.keep_sprite2_move == True:
                            if self.keep_slow_speed2:
                                self.moveRight2(self.slow_speed)
                            if self.keep_quick_speed2:
                                self.moveRight2(self.quick_speed)

                    elif self.keep_move_down2 == True:
                        if self.keep_sprite2_move == True:
                            if self.keep_slow_speed2:
                                self.moveDown2(self.slow_speed)
                            if self.keep_quick_speed2:
                                self.moveDown2(self.quick_speed)

                #flip the display
                pygame.display.flip()   

def main():
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    pygame.init()

    g = demo()
    g.main_loop()
 
if __name__ == '__main__': 
    main()