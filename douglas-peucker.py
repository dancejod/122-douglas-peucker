try:
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    from sympy import Polygon, Point

except ImportError as e:
    raise ImportError(f"{e}.\nNemate nainstalovane nejaku z pozadovanych kniznic (matplotlib, numpy, sympy). Nainstalujte ich a spustite skript znova.")

def distance(x1, y1, x2, y2):
    '''Vypocet vzdialenosti medzi dvoma bodmi o znamych suradniciach'''
    d = Point(x1, y1).distance(Point(x2, y2))
    return float(d)

def calculate_area(x1, y1, x2, y2, x3, y3):
    '''Vypocet plochy trojuholnika definovaneho bodmi o znamych suradniciach'''
    triangle = Polygon((x1, y1), (x2, y2), (x3, y3))
    return float(triangle.area)

def triangle_height(base, area):
    '''
    Vypocet vysky trojuholnika podla zakladne a plochy; potrebne pre urcenie 
    vzdialenosti bodov od spojnice prveho a posledneho bodu
    '''
    height = (2*area)/base
    return abs(height)

def douglas_peucker(points, epsilon):
    '''
    Generalizacny algoritmus; vezme vstupne suradnice bodov tvoriace liniu
    a rekurzivne zmensi ich pocet tak, aby sa zachoval tvar linie. 
    Intenzita generalizacie je dana parametrom epsilon.

    Parameters:
        points(list): Zoznam vstupnych suradnic bodov.
        
        epsilon(float): "Prahova" hodnota, ktora urcuje intenzitu generalizacie.
            Cim je tato hodnota vyssia, tym menej bodov bude tvorit vystupnu liniu.
    
    Returns:
        vertices_dump(list): Zoznam vystupnych bodov po generalizacii.

    '''
    # Definovanie prveho a posledneho bodu v zozname,
    # na zaklade ktorych sa vypocita zakladna trojuholnika
    start, end = points[0], points[-1]
    base = distance(start[0], start[1], end[0], end[1])
    max_length = 0
    max_length_index = 0
    vertices_dump = []

    # Prechadzanie vsetkych bodov medzi prvym a poslednym bodom
    for point in points[1:-1]:
        area = calculate_area(start[0], start[1], point[0], point[1], end[0], end[1])
        
        # Vypocet vzdialenosti bodu od zakladne
        # danej prvym a poslednym bodom 
        distance_to_base = triangle_height(base, area)

        # Ukladanie indexu a vzdialenosti najvzdialenejsieho bodu
        if max_length == 0 or max_length < distance_to_base:
            max_length = distance_to_base
            max_length_index = points.index(point)
    
    # Vzdialenost najvzdialenejsieho bodu sa porovnava s epsilonom,
    # ak je vacsia, bod sa ponecha a linia sa rozdeli na dve casti,
    # na ktorych je opat funkcia aplikovana
    if max_length > epsilon:
        left_side = douglas_peucker(points[:max_length_index+1], epsilon)
        vertices_dump += [list(vertex) for vertex in left_side if list(vertex) not in vertices_dump]
        right_side = douglas_peucker(points[max_length_index:], epsilon)
        vertices_dump += [list(vertex) for vertex in right_side if list(vertex) not in vertices_dump]
    
    else:
        vertices_dump += [points[0], points[-1]]
    
    # Vratenie bodov po zjednoduseni
    return vertices_dump

def create_figure(graph1_x, graph1_y, graph2_x, graph2_y):
    '''
    Vizualizovanie vstupnej a zjednodusenej linie. 

    Parameters:
        graph1_x(y)(list): Zoznam suradnic bodov vstupnej linie.
        
        graph2_x(y)(list): Zoznam suradnic bodov zjednodusenej linie.

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

# Nacitanie dat zo suboru
try:
    with open ("sample_line.json", encoding="utf-8") as sample_line:
        lines = json.load(sample_line)
        points = lines["features"][0]["geometry"]["paths"][0]

except IOError as e:
    raise IOError(f'{e}.\nSubor neexistuje. Skontrolujte, ci je spravne pomenovany, v spravnom adresari, a spustite skript znova.')

except KeyError as e:
    raise KeyError(f"{e}.\nSubor nema vsetky pozadovane atributy, opravte ho a spustite skript znova.")

# Nastavenie hodnoty epsilon, ! v S-JTSK su potrebne vyssie hodnoty pre prejavenie zmeny !
set_epsilon = 50

# Ulozenie vystupnej zjednodusenej linie, spustenie algoritmu
result = np.array(douglas_peucker(points, set_epsilon))

# Transponovanie suradnic pre vizualizaciu
x, y = np.array(points).T
xs, ys = result.T

# Vytvorenie vystupneho suboru
to_json = {
    "features": {
        "geometry": result.tolist()
    }
}

with open("simplified_line.json","w", encoding="utf-8") as output:
    json.dump(to_json, output, ensure_ascii = False, indent = 2)

# Vizualizacia algoritmu pred a po prevedeni
create_figure(x, y, xs, ys)