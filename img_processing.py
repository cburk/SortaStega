import numpy
import numpy.ma as ma
import cv2
import img_geometry

# image = cv2.imread('C:\Users\cburkhartsmeyer\Pictures\iggySample.jpg')

#image = cv2.imread('VIPER!.jpg')
#image = cv2.imread('LoremREDACTED.PNG')
image = cv2.imread('LoremREDACTEDspacing.PNG')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#cv2.imshow("Image", gray_image)
print('base image')

"""
# Shouldn't use blurring on text images, no irregularities to smooth out
# blurred_image = cv2.GaussianBlur(gray_image, (7,7), 0)

# cv2.imshow("Lil Blurry", blurred_image)
# print 'blurred image'

canny = cv2.Canny(blurred_image, 30, 70)
cv2.imshow("Canny with low thresholds", canny)
# This one looks better

canny = cv2.Canny(blurred_image, 50, 150)
cv2.imshow("Canny with high thresholds", canny)
"""

canny = cv2.Canny(image, 30, 70)
#cv2.imshow("Canny with low thresholds", canny)
# This one looks better

#canny = cv2.Canny(image, 50, 150)
#cv2.imshow("Canny with high thresholds", canny)

# Get edges
im, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
# im, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

"""
If the shape found has way too many sides, it's probably not a rectangle.
"""
def plausibleRectangles(contours):
    return [x for x in contours if len(x) < 20 ]

# Min distance between original shape and enclosing rect?  I.e. most rectangle like shapes?

# returns true if the pixel at x,y in the image img is somewhere between a dark grey and full black
def isPixelMostlyBlack(image, xy):
    pixel = image[xy[1]][xy[0]]
    image[xy[0]][xy[0]] = (255, 0, 0)
    #print("This one black? " + str(ma.masked_where(pixel > 50, pixel).count() == 0))
    
    # Make sure the rgb values are minimal
    #return ma.masked_where(pixel > 50, pixel).count() == 0

    pixel = pixel.tolist()
    return pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50

"""
Finding the blacked out boxes
"""
# Ignore shapes w/ too many sides
posSquares = plausibleRectangles(contours)

# Get the corners of a rectangle enclosing each remaining shape
posSquares = [numpy.int0(cv2.boxPoints(cv2.minAreaRect(shape))) for shape in posSquares]
rectangleIdToCorners = {id: posSquares[id] for id in range(len(posSquares))}    

interiorPixels = {id: img_geometry.getPointsInRectangle(rectangleIdToCorners[id]) for id in rectangleIdToCorners}  # The interior pixels of each rectangle in posSquares are stored at the same index in this array

# Drop any that have no interiors, otherwise % calculations would be invalid
pixelCounts = {id: len(interiorPixels[id]) for id in interiorPixels}

newInteriorPixels = {}
newPixelCounts = {}
for id in pixelCounts:
    if pixelCounts[id] != 0:
        newPixelCounts[id] = pixelCounts[id]
        newInteriorPixels[id] = interiorPixels[id]
interiorPixels = newInteriorPixels
pixelCounts = newPixelCounts

# TODO: Just for testing, remove
print('most internals ids: ')
mostIds = sorted(pixelCounts, key=lambda ind: pixelCounts[ind])[-5:]
print(mostIds)
majorCoords = [rectangleIdToCorners[id] for id in mostIds]


# Get the number of pixels that are black
#pixelsBlackCount = {id: [[isPixelMostlyBlack(image, pixel) for pixel in interiorPixels[id]].count(True), pixelCounts[id]] for id in interiorPixels}
pixelsBlackCount = [[isPixelMostlyBlack(image, pixel) for pixel in interiorPixels[id]].count(True) for id in mostIds]
print("Black count for these vs num pixels total")
print(pixelsBlackCount)
print([pixelCounts[id] for id in mostIds])

# Only take the shapes that are almost all black
#posSquares = [rectangleIdToCorners[id] for id in pixelCounts if float(pixelsBlackCount[id][0])/float(pixelCounts[id]) > .5]

"""
print("Original points:")
print(posSquares[5])
print("modified:")
rect = cv2.minAreaRect(posSquares[5])
print(rect)
"""
"""
box = cv2.boxPoints(rect)
print(box)
box = numpy.int0(box)
"""

#cv2.drawContours(image,[box],0,(0,255,0),2)
#cv2.drawContours(image, posSquares, -1, (0,255,0), 2)
cv2.drawContours(image, majorCoords, -1, (0,255,0), 2)
cv2.imshow("objects Found", image)

cv2.waitKey(0)

