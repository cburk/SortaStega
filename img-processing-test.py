import numpy
import cv2

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
print ("Contours")

largestContoursMaybe = sorted(contours, key=lambda contGroup: len(contGroup))[-5: -1]

print [len(x) for x in largestContoursMaybe]
"""

def possibleSquares(contours):
    # TODO: check that it's a parallelogram, idk
    return [x for x in contours if len(x) < 20 ]

def euclidianDistance(xy1, xy2):
    return numpy.sqrt(numpy.square(xy1[0] - xy2[0]) + numpy.square(xy1[1] - xy2[1]))

def rectArea(fourPtsRepresentation):
    arbitraryPoint = fourPtsRepresentation[0]
    remainingPoints = fourPtsRepresentation[1:]
    # get the point opposite the chosen one by finding the longest distance between two points hypotenuse
    pointOppositeArbitrary = sorted(remainingPoints, key=lambda point: euclidianDistance(point, arbitraryPoint))[-1]

    # Get the length and width of the rectangle.  Obtained by calculating distance from arbitrary point to the two points that are adjacent to it (remaining points)
    remainingPoints -= pointOppositeArbitrary
    l = euclidianDistance(arbitraryPoint, remainingPoints[0]) # Note: since these rectangles can be rotated however, the choice for which side is length and which is width is arbitrary
    w = euclidianDistance(arbitraryPoint, remainingPoints[1])
    return l * w

# Min distance between original shape and enclosing rect?  I.e. most rectangle like shapes?

# Drawing squares around stuff
posSquares = possibleSquares(contours)
print("Original points:")
print(posSquares[5])
print("modified:")
rect = cv2.minAreaRect(posSquares[5])
print(rect)
box = cv2.boxPoints(rect)
print(box)
box = numpy.int0(box)

cv2.drawContours(image,[box],0,(0,255,0),2)
#cv2.drawContours(image, posSquares, -1, (0,255,0), 2)
cv2.imshow("objects Found", image)

cv2.waitKey(0)

