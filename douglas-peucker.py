import json
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from sympy import Polygon, Point

def distance(x1, y1, x2, y2):
    d = sqrt((x1-x2)**2 + (y1-y2)**2)
    return(d)

def distance2(x1, y1, x2, y2):
    d = Point(x1, y1).distance(Point(x2, y2))
    return float(d)

def calculate_area(x1, y1, x2, y2, x3, y3):
    triangle = Polygon((x1, y1), (x2, y2), (x3, y3))
    return float(triangle.area)

def distance_ptl(base, area):
    height = (2*area)/base
    return height

with open ("sample_line.json", encoding="utf-8") as sample_line:
    lines = json.load(sample_line)

points = np.array(lines["features"][0]["geometry"]["paths"][0])
x, y = points.T

sample = distance(points[0][0], points[0][1], points[-1][0], points[-1][1])
#sample2 = Point(points[0][0],points[0][1]).distance(Point(points[-1][0],points[-1][1]))
sample3 = distance2(points[0][0], points[0][1], points[-1][0], points[-1][1])

poly = Polygon((points[0][0],points[0][1]),(points[1][0],points[1][1]),(points[2][0],points[2][1]),(points[3][0],points[3][1]))
print(points)



plt.scatter(x, y)
plt.show()
print(sample)
print(sample3)
print(float(poly.area))
