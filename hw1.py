import math

def side_length(x):
    return(x)
def area_of_square(side_length):
    return(side_length*side_length)

def radius(y):
    return(y)
def area_of_circle(radius):
    return(radius**2*math.pi)


print(area_of_square(side_length(3)))
print(area_of_circle(radius(2)))
#since 9<12.566..., the area of a circle with radius 2 is larger than the area of a square with side length 3
