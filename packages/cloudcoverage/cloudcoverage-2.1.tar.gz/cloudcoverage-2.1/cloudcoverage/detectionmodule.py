import cv2, Rectangle, os

__CLOUD_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CloudCascade.xml'))
__WATERSPOUT_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'WaterspoutCascade.xml'))

#Detects clouds in a given image.
#@param image: the image to detect clouds in
#@return list of Rectangles that are the clouds found
def detectClouds(image):
	return __detect(image, __CLOUD_CASCADE,
			(50, 50),
			(700, 700),
			1.01,
			2,
			.5)

#Detects waterspouts in a given image.
#@param image: the image to detect clouds in
#@return list of Rectangles that are the clouds found
def detectWaterspouts(image):
	return __detect(image, __WATERSPOUT_CASCADE,
			(40, 40),
			(600, 600),
			1.01,
			3,
			.5)

#Writes the given list of Rectangles to the file corresponding
#	to the file path given.
#@param rects list of Rectangles to write
#@param filePath path to the file to write to
#@return nothing
def writeRects(rects, filePath):
	string = ""
	
	for rect in rects:
		string += str(rect) + "\n"
	
	if len(string) > 0:
		string = string[0 : len(string) - 1]
	
	file = open(filePath, "w")
	file.write(string)
	file.flush()

#Displays the given image. The displayed image can be
#	closed by pressing escape.
#@param image image to show
#@param title title of the window
#@return nothing
def displayImage(image, title):
	cv2.imshow(title, image)
	
	key = 0
	while key != 27:
		key = cv2.waitKey(30) & 0xff
	
	cv2.destroyAllWindows()

#Draws the given list of Rectangles to the given image.
#@param image image to draw to
#@param rects list of Rectangles to draw
#@param color 3-tuple of integer values 0-255 (RGB) that
#	is the color to draw the rectangles
#@param thickness thickness of the rectangles drawn
def drawRects(image, rects, color, thickness):
	for rect in rects:
		cv2.rectangle(image, rect.getPoint(), rect.getOppositePoint(),
				(0, 0, 255), 2)

#Uses OpenCV to detect things using given parameters.
#@param image image to find objects in
#@param cascade CascadeClassifier to use
#@param minsize 2-tuple of integers that is the minimum size of
#	an object to find
#@param maxsize 2-tuple of integers that is the maximum size of
#	an object to find
#@param scalefactor factor to scale the image by each pass
#@param minneighbors minimum number of neighbor rectangles for a
#	rectangle to be valid
#@param areatheshold number 0-1 that determines if two intersecting
#	rectangles will be combined. The number 0-1 represents shared
#	area to be required
#@return list of Rectangles representing all the objects found
def __detect(image, cascade, minsize, maxsize, scalefactor, minneighbors, areathreshold):
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	
	finds = cascade.detectMultiScale(image,
			minSize = minsize,
			maxSize = maxsize,
			scaleFactor = scalefactor,
			minNeighbors = minneighbors)
            
	
	rects = []
	for x, y, w, h in finds:
		rects.append(Rectangle.Rectangle(x, y, w, h))
	
	rects = Rectangle.combineRects(rects, areathreshold)
	
	return rects