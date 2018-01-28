import numpy

def euclidianDistance(xy1, xy2):
    return numpy.sqrt(numpy.square(xy1[0] - xy2[0]) + numpy.square(xy1[1] - xy2[1]))

def EquivalentPoints(a, b):
    return (a[0] in b) and (a[1] in b)

# Returns true if the same point occurs twice in the list, false otherwise
def DuplicatePoints(pointsList):
    for point in pointsList:
        # We need to use a custom equivalency function, so doing it this kinda ugly way instead of using the built in counts
        thisCount = 0
        for otherPoint in pointsList:
            if EquivalentPoints(point, otherPoint):
                thisCount += 1
        if thisCount > 1:
            return True
    return False
            
        
# Given a list of 4 lists representing the euclidian coords of the 4 corners of a rectangle, return the area of the rectangle said points enclose
def rectArea(fourPtsRepresentation):
    # If any poinst are duplicates, one side has 0 length, therefore the area of the rectangle is 0
    if(DuplicatePoints(fourPtsRepresentation)):
        return 0
    
    arbitraryPoint = fourPtsRepresentation[0]
    remainingPoints = fourPtsRepresentation[1:]
    # get the point opposite the chosen one by finding the longest distance between two points hypotenuse
    pointOppositeArbitrary = sorted(remainingPoints, key=lambda point: euclidianDistance(point, arbitraryPoint))[-1]

    # Get the length and width of the rectangle.  Obtained by calculating distance from arbitrary point to the two points that are adjacent to it (remaining points)
    remainingPoints = [point for point in remainingPoints if not EquivalentPoints(point, pointOppositeArbitrary) ] # Adjacent points are those that aren't the point opposite the starter on the rectangle

    # remainingPoints -= pointOppositeArbitrary
    l = euclidianDistance(arbitraryPoint, remainingPoints[0]) # Note: since these rectangles can be rotated however, the choice for which side is length and which is width is arbitrary
    w = euclidianDistance(arbitraryPoint, remainingPoints[1])
    return l * w

"""
    returns the constants (a, b, and c) in the standard representation of the line:
    ax + by = c, or y = c/b - ax/b
    describing
    I.E. returns the definition of the line that pt1 and pt2 both lie on
    
    as per https://stackoverflow.com/questions/13242738/how-can-i-find-the-general-form-equation-of-a-line-from-two-points
    Originally using f(x) = ax + c, but this solution handled vertical lines very poorly
    """
def getLineBetween(pt1, pt2):
    # If the line is vertical, b = 0, have c/a = x value.
    if pt1[0] == pt2[0]:
        return {'a': 1, 'b': 0, 'c': pt1[0]}
    
    # Otherwise, start by using y = ax + c form
    a = float(pt2[1] - pt1[1])/float(pt2[0] - pt1[0])
    #c = float(pt1[1])/(a * pt1[0])
    # y = ax + c, y - ax = c
    c = pt1[1] - (a * pt1[0])

    # Translate to ax + by = c form.
    a *= -1
    b = 1
    
    return {'a': a, 'b': b, 'c': c}


def getOppositeRectangleCorners(rectanglePointsList):
    arbitraryPoint = rectanglePointsList[0]
    remainingPoints = rectanglePointsList[1:]
    # get the point opposite the chosen one by finding the longest distance between two points hypotenuse
    pointOppositeArbitrary = sorted(remainingPoints, key=lambda point: euclidianDistance(point, arbitraryPoint))[-1]
    return arbitraryPoint, pointOppositeArbitrary

"""
Returns a boolean indicating if the point (x, y) falls between the lines described by the pairing (a, b, c), representing
lines of the form: ax + by = c.
"""
def pointBetweenParallelLines(line_one, line_two, pt):
    # If the lines are vertical, just see if x falls between c1/a1 and c2/a2
    if(line_one['b'] == 0.0):
        x = pt[0]
        ones_x = line_one['c']/line_one['a']
        twos_x = line_two['c']/line_two['a']
        return ((ones_x > x and twos_x < x) or (twos_x > x and ones_x < x))
    
    # Otherwise, calculate y for both lines based on the x value of pt
    y = pt[1]
    x = pt[0]
    print("Point: " + str(pt))
    print("Line1: " + str(line_one))
    print("Line2: " + str(line_two))

    y1 = (line_one['c'] - (line_one['a'] * x)) / line_one['b']
    y2 = (line_two['c'] - (line_two['a'] * x)) / line_two['b']

    print("Y1 @x: " + str(y1))
    print("Y2 @x: " + str(y2))

    return (y1 > y and y2 < y) or (y2 > y and y1 < y)

# if the lines are vertical, just return whether

"""
    Given a list of 4 [x,y] coordinates (where x and y are integers) representing the edges of a rectangle, returns
    a list of all the (integer) coordinate pairs inside the rectangle

    Applicable to image processing, where this function returns the coordinates of all the pixels w/in a rectangle
"""
def getPointsInRectangle(coords_list):
    # Get the points farthest left, right, up, and down
    max_x = max([xy[0] for xy in coords_list])
    max_y = max([xy[1] for xy in coords_list])
    min_x = min([xy[0] for xy in coords_list])
    min_y = min([xy[1] for xy in coords_list])
    
    print("Mins: " + str(min_x) + ',' + str(min_y))
    print("maxs: " + str(max_x) + ',' + str(max_y))

    # Get two points opposite each other on the rectangle
    corner, opposite_corner = getOppositeRectangleCorners(coords_list)
    other_opposites = [pt for pt in coords_list if not pt in [corner, opposite_corner]]

    # Get all 4 outside lines, group parallel lines
    side_one = [corner, other_opposites[0]]
    side_two = [opposite_corner, other_opposites[1]]
    parallel_line_segments_one_pts = [side_one, side_two]
    
    side_three = [corner, other_opposites[1]]
    side_four = [opposite_corner, other_opposites[0]]
    parallel_line_segments_two_pts = [side_three, side_four]
    
    # Get the constants of each line
    side_one_defn = getLineBetween(side_one[0], side_one[1])
    side_two_defn = getLineBetween(side_two[0], side_two[1])
    parallel_line_segments_one = [side_one_defn, side_two_defn]
    
    print("b is the same for both, right? " + str(side_one_defn['a']) + ',' + str(side_two_defn['a']))

    side_three_defn = getLineBetween(side_three[0], side_three[1])
    side_four_defn = getLineBetween(side_four[0], side_four[1])
    parallel_line_segments_two = [side_three_defn, side_four_defn]

    print("b is the same for both, right? " + str(side_three_defn['a']) + ',' + str(side_four_defn['a']))

    # To be w/in the confines of the
    results = []
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            point = [x, y]
            if pointBetweenParallelLines(parallel_line_segments_one[0], parallel_line_segments_one[1], point) and pointBetweenParallelLines(parallel_line_segments_two[0], parallel_line_segments_two[1], point):
                results.append(point)

    return results


"""
Tests
"""

#res = getPointsInRectangle([[0,0], [2,0], [1,6], [3,6]])
res = getPointsInRectangle([[1,0], [0,3], [3,1], [2,4]])
print "Getting points:"
print res
print "points get got:"

def testLineWorksCorrectly():
    res = getLineBetween([2,1], [6, 3])
    print(res)
    if res['a'] != .5 or res['c'] != .0:
        print("Error: testLineWorksCorrectly returned " + str(res))


testLineWorksCorrectly()
