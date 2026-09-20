import math
from core.mechanics import distance_and_direction
import networkx as nx
from scipy.spatial import Delaunay

def expanse(cells):
    
    total_area = sum(math.pi * (cell.radius)**2 for cell in cells)
    center_x = sum(math.pi * (cell.radius)**2 * cell.pos[0] for cell in cells)/ total_area
    center_y = sum(math.pi * (cell.radius)**2 * cell.pos[1] for cell in cells)/ total_area

    center_of_mass = (center_x, center_y)

    expanse = max(
    distance_and_direction(cell.pos, center_of_mass)[0] + cell.radius 
    for cell in cells
    )


    return expanse

def sparsity(cells):

    total_area = sum(math.pi * (cell.radius)**2 for cell in cells)

    sparsity = (math.pi * (expanse(cells)**2))/total_area

    return sparsity

def build_spatial_graph(cells):

    position = [cell.pos for cell in cells]

    tri = Delaunay(position)

    edges = set()
    for simplex in tri.simplices:
        i, j, k = simplex
        edges.add(tuple(sorted((i,j))))
        edges.add(tuple(sorted((j,k))))
        edges.add(tuple(sorted((i,k))))

    G = nx.Graph()

    for i, cell in enumerate(cells):
        G.add_node(i, cell=cell)
    G.add_edges_from(edges)

    return G

def build_lineage_graph(cells):
    
    G_l = nx.DiGraph()

    for i, cell in enumerate(cells):
        G_l.add_node(i, cell=cell)

    id_to_index = {cell.id : i for i, cell in enumerate(cells)}

    for cell in cells:
        if cell.mother_id != -1:

            G_l.add_edge(id_to_index[cell.mother_id], id_to_index[cell.id])

    return G_l