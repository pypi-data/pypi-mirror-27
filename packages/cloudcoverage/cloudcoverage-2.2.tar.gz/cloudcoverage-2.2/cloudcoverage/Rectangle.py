#Combines rectangles in a list of rectangles if two rectangles
#	intersect by an area greater than or equal to a given threshold
#@param rects list of Rectangles to check
#@param areatheshold number 0-1 that determines if two intersecting
#	rectangles will be combined. The number 0-1 represents shared
#	area to be required
def combineRects(rects, areaThreshold):
	i = 0
	j = 0
	
	while i < len(rects):
		j = i + 1
		
		while j < len(rects):
			intersectRect = rects[i].getIntersection(rects[j])
			
			if intersectRect != None:
				area1 = rects[i].getArea()
				area2 = rects[j].getArea()
				area = area1 if area1 < area2 else area2
				threshold = area * areaThreshold
				
				intersect_area = intersectRect.getArea()
				
				if intersect_area > threshold:
					rect1 = rects.pop(j)
					rect2 = rects.pop(i)
					rects.append(rect1.getIntersection(rect2))
					return combineRects(rects, areaThreshold)
			
			j += 1
		
		i += 1
	return rects

class Rectangle:
	x = 0
	y = 0
	w = 0
	h = 0
	
	#Initialize the rectangle with x=0, y=0, w=0, h=0.
	def __init__(self):
		pass
	
	#Initialize the rectangle with x, y, w, h.
	#@param x starting x-value
	#@param y starting y-value
	#@param w starting width
	#@param h starting height
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
	#Determines if this rectangle contains a given point.
	#@param x x-coordinate to check
	#@param y y-coordinate to check
	#@return True if this Rectangle contains the given point
	def contains(self, x, y):
		return x >= self.x and y >= self.y and \
			   x < self.x + self.w and y < self.y + self.h
	
	#Determines if a given Rectangle is entirely contained
	#	within this rectangle.
	#@param rect Rectangle to check
	#@return True if the given Rectangle is entirely contained
	#	in this one
	def containsRect(self, rect):
		return rect.x >= self.x and \
			   rect.y >= self.y and \
			   rect.x + rect.w < self.x + self.w and \
			   rect.y + rect.h < self.y + self.h
	
	#Determines if a given Rectangle intersects this one.
	#@param rect Rectangle to check
	#@return True if the given Rectangle intersects this one
	def intersects(self, rect):
		return self.contains(rect.x, rect.y) or \
			   self.contains(rect.x + rect.w, rect.y) or \
			   self.contains(rect.x, rect.y + rect.h) or \
			   self.contains(rect.x + rect.w, rect.y + rect.h) or \
			   rect.contains(self.x, self.y) or \
			   rect.contains(self.x + self.w, self.y) or \
			   rect.contains(self.x, self.y + self.h) or \
			   rect.contains(self.x + self.w, self.y + self.h)
	
	#Finds a Rectangle that is the intersection rectangle of
	#	a given Rectangle and this one.
	#@param rect Rectangle to check
	#@return intersection Rectangle of the given Rectangle and this one
	def getIntersection(self, rect):
		if not self.intersects(rect):
			return None
		
		x1 = self.x if self.x < rect.x else rect.x
		y1 = self.y if self.y < rect.y else rect.y
		
		x_1 = self.x + self.w
		x_2 = rect.x + rect.w
		x2 = x_1 if x_1 > x_2 else x_2
		
		y_1 = self.y + self.h
		y_2 = rect.y + rect.h
		y2 = y_1 if y_1 > y_2 else y_2
		
		w = x2 - x1
		h = y2 - y1
		
		return Rectangle(x1, y1, w, h)
	
	#@return 2-tuple (x, y) where x and y are the coordinates
	#	of the upper-left corner of this rectangle
	def getPoint(self):
		return (self.x, self.y)
	
	#@return 2-tuple (x, y) where x and y are the coordinates
	#	of the lower-right corner of this rectangle
	def getOppositePoint(self):
		return (self.x + self.w, self.y + self.h)
	
	#@return area of this rectangle
	def getArea(self):
		return self.w * self.h
	
	#@return string representation of this Rectangle in the
	#	form "[x, y, w, h]"
	def __str__(self):
		return "[%d, %d, %d, %d]" % (self.x, self.y, self.w, self.h)