# Wenzhu Liu + wenzhul + section L
# This is the basic class which includes some basic functions 
# that get the pressed position, get the angle of line and get the length of line.
import operator
import math
class basic(object):
	# get the mouse press position, get the length of the line 
	# which you draw
	def __init__(self,x,y=None):
		if x is not None and y is not None:
			self.x=float(x)
			self.y=float(y)
		# if x is a class, make a x,zy
		elif type(x)==basic:
			self.x=x.x
			self.y=x.y
		# if x is a list or tuple, make a x,y
		elif type(x)==list or type(x)==tuple:
			self.x=x[0]
			self.y=x[1]
		else:
			raise TypeError()

	# get and set the position of mouse pressed
	def get_pos(self):
		return (self.x,self,y)

	def set_pos(self,pos):
		self.x=float(x)
		slef.y=float(y)
	pos=property(get_pos,set_pos)

	def get_int_pos(self):
		return (int(round(self.x)),int(round(self.y)))
	ipos=property(get_int_pos,set_pos)

	# get the length of user have draw
	def get_length(self):
		return math.sqrt(self.x**2 + self.y**2)        
	def set_length(self, len):
		l = self.get_length()
		if l: 
		    self.x /= l
		    self.y /= l
		self.x *= len
		self.y *= len 
	length = property(get_length, set_length)


    # get the thick line's both ends' angle
	def get_angle(self):
		if((self.x**2 + self.y**2) == 0):
			return 0
		return math.degrees(math.atan2(self.y, self.x)) 

	def set_angle(self, angle):
	    self.x = self.get_length()
	    self.y = 0
	    r = math.radians(angle)
	    c = math.cos(r)
	    s = math.sin(r)
	    nx = self.x*c - self.y*s
	    ny = self.x*s + self.y*c
	    self.x = nx
	    self.y = ny        
	angle = property(get_angle, set_angle)

	# make some operators
	def __add__(self, other): 
	    return basic(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
	    return basic(self.x-other.x,self.y-other.y)