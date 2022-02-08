import json
import matplotlib.pyplot as plt
import numpy as np
from sympy import Polygon, Point

def distance(x1, y1, x2, y2):
    d = Point(x1, y1).distance(Point(x2, y2))
    return float(d)

def calculate_area(x1, y1, x2, y2, x3, y3):
    triangle = Polygon((x1, y1), (x2, y2), (x3, y3))
    return float(triangle.area)

def triangle_height(base, area):
    height = (2*area)/base
    return abs(height)

with open ("sample_line.json", encoding="utf-8") as sample_line:
    lines = json.load(sample_line)

points = lines["features"][0]["geometry"]["paths"][0]

unedited = np.array(points)

print(points)

def douglas_peucker(points, epsilon):
    start, end = points[0], points[-1]
    base = distance(start[0], start[1], end[0], end[1])
    max_length = 0
    max_length_index = None
    

    for point in points[1:-1]:
        area = calculate_area(start[0], start[1], point[0], point[1], end[0], end[1])
        distance_to_base = triangle_height(base, area)

        if max_length == 0 or max_length < distance_to_base:
            max_length = distance_to_base
            max_length_index = points.index(point)
    
    vertices_dump = []
    if max_length > epsilon:

        left_side = douglas_peucker(points[:max_length_index+1], epsilon)
        vertices_dump += [list(i) for i in left_side if list(i) not in vertices_dump]
        right_side = douglas_peucker(points[max_length_index:], epsilon)
        vertices_dump += [list(i) for i in right_side if list(i) not in vertices_dump]
    
    else:
        vertices_dump += [points[0], points[-1]]
    
    return vertices_dump

result = np.array(douglas_peucker(points, 100))
print(result)
x, y = result.T
xs, ys = unedited.T




plt.plot(x, y)
plt.plot(xs,ys)
plt.plot(x, y, "r+")
plt.show()
#print(sample)
#print(sample3)
#print(float(poly.area))
