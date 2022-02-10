try:
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    from math import sqrt

except ImportError:
    print("Failed to import a library. Check if you have installed the required libraries (numpy, matplotlib).")
    raise


def distance(x1, y1, x2, y2):
    '''Compute the distance between two points using Pythagorean theorem'''
    d = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return d


def calculate_area(x1, y1, x2, y2, x3, y3):
    '''Compute the area of a triangle defined by three points using Heron's formula'''
    a, b, c = distance(x1, y1, x2, y2), distance(x2, y2, x3, y3), distance(x1, y1, x3, y3)
    s = (a + b + c)/2
    triangle_area = sqrt(s*(s-a)*(s-b)*(s-c))
    return triangle_area


def triangle_height(base, area):
    '''
    Compute the height of a triangle required for determining 
    the distance between a point and a line connecting two other points
    '''
    height = (2*area)/base
    return abs(height)


def douglas_peucker(points, epsilon):
    '''
    Line simplification algorithm; takes input coordinates of points
    and eliminates redundant points while preserving the shape of the line. 
    The amount of eliminated points is defined by the parameter epsilon.

    Parameters:
        points(list): List of input coordinates of points.
        
        epsilon(float): A "threshold" value which determines the intensity of simplification.
            The higher the value, the more points will be eliminated.
    
    Returns:
        vertices_dump(list): List of the remaining coordinates of points after simplification.
    '''

    # Select the first and the last point in the list,
    # compute the distance between them
    start, end = points[0], points[-1]
    base = distance(start[0], start[1], end[0], end[1])
    max_length = 0
    max_length_index = 0
    vertices_dump = []

    # Scan the points between the first and the last point
    for point in points[1:-1]:
        area = calculate_area(start[0], start[1], point[0], point[1], end[0], end[1])
        
        # Calculate the distance between the currently iterated point
        # and the line defined by the first and the last point
        distance_to_base = triangle_height(base, area)

        # Store the distance and the index of the most distant point
        if max_length == 0 or max_length < distance_to_base:
            max_length = distance_to_base
            max_length_index = points.index(point)
    
    # Compare the distance of the most distant point to epsilon,
    # if greater, preserve the point and recursively split the line into two segments
    # and repeat the procedure
    if max_length > epsilon:
        left_side = douglas_peucker(points[:max_length_index+1], epsilon)
        vertices_dump += [list(vertex) for vertex in left_side if list(vertex) not in vertices_dump]
        right_side = douglas_peucker(points[max_length_index:], epsilon)
        vertices_dump += [list(vertex) for vertex in right_side if list(vertex) not in vertices_dump]
    
    else:
        vertices_dump += [points[0], points[-1]]
    
    # Return the remaining points after simplification
    return vertices_dump

def create_figure(graph1_x, graph1_y, graph2_x, graph2_y):
    '''
    Visualize the input and the simplified line. 

    Parameters:
        graph1_x(y)(list): List of coordinates of points of the input line.
        
        graph2_x(y)(list): List of coordinates of points of the simplified line.
    '''
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Douglas-Peucker algorithm, ε set to {}".format(set_epsilon), fontsize = 20)
    ax1.plot(graph1_x, graph1_y, "-o", color = "black", markersize = 5, markerfacecolor = "white")
    ax1.set_title("Raw line; number of vertices: {}".format(len(points)))
    ax1.set(xlabel = "x-axis", ylabel = "y-axis")
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.plot(graph2_x, graph2_y, "-o", color = "black", markersize = 5, markerfacecolor = "white")
    ax2.set_title("Simplified line; number of vertices: {}".format(len(result)))
    ax2.set(xlabel = "x-axis", ylabel = "y-axis")
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    plt.show()

# Set the name of the input and output file. This is the default setting.
infilename = "sample_line.json"
outfilename = "simplified_line.json"

# Load from the input file
try:
    with open (infilename, encoding = "utf-8") as sample_line:
        lines = json.load(sample_line)
        points = lines["features"][0]["geometry"]["paths"][0]

except IOError:
    print(f"File {infilename} does not exist. Check if the file is in the same directory as the script.")
    raise

except KeyError:
   print("File does not contain the required attributes, or their path is incorrect.\
        Repair the file and run the script again.")
   raise

except:
    print("Something went wrong, the script will now terminate .")
    raise

# Set the value of epsilon. This is the default value for the input coordinates in S-JTSK.
# Lower the value if you use a different coordinate system.
set_epsilon = 50

# Store the simplified line into a variable
result = np.array(douglas_peucker(points, set_epsilon))

# Transpose the lines' coordinates, required for visualization
x, y = np.array(points).T
xs, ys = result.T

# Create a JSON file for the simplified coordinates
to_json = {
    "features": {
        "geometry": result.tolist()
    }
}

with open(outfilename, "w", encoding = "utf-8") as output:
    json.dump(to_json, output, ensure_ascii = False, indent = 2)

# Visualize the algorithm before and after execution
create_figure(x, y, xs, ys)