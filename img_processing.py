import numpy
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

"""
Finding the blacked out boxes
"""
# Ignore shapes w/ too many sides
posSquares = plausibleRectangles(contours)

# Get the corners of a rectangle enclosing each remaining shape
posSquares = [numpy.int0(cv2.boxPoints(cv2.minAreaRect(shape))) for shape in posSquares]
rectangleIdToCorners = {id: posSquares[id] for id in range(len(posSquares))}

# Ignore any rectangles that aren't mostly black
interiorPixels = {id: img_geometry.getPointsInRectangle(rectangleIdToCorners[id]) for id in rectangleIdToCorners}  # The interior pixels of each rectangle in posSquares are stored at the same index in this array
# TODO: Drop any that have no interiors, otherwise % calculations would be invalid

#print("Interiors found: ")
#print(interiorPixels[0])
#print(interiorPixels[3])
#print(interiorPixels[6])

#posSquares = pixelMostlyBlack()

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
cv2.drawContours(image, posSquares, -1, (0,255,0), 2)
cv2.imshow("objects Found", image)

cv2.waitKey(0)

