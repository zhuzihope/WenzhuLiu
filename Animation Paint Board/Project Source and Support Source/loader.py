# Wenzhu Liu + wenzhul
# load the image and font on the canvas.
import pygame
from pygame.locals import*
from os import path

# it is a class that load image and font on the canvas

class Loader(object):
	def __init__(self):
		pass

	def load_image(self,filename,alpha=False):
		# load the image (which you have drawn on the canvas)
		filepath = path.join("data","img",filename)
		img = pygame.image.load(filepath)
		if alpha:
		    img = img.convert_alpha()
		else:
		    img = img.convert()
		return img  

	def load_font(self,filename,size):
		# load font on the canvas
		filepath=path.join("data",filename)
		fnt=pygame.font.Font(filepath,size)
		return fnt