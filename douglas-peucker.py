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

def douglas_peucker(points, epsilon):
    start, end = points[0], points[-1]
    base = distance(start[0], start[1], end[0], end[1])
    max_length = 0
    max_length_index = None
    vertices_dump = []

    for point in points[1:-1]:
        area = calculate_area(start[0], start[1], point[0], point[1], end[0], end[1])
        distance_to_base = triangle_height(base, area)

        if max_length == 0 or max_length < distance_to_base:
            max_length = distance_to_base
            max_length_index = points.index(point)
    
    if max_length > epsilon:
        left_side = douglas_peucker(points[:max_length_index+1], epsilon)
        vertices_dump += [list(i) for i in left_side if list(i) not in vertices_dump]
        right_side = douglas_peucker(points[max_length_index:], epsilon)
        vertices_dump += [list(i) for i in right_side if list(i) not in vertices_dump]
    
    else:
        vertices_dump += [points[0], points[-1]]
    
    return vertices_dump

with open ("sample_line.json", encoding="utf-8") as sample_line:
    lines = json.load(sample_line)

points = lines["features"][0]["geometry"]["paths"][0]
rawline = np.array(points)
set_epsilon = 50

result = np.array(douglas_peucker(points, set_epsilon))

x, y = result.T
xs, ys = rawline.T

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Douglas-Peucker algorithm, ε set to {}".format(set_epsilon))
ax1.plot(xs, ys)
ax1.plot(xs, ys, "r+")
ax1.set_title("Raw line")
ax1.set(xlabel = "x-axis", ylabel = "y-axis")
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax2.plot(x, y)
ax2.plot(x, y, "r+")
ax2.set_title("Simplified line")
ax2.set(xlabel = "x-axis", ylabel = "y-axis")
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)

plt.show()