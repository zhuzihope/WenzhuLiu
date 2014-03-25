# cite from the website
# and I change something and add my comments
import pygame
from pygame.locals import *

from basic import basic

# make different brushes

class PaintBrush(object):
    def __init__(self,surface):
        # create the different brush to paint on the surface
        self.lastPos = None
        self.surface = surface
        self.draw_angle = None
        self.rest = 0.0
        # at first, if the user does not choose a brush, 
        # user could not draw things on canvas
        self.org_brush = None
        self.brush = None
        self.brush_rect = None

        self.space = 1.0
        self.follow_angle = False
        self.line_pattern = None
        self.pattern_index = 0
        self.pattern_cnt = 0 
        #self.image_brush = False
        
        self.color = None
                        
    def _blit(self,pos):
        if self.brush is None:
            return
        
        if self.pattern is not None:
            # draw the blit each by each
            self.pattern_cnt += 1            
            if self.pattern_cnt > self.pattern[self.pattern_index]:
                self.pattern_index = (self.pattern_index+1)%len(self.pattern)
                self.pattern_cnt = 0
                self.pattern_on = not self.pattern_on 
            if not self.pattern_on:
                return
        
        if self.follow_angle and self.draw_angle is not None:
            # to make the line which the brush draw more smooth
            bimg = pygame.transform.rotozoom(self.brush,-self.draw_angle.get_angle(),1.0) 
            brect = bimg.get_rect()
        else:
            bimg = self.brush
            brect = self.brush_rect
                    
        brect.center = pos.ipos
        self.surface.blit(bimg,brect.topleft)

    def _blit_line(self,fromPos,toPos):
         # make the blits to be a line       
        drawVect = toPos-fromPos
        
        if self.draw_angle is None:
            # the line is a straight line
            self.draw_angle = basic(drawVect)
            self.draw_angle.length = 20.0
        else:
            # the line has angle
            self.draw_angle+=drawVect
            self.draw_angle.length = 20.0
           
        length= drawVect.length      
        
        if length < self.rest:
            self.rest-=length
            return
        # let the line not have intervals
        if self.rest>0.0:
            drawVect.length = self.rest
            cur_pos = fromPos+drawVect
        else:
            cur_pos = basic(fromPos)
        
        length-=self.rest
        self.rest = 0.0
        self._blit(cur_pos)
        
        drawVect.length = self.space
        while length > self.space:
            cur_pos += drawVect
            self._blit(cur_pos)
            length-=self.space
            
        self.rest = self.space-length
        
    def set_brush(self,brush,image_brush=False):
        # give the orignal data to the brush.
      
        self.org_brush = brush.copy()
        self.brush = brush.copy()
        self.brush_rect = brush.get_rect()
        # space is 1.0, we could not observe the space between blits
        self.space = 1.0
        self.follow_angle = False
        self.image_brush = image_brush
        self.pattern = None
        self.pattern_index = 0
        self.pattern_cnt = 0 
        self.pattern_on = True
     
    def set_space(self,space):
        # the space is distance between each blit. When space is 1.0, 
        #the space could not be observed. 
        self.space = float(space)

    def set_follow_angle(self,follow_angle):
        # when the follow_angle is true, the brush would rotate with the draw angle.
        # the line would look like more smooth
        self.follow_angle = follow_angle
                
    def set_pattern(self,pattern):
        # set a line pattern. This pattern should contain intergers to draw continuous lines.
        
        self.pattern = pattern
        self.pattern_index = 0
        self.pattern_cnt = 0 
        self.pattern_on = True
        
    def set_color(self,color):
        # the color would be got on the brush rectangle.
        if not self.brush:
            return
        self.color = color
        for x in range(self.brush_rect.width):
            for y in range(self.brush_rect.height):
                # here we get the color value at a single pixe
                c = self.brush.get_at((x, y))
                color.a = c.a
                self.brush.set_at((x,y),color)
        
    def set_alpha(self,alpha):
        # if we set this, the transparency of the line could be changed
        if not self.brush:
            return
        for x in range(self.brush_rect.width):
            for y in range(self.brush_rect.height):
                c = self.org_brush.get_at((x, y))
                if self.color is not None and not self.image_brush:
                    c.r = self.color.r
                    c.g = self.color.g
                    c.b = self.color.b
                c.a = int(round(float(c.a)*alpha))
                # here we set the color value at a single pixe
                self.brush.set_at((x,y),c)        
        
    def paint_line(self,fromPos,toPos):
        # use it to paint a line
        if not self.brush:
            return
        self.paint_from(fromPos)
        self.paint_to(toPos)    
        
    def paint_circle(self,color,fromPos,toPos):
        if not self.brush:
            return
        

    def paint_from(self,pos):
        # the line which is painted starts this position
        if not self.brush:
            return        
        self.rest = 0.0
        self.lastPos = basic(pos)
        if not self.follow_angle:            
            self._blit_line(self.lastPos,basic(pos))
        else:
            self.draw_angle = None
        self.pattern_index = 0
        self.pattern_cnt = 0
        self.pattern_on = True 

    def paint_to(self,pos):
        # the line which is painted ends this position
        if not self.brush:
            return        
        if pos and self.lastPos:
            pos = basic(pos)
            self._blit_line(self.lastPos,pos)
            self.lastPos = pos